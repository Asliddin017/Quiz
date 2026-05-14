'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken } from '@/lib/auth';

interface Quiz {
  id: number;
  title: string;
  description: string | null;
  duration_minutes: number;
  questions: { id: number; text: string; choices: { id: number; text: string }[] }[];
}

export default function QuizDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!getToken()) { router.push('/login'); return; }
    api.get<Quiz>(`/quizzes/${params.id}`)
      .then(setQuiz)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [params.id, router]);

  const startQuiz = async () => {
    setStarting(true);
    setError('');
    try {
      const { session_id } = await api.post<{ session_id: number; quiz_id: number; duration_minutes: number }>(
        `/sessions/start/${params.id}`
      );
      router.push(`/quiz/${params.id}/take?session=${session_id}`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Xato yuz berdi');
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!quiz) return <p className="text-red-400">{error || 'Quiz topilmadi'}</p>;

  return (
    <div className="max-w-2xl mx-auto">
      <button onClick={() => router.back()} className="text-gray-400 hover:text-white text-sm mb-6 flex items-center gap-1">
        ← Orqaga
      </button>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
        <h1 className="text-2xl font-bold mb-3">{quiz.title}</h1>
        {quiz.description && <p className="text-gray-400 mb-4">{quiz.description}</p>}
        <div className="flex gap-6 text-sm text-gray-400">
          <span>⏱ {quiz.duration_minutes} daqiqa</span>
          <span>❓ {quiz.questions.length} ta savol</span>
        </div>
      </div>

      {error && (
        <div className="bg-red-900/40 border border-red-600 text-red-300 px-4 py-3 rounded-lg mb-4 text-sm">
          {error}
        </div>
      )}

      <div className="bg-yellow-900/20 border border-yellow-700/40 rounded-xl p-4 mb-6 text-sm text-yellow-300">
        <strong>Diqqat:</strong> Test boshlanganidan so'ng vaqt hisoblana boshlaydi.
        Barcha savollarga javob bering va tugmasini bosing.
      </div>

      <button
        onClick={startQuiz}
        disabled={starting}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-3 rounded-xl font-semibold text-lg transition"
      >
        {starting ? 'Boshlanmoqda...' : 'Testni boshlash'}
      </button>
    </div>
  );
}
