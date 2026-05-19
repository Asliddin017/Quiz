'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken } from '@/lib/auth';

interface Result {
  id: number;
  quiz_id: number;
  quiz_title: string;
  score: number;
  total_questions: number;
  correct_answers: number;
  percentage: number;
  created_at: string;
}

interface QuestionReview {
  questionId: number;
  questionText: string;
  userChoiceText: string | null;
  correctChoiceText: string | null;
  isCorrect: boolean;
  answered: boolean;
}

interface ReviewData {
  quizId: number;
  quizTitle: string;
  questions: QuestionReview[];
}

const PASS_PCT = 60;

function JustFinishedSection() {
  const params = useSearchParams();
  const score  = params.get('score');
  const total  = params.get('total');
  const correct = params.get('correct');
  const pct    = params.get('pct');
  const quizId = params.get('quizId');

  const [review, setReview] = useState<ReviewData | null>(null);

  useEffect(() => {
    try {
      const raw = sessionStorage.getItem('lastQuizReview');
      if (raw) setReview(JSON.parse(raw));
    } catch {}
  }, []);

  if (!score) return null;

  const pctNum    = parseFloat(pct ?? '0');
  const totalNum  = parseInt(total ?? '0');
  const correctNum = parseInt(correct ?? '0');
  const wrongNum  = totalNum - correctNum;
  const passed    = pctNum >= PASS_PCT;

  const scoreColor =
    pctNum >= 80 ? 'text-green-400' :
    pctNum >= 60 ? 'text-yellow-400' :
    'text-red-400';

  return (
    <div className="mb-10">
      {/* ── Score card ── */}
      <div className="bg-gray-900 border border-blue-600/40 rounded-2xl p-6 mb-5">
        <div className="text-center mb-5">
          <p className="text-sm text-gray-400 mb-1">{review?.quizTitle ?? 'Natija'}</p>
          <p className={`text-6xl font-bold mb-3 ${scoreColor}`}>{pct}%</p>
          <span className={`inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-semibold border ${
            passed
              ? 'bg-green-900/30 border-green-600 text-green-300'
              : 'bg-red-900/30 border-red-600 text-red-300'
          }`}>
            {passed ? "✅ O'tdingiz!" : "❌ O'tolmadingiz"}
            <span className="text-xs font-normal opacity-70">({PASS_PCT}% dan yuqori kerak)</span>
          </span>
        </div>

        <div className="grid grid-cols-3 gap-3 text-center">
          <div className="bg-gray-800 rounded-xl p-3">
            <p className="text-2xl font-bold text-white">{totalNum}</p>
            <p className="text-xs text-gray-400 mt-0.5">Jami savol</p>
          </div>
          <div className="bg-green-950/50 border border-green-900 rounded-xl p-3">
            <p className="text-2xl font-bold text-green-400">{correctNum}</p>
            <p className="text-xs text-gray-400 mt-0.5">To&apos;g&apos;ri</p>
          </div>
          <div className="bg-red-950/50 border border-red-900 rounded-xl p-3">
            <p className="text-2xl font-bold text-red-400">{wrongNum}</p>
            <p className="text-xs text-gray-400 mt-0.5">Noto&apos;g&apos;ri</p>
          </div>
        </div>
      </div>

      {/* ── Action buttons ── */}
      <div className="flex gap-3 mb-8">
        {quizId && (
          <Link
            href={`/quiz/${quizId}`}
            className="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-xl font-medium transition"
          >
            🔄 Qayta urinish
          </Link>
        )}
        <Link
          href="/"
          className="flex-1 text-center bg-gray-800 hover:bg-gray-700 text-gray-200 py-2.5 rounded-xl font-medium transition"
        >
          🏠 Bosh sahifa
        </Link>
      </div>

      {/* ── Question review ── */}
      {review && review.questions.length > 0 && (
        <div>
          <h2 className="text-xl font-bold mb-1">Savollar sharhi</h2>
          <p className="text-sm text-gray-400 mb-4">
            {review.questions.filter(q => q.isCorrect).length} ta to&apos;g&apos;ri ·{' '}
            {review.questions.filter(q => !q.isCorrect && q.answered).length} ta noto&apos;g&apos;ri ·{' '}
            {review.questions.filter(q => !q.answered).length} ta javobsiz
          </p>

          <div className="space-y-2">
            {review.questions.map((q, i) => {
              const border =
                !q.answered ? 'border-gray-700 bg-gray-900' :
                q.isCorrect ? 'border-green-800/50 bg-green-950/20' :
                'border-red-800/50 bg-red-950/20';

              return (
                <div key={q.questionId} className={`rounded-xl border p-4 ${border}`}>
                  <div className="flex items-start gap-3">
                    {/* Status icon */}
                    <span className="mt-0.5 shrink-0 text-base leading-none">
                      {!q.answered ? '⬜' : q.isCorrect ? '✅' : '❌'}
                    </span>

                    <div className="flex-1 min-w-0">
                      {/* Question text */}
                      <p className="text-sm text-gray-200 font-medium mb-1.5">
                        {i + 1}. {q.questionText}
                      </p>

                      {/* Answer details */}
                      {!q.answered ? (
                        <p className="text-xs text-gray-500 italic">Javob berilmadi</p>
                      ) : q.isCorrect ? (
                        <p className="text-xs text-green-400">✅ {q.userChoiceText}</p>
                      ) : (
                        <div className="space-y-0.5">
                          <p className="text-xs text-red-400">❌ Sizning javobingiz: {q.userChoiceText ?? '—'}</p>
                          <p className="text-xs text-green-400">✅ To&apos;g&apos;ri javob: {q.correctChoiceText ?? '—'}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState('');

  useEffect(() => {
    if (!getToken()) { router.push('/login'); return; }
    api.get<Result[]>('/results/me')
      .then(setResults)
      .catch((e: unknown) => setFetchError(e instanceof Error ? e.message : 'Natijalar yuklanmadi'))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div>
      {/* Shows only when arriving from a finished quiz */}
      <JustFinishedSection />

      <h1 className="text-3xl font-bold mb-2">Mening natijalarim</h1>
      <p className="text-gray-400 mb-8">Barcha tugatilgan testlar</p>

      {fetchError && (
        <div className="bg-red-900/30 border border-red-600/50 text-red-300 px-4 py-3 rounded-xl mb-6 text-sm">
          {fetchError}
        </div>
      )}

      {results.length === 0 && !fetchError && (
        <div className="text-center text-gray-500 py-16">
          <p className="text-lg">Hali test topshirilmagan</p>
          <Link href="/" className="text-blue-400 hover:underline text-sm mt-2 inline-block">
            Testlarga o&apos;tish
          </Link>
        </div>
      )}

      <div className="space-y-3">
        {results.map((r) => {
          const color =
            r.percentage >= 80 ? 'text-green-400' :
            r.percentage >= 60 ? 'text-yellow-400' :
            'text-red-400';
          return (
            <div key={r.id} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex items-center justify-between">
              <div>
                <p className="font-medium">{r.quiz_title}</p>
                <p className="text-sm text-gray-400 mt-0.5">
                  {r.correct_answers}/{r.total_questions} to&apos;g&apos;ri ·{' '}
                  {new Date(r.created_at).toLocaleDateString('uz')}
                </p>
              </div>
              <div className="text-right">
                <p className={`text-2xl font-bold ${color}`}>{r.percentage}%</p>
                <p className="text-sm text-gray-400">{r.score} ball</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
