'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken } from '@/lib/auth';

interface Quiz {
  id: number;
  title: string;
  description: string | null;
  duration_minutes: number;
  question_count: number;
}

export default function HomePage() {
  const router = useRouter();
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!getToken()) {
      router.push('/login');
      return;
    }
    api.get<Quiz[]>('/quizzes')
      .then(setQuizzes)
      .catch((e) => setError(e.message))
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
      {/* Hero */}
      <div className="mb-10">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
          Testlar
        </h1>
        <p className="text-gray-400">Istalgan testni tanlang va boshlang</p>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-600/50 text-red-300 px-4 py-3 rounded-xl mb-6 text-sm">
          {error}
        </div>
      )}

      {quizzes.length === 0 && !error && (
        <div className="text-center py-20">
          <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">📝</div>
          <p className="text-gray-400 font-medium">Hozircha testlar yo'q</p>
          <p className="text-sm text-gray-600 mt-1">Admin yangi test qo'shishi kerak</p>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {quizzes.map((quiz) => (
          <Link key={quiz.id} href={`/quiz/${quiz.id}`} className="group">
            <div className="card p-5 hover:border-blue-600/60 hover:bg-gray-800/50 transition-all duration-200 cursor-pointer h-full flex flex-col">
              <div className="flex-1">
                <h2 className="font-semibold text-lg mb-2 text-white group-hover:text-blue-400 transition-colors">
                  {quiz.title}
                </h2>
                {quiz.description && (
                  <p className="text-gray-500 text-sm mb-4 line-clamp-2">{quiz.description}</p>
                )}
              </div>
              <div className="flex items-center gap-3 mt-4 pt-4 border-t border-gray-800">
                <span className="flex items-center gap-1.5 text-xs text-gray-500 bg-gray-800 px-2.5 py-1 rounded-lg">
                  ⏱ {quiz.duration_minutes} daqiqa
                </span>
                <span className="flex items-center gap-1.5 text-xs text-gray-500 bg-gray-800 px-2.5 py-1 rounded-lg">
                  ❓ {quiz.question_count} savol
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
