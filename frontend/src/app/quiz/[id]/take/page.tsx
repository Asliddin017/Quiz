'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken } from '@/lib/auth';

interface Choice { id: number; text: string; }
interface Question { id: number; text: string; order: number; choices: Choice[]; }
interface Quiz {
  id: number; title: string; duration_minutes: number;
  questions: Question[];
}

export default function TakeQuizPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session');

  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [remaining, setRemaining] = useState<number | null>(null);
  const [timeUp, setTimeUp] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [currentQ, setCurrentQ] = useState(0);

  const wsRef = useRef<WebSocket | null>(null);
  const savingRef = useRef<Record<number, boolean>>({});

  useEffect(() => {
    const token = getToken();
    if (!token || !sessionId) { router.push('/login'); return; }

    api.get<Quiz>(`/quizzes/${params.id}`).then((q) => {
      const sorted = [...q.questions].sort((a, b) => a.order - b.order);
      setQuiz({ ...q, questions: sorted });
    });

    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/api/v1/ws/session/${sessionId}?token=${token}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'timer') {
        setRemaining(data.remaining_seconds);
        setError('');
      }
      if (data.type === 'time_up') {
        setTimeUp(true);
        setRemaining(0);
        // Vaqt tugadi — avtomatik yakunlash
        setTimeout(() => {
          document.getElementById('auto-finish-btn')?.click();
        }, 500);
      }
    };
    ws.onerror = () => setError('WebSocket ulanishda xato');

    return () => ws.close();
  }, [params.id, sessionId, router]);

  const saveAnswer = useCallback(async (questionId: number, choiceId: number) => {
    if (savingRef.current[questionId]) return;
    savingRef.current[questionId] = true;
    try {
      await api.post(`/sessions/${sessionId}/answer`, {
        question_id: questionId,
        choice_id: choiceId,
      });
    } catch {
      // silent — javob saqlanmasa ham davom etaveradi
    } finally {
      savingRef.current[questionId] = false;
    }
  }, [sessionId]);

  const handleChoice = (questionId: number, choiceId: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceId }));
    saveAnswer(questionId, choiceId);
  };

  const handleFinish = async () => {
    setSubmitting(true);
    setError('');
    try {
      const result = await api.post<{
        score: number; total_questions: number;
        correct_answers: number; percentage: number;
      }>(`/sessions/${sessionId}/finish`);
      wsRef.current?.close();
      router.push(
        `/results?score=${result.score}&total=${result.total_questions}&correct=${result.correct_answers}&pct=${result.percentage}`
      );
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Xato yuz berdi');
      setSubmitting(false);
    }
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  if (!quiz) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  const questions = quiz.questions;
  const q = questions[currentQ];
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="max-w-2xl mx-auto">
      {/* Yashirin avtomatik yakunlash tugmasi */}
      <button id="auto-finish-btn" onClick={handleFinish} className="hidden" />

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-bold truncate">{quiz.title}</h1>
        <div className={`font-mono text-lg font-bold px-4 py-1.5 rounded-lg ${
          remaining !== null && remaining < 60
            ? 'bg-red-900 text-red-300 animate-pulse'
            : 'bg-gray-800 text-blue-400'
        }`}>
          {remaining !== null ? formatTime(remaining) : '--:--'}
        </div>
      </div>

      {/* Progress */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-400 mb-1">
          <span>Savol {currentQ + 1} / {questions.length}</span>
          <span>{answeredCount} ta javob berildi</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-1.5">
          <div
            className="bg-blue-500 h-1.5 rounded-full transition-all"
            style={{ width: `${((currentQ + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      {timeUp && (
        <div className="bg-red-900/40 border border-red-600 text-red-300 px-4 py-3 rounded-lg mb-4 text-sm font-medium">
          Vaqt tugadi! Iltimos testni yakunlang.
        </div>
      )}

      {error && (
        <div className="bg-red-900/40 border border-red-600 text-red-300 px-4 py-3 rounded-lg mb-4 text-sm">
          {error}
        </div>
      )}

      {/* Question card */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
        <p className="text-lg font-medium mb-5">{q.text}</p>
        <div className="space-y-3">
          {q.choices.map((choice) => {
            const selected = answers[q.id] === choice.id;
            return (
              <button
                key={choice.id}
                onClick={() => handleChoice(q.id, choice.id)}
                disabled={timeUp && submitting}
                className={`w-full text-left px-4 py-3 rounded-lg border transition ${
                  selected
                    ? 'border-blue-500 bg-blue-900/30 text-white'
                    : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-gray-500'
                }`}
              >
                {choice.text}
              </button>
            );
          })}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between gap-3">
        <button
          onClick={() => setCurrentQ((p) => Math.max(0, p - 1))}
          disabled={currentQ === 0}
          className="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:border-gray-500 disabled:opacity-30 transition"
        >
          ← Oldingi
        </button>

        {currentQ < questions.length - 1 ? (
          <button
            onClick={() => setCurrentQ((p) => p + 1)}
            className="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:border-gray-500 transition"
          >
            Keyingi →
          </button>
        ) : (
          <button
            onClick={handleFinish}
            disabled={submitting}
            className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium transition"
          >
            {submitting ? 'Yakunlanmoqda...' : 'Testni yakunlash'}
          </button>
        )}
      </div>

      {/* Question dots */}
      <div className="mt-6 flex flex-wrap gap-2">
        {questions.map((question, i) => (
          <button
            key={question.id}
            onClick={() => setCurrentQ(i)}
            className={`w-8 h-8 rounded text-xs font-medium transition ${
              i === currentQ
                ? 'bg-blue-600 text-white'
                : answers[question.id]
                ? 'bg-green-700 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
