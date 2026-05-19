'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken } from '@/lib/auth';

interface Choice { id: number; text: string; }
interface Question { id: number; text: string; order: number; choices: Choice[]; }
interface Quiz { id: number; title: string; duration_minutes: number; questions: Question[]; }

interface Feedback { isCorrect: boolean; correctChoiceId: number; }

interface QuestionReview {
  questionId: number;
  questionText: string;
  userChoiceId: number | null;
  userChoiceText: string | null;
  correctChoiceId: number | null;
  correctChoiceText: string | null;
  isCorrect: boolean;
  answered: boolean;
}

function buildReview(
  quiz: Quiz,
  answers: Record<number, number>,
  revealed: Record<number, Feedback>,
): { quizId: number; quizTitle: string; questions: QuestionReview[] } {
  return {
    quizId: quiz.id,
    quizTitle: quiz.title,
    questions: quiz.questions.map((q) => {
      const fb = revealed[q.id];
      const userChoiceId = answers[q.id] ?? null;
      const userChoice = q.choices.find((c) => c.id === userChoiceId);
      const correctChoice = fb ? q.choices.find((c) => c.id === fb.correctChoiceId) : null;
      return {
        questionId: q.id,
        questionText: q.text,
        userChoiceId,
        userChoiceText: userChoice?.text ?? null,
        correctChoiceId: fb?.correctChoiceId ?? null,
        correctChoiceText: correctChoice?.text ?? null,
        isCorrect: fb?.isCorrect ?? false,
        answered: userChoiceId !== null,
      };
    }),
  };
}

