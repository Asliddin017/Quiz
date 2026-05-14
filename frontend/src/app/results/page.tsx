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

function JustFinishedCard() {
  const params = useSearchParams();
  const score = params.get('score');
  const total = params.get('total');
  const correct = params.get('correct');
  const pct = params.get('pct');

  if (!score) return null;

  const pctNum = parseFloat(pct || '0');
  const color = pctNum >= 80 ? 'text-green-400' : pctNum >= 50 ? 'text-yellow-400' : 'text-red-400';

  return (
    <div className="bg-gray-900 border border-blue-600 rounded-xl p-6 mb-8 text-center">
      <p className="text-gray-400 text-sm mb-2">Oxirgi natija</p>
      <p className={`text-5xl font-bold mb-2 ${color}`}>{pct}%</p>
      <p className="text-gray-300">
        {correct} ta to'g'ri / {total} ta savol · {score} ball
      </p>
    </div>
  );
}

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) { router.push('/login'); return; }
    api.get<Result[]>('/results/me')
      .then(setResults)
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
      <h1 className="text-3xl font-bold mb-2">Mening natijalarim</h1>
      <p className="text-gray-400 mb-8">Barcha tugatilgan testlar</p>

      <JustFinishedCard />

      {results.length === 0 && (
        <div className="text-center text-gray-500 py-16">
          <p className="text-lg">Hali test topshirilmagan</p>
          <Link href="/" className="text-blue-400 hover:underline text-sm mt-2 inline-block">
            Testlarga o'tish
          </Link>
        </div>
      )}

      <div className="space-y-3">
        {results.map((r) => {
          const color = r.percentage >= 80 ? 'text-green-400' : r.percentage >= 50 ? 'text-yellow-400' : 'text-red-400';
          return (
            <div key={r.id} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex items-center justify-between">
              <div>
                <p className="font-medium">{r.quiz_title}</p>
                <p className="text-sm text-gray-400 mt-0.5">
                  {r.correct_answers}/{r.total_questions} to'g'ri ·{' '}
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
