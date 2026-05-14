'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken, getUser } from '@/lib/auth';

interface QuestionDetail {
  question: string;
  selected: string;
  correct_answer: string;
  is_correct: boolean;
}

interface StudentResult {
  username: string;
  score: number;
  correct_answers: number;
  total_questions: number;
  percentage: number;
  finished_at: string;
  questions: QuestionDetail[];
}

interface QuizStats {
  quiz_id: number;
  quiz_title: string;
  total_participants: number;
  students: StudentResult[];
}

export default function QuizStatsPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [stats, setStats] = useState<QuizStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    const user = getUser();
    if (!getToken() || user?.role !== 'admin') { router.push('/'); return; }
    api.get<QuizStats>(`/quizzes/${params.id}/stats`)
      .then(setStats)
      .finally(() => setLoading(false));
  }, [params.id, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!stats) return <p className="text-red-400">Ma'lumot topilmadi</p>;

  return (
    <div className="max-w-4xl mx-auto">
      <button onClick={() => router.push('/admin')} className="text-gray-400 hover:text-white text-sm mb-6 flex items-center gap-1">
        ← Orqaga
      </button>

      <h1 className="text-2xl font-bold mb-1">{stats.quiz_title}</h1>
      <p className="text-gray-400 mb-6">Jami ishtirokchilar: <span className="text-white font-semibold">{stats.total_participants}</span></p>

      {stats.students.length === 0 && (
        <div className="text-center text-gray-500 py-16">
          <p>Hali hech kim bu testni topshirmagan</p>
        </div>
      )}

      <div className="space-y-3">
        {stats.students.map((s, i) => {
          const color = s.percentage >= 80 ? 'text-green-400' : s.percentage >= 50 ? 'text-yellow-400' : 'text-red-400';
          const isOpen = expanded === s.username + i;
          return (
            <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              {/* Student row */}
              <button
                onClick={() => setExpanded(isOpen ? null : s.username + i)}
                className="w-full flex items-center justify-between px-5 py-4 hover:bg-gray-800 transition"
              >
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold">
                    {s.username[0].toUpperCase()}
                  </div>
                  <div className="text-left">
                    <p className="font-medium">{s.username}</p>
                    <p className="text-sm text-gray-400">
                      {s.correct_answers}/{s.total_questions} to'g'ri · {new Date(s.finished_at).toLocaleString('uz')}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className={`text-xl font-bold ${color}`}>{s.percentage}%</p>
                    <p className="text-sm text-gray-400">{s.score} ball</p>
                  </div>
                  <span className="text-gray-500">{isOpen ? '▲' : '▼'}</span>
                </div>
              </button>

              {/* Savol tafsilotlari */}
              {isOpen && (
                <div className="border-t border-gray-800 px-5 py-4 space-y-3">
                  {s.questions.map((q, qi) => (
                    <div key={qi} className={`rounded-lg p-3 border ${q.is_correct ? 'border-green-700/50 bg-green-900/10' : 'border-red-700/50 bg-red-900/10'}`}>
                      <p className="text-sm font-medium mb-2">{qi + 1}. {q.question}</p>
                      <div className="flex flex-col gap-1 text-sm">
                        <p>
                          <span className="text-gray-400">Tanlagan: </span>
                          <span className={q.is_correct ? 'text-green-400' : 'text-red-400'}>
                            {q.selected} {q.is_correct ? '✓' : '✗'}
                          </span>
                        </p>
                        {!q.is_correct && (
                          <p>
                            <span className="text-gray-400">To'g'ri javob: </span>
                            <span className="text-green-400">{q.correct_answer}</span>
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