export default function TakeQuizPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session');

  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [revealed, setRevealed] = useState<Record<number, Feedback>>({});
  const [remaining, setRemaining] = useState<number | null>(null);
  const [timeUp, setTimeUp] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [currentQ, setCurrentQ] = useState(0);

  const wsRef = useRef<WebSocket | null>(null);
  const savingRef = useRef<Record<number, boolean>>({});
  const handleFinishRef = useRef<() => Promise<void>>(async () => {});

  // Mutable refs so the timer-triggered handleFinish sees current state
  const quizRef = useRef<Quiz | null>(null);
  const answersRef = useRef<Record<number, number>>({});
  const revealedRef = useRef<Record<number, Feedback>>({});
  useEffect(() => { quizRef.current = quiz; }, [quiz]);
  useEffect(() => { answersRef.current = answers; }, [answers]);
  useEffect(() => { revealedRef.current = revealed; }, [revealed]);

  const handleFinish = async () => {
    setSubmitting(true);
    setError('');
    try {
      const currentQuiz = quizRef.current;
      if (currentQuiz) {
        const reviewData = buildReview(currentQuiz, answersRef.current, revealedRef.current);
        sessionStorage.setItem('lastQuizReview', JSON.stringify(reviewData));
      }

      const result = await api.post<{
        score: number; total_questions: number;
        correct_answers: number; percentage: number;
      }>(`/sessions/${sessionId}/finish`);

      wsRef.current?.close();
      router.push(
        `/results?score=${result.score}&total=${result.total_questions}` +
        `&correct=${result.correct_answers}&pct=${result.percentage}` +
        `&quizId=${quizRef.current?.id ?? ''}`,
      );
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Xato yuz berdi');
      setSubmitting(false);
    }
  };
  handleFinishRef.current = handleFinish;

  useEffect(() => {
    const token = getToken();
    if (!token || !sessionId) { router.push('/login'); return; }

    api.get<Quiz>(`/quizzes/${params.id}`)
      .then((q) => {
        const sorted = [...q.questions].sort((a, b) => a.order - b.order);
        setQuiz({ ...q, questions: sorted });
      })
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'Quiz yuklanmadi'));

    const wsUrl =
      `${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/api/v1/ws/session/${sessionId}?token=${token}`;
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
        setTimeout(() => handleFinishRef.current(), 500);
      }
    };
    ws.onerror = () => setError('WebSocket ulanishda xato');

    return () => ws.close();
  }, [params.id, sessionId, router]);

  const handleChoice = async (questionId: number, choiceId: number) => {
    if (revealed[questionId] !== undefined || savingRef.current[questionId]) return;

    setAnswers((prev) => ({ ...prev, [questionId]: choiceId }));
    savingRef.current[questionId] = true;

    try {
      const resp = await api.post<{ ok: boolean; is_correct: boolean; correct_choice_id: number }>(
        `/sessions/${sessionId}/answer`,
        { question_id: questionId, choice_id: choiceId },
      );
      setRevealed((prev) => ({
        ...prev,
        [questionId]: { isCorrect: resp.is_correct, correctChoiceId: resp.correct_choice_id },
      }));
    } catch {
      // Silent — selection is recorded locally even if colors won't show
    } finally {
      savingRef.current[questionId] = false;
    }
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  if (!quiz) {
    if (error) return <p className="text-red-400 mt-8 text-center">{error}</p>;
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  const questions = quiz.questions;
  const q = questions[currentQ];
  const feedback = revealed[q.id];
  const isAnswered = feedback !== undefined;
  const answeredCount = Object.keys(revealed).length;

  const getChoiceStyle = (choiceId: number): string => {
    if (!feedback) {
      return answers[q.id] === choiceId
        ? 'border-blue-500 bg-blue-900/30 text-white'
        : 'border-gray-700 bg-gray-800 text-gray-300 hover:border-gray-500';
    }
    if (choiceId === feedback.correctChoiceId) return 'border-green-500 bg-green-900/30 text-green-200';
    if (choiceId === answers[q.id]) return 'border-red-500 bg-red-900/30 text-red-300';
    return 'border-gray-700 bg-gray-800/40 text-gray-600';
  };

  const getChoicePrefix = (choiceId: number): string => {
    if (!feedback) return '';
    if (choiceId === feedback.correctChoiceId) return '✅ ';
    if (choiceId === answers[q.id] && !feedback.isCorrect) return '❌ ';
    return '';
  };

  const getDotStyle = (i: number, question: Question): string => {
    if (i === currentQ) return 'bg-blue-600 text-white';
    const fb = revealed[question.id];
    if (fb?.isCorrect) return 'bg-green-700 text-white';
    if (fb && !fb.isCorrect) return 'bg-red-700 text-white';
    if (answers[question.id]) return 'bg-yellow-700/80 text-white';
    return 'bg-gray-800 text-gray-400 hover:bg-gray-700';
  };

  return (
    <div className="max-w-2xl mx-auto">
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
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-4">
        <p className="text-lg font-medium mb-5">{q.text}</p>
        <div className="space-y-3">
          {q.choices.map((choice) => (
            <button
              key={choice.id}
              onClick={() => handleChoice(q.id, choice.id)}
              disabled={isAnswered || (timeUp && submitting)}
              className={`w-full text-left px-4 py-3 rounded-lg border transition disabled:cursor-default ${getChoiceStyle(choice.id)}`}
            >
              {getChoicePrefix(choice.id)}{choice.text}
            </button>
          ))}
        </div>

        {/* Feedback banner */}
        {feedback && (
          <div className={`mt-4 px-4 py-2.5 rounded-lg text-sm font-medium ${
            feedback.isCorrect
              ? 'bg-green-900/30 border border-green-700 text-green-300'
              : 'bg-red-900/30 border border-red-700 text-red-300'
          }`}>
            {feedback.isCorrect
              ? "✅ To'g'ri javob!"
              : "❌ Noto'g'ri. To'g'ri javob yashil bilan belgilangan."}
          </div>
        )}
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
            className={`px-5 py-2 rounded-lg font-medium transition ${
              isAnswered
                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                : 'border border-gray-700 text-gray-300 hover:border-gray-500'
            }`}
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
            className={`w-8 h-8 rounded text-xs font-medium transition ${getDotStyle(i, question)}`}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
