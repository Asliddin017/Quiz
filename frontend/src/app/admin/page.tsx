'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { getToken, getUser } from '@/lib/auth';

interface QuizItem { id: number; title: string; question_count: number; }

interface ChoiceForm { text: string; is_correct: boolean; }
interface QuestionForm { text: string; choices: ChoiceForm[]; }

const defaultChoice = (): ChoiceForm => ({ text: '', is_correct: false });
const defaultQuestion = (): QuestionForm => ({
  text: '',
  choices: [defaultChoice(), defaultChoice(), defaultChoice(), defaultChoice()],
});

export default function AdminPage() {
  const router = useRouter();
  const [quizzes, setQuizzes] = useState<QuizItem[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [duration, setDuration] = useState(10);
  const [questions, setQuestions] = useState<QuestionForm[]>([defaultQuestion()]);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const token = getToken();
    const user = getUser();
    if (!token || user?.role !== 'admin') { router.push('/'); return; }
    api.get<QuizItem[]>('/quizzes/my').then(setQuizzes);
  }, [router]);

  const updateQuestion = (qi: number, text: string) => {
    setQuestions((prev) => prev.map((q, i) => (i === qi ? { ...q, text } : q)));
  };

  const updateChoice = (qi: number, ci: number, field: keyof ChoiceForm, value: string | boolean) => {
    setQuestions((prev) =>
      prev.map((q, i) =>
        i === qi
          ? { ...q, choices: q.choices.map((c, j) => (j === ci ? { ...c, [field]: value } : c)) }
          : q
      )
    );
  };

  const setCorrect = (qi: number, ci: number) => {
    setQuestions((prev) =>
      prev.map((q, i) =>
        i === qi
          ? { ...q, choices: q.choices.map((c, j) => ({ ...c, is_correct: j === ci })) }
          : q
      )
    );
  };

  const addQuestion = () => setQuestions((prev) => [...prev, defaultQuestion()]);

  const removeQuestion = (qi: number) =>
    setQuestions((prev) => prev.filter((_, i) => i !== qi));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    for (const [qi, q] of questions.entries()) {
      if (!q.text.trim()) { setError(`${qi + 1}-savol matni bo'sh`); return; }
      if (!q.choices.some((c) => c.is_correct)) {
        setError(`${qi + 1}-savolda to'g'ri javob belgilanmagan`); return;
      }
      if (q.choices.some((c) => !c.text.trim())) {
        setError(`${qi + 1}-savolda bo'sh variant bor`); return;
      }
    }

    setSubmitting(true);
    try {
      await api.post('/quizzes', {
        title,
        description: description || null,
        duration_minutes: duration,
        questions: questions.map((q, i) => ({ ...q, order: i })),
      });
      setSuccess('Test muvaffaqiyatli yaratildi!');
      setTitle('');
      setDescription('');
      setDuration(10);
      setQuestions([defaultQuestion()]);
      api.get<QuizItem[]>('/quizzes/my').then(setQuizzes).catch(() => {});
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Xato yuz berdi');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Admin paneli</h1>
      <p className="text-gray-400 mb-6">Testlarni boshqarish</p>

      {/* Mavjud testlar */}
      {quizzes.length > 0 && (
        <div className="mb-10">
          <h2 className="text-lg font-semibold mb-3 text-gray-300">Yaratilgan testlar</h2>
          <div className="space-y-2">
            {quizzes.map((q) => (
              <div key={q.id} className="bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 flex items-center justify-between">
                <div>
                  <p className="font-medium">{q.title}</p>
                  <p className="text-sm text-gray-400">{q.question_count} ta savol</p>
                </div>
                <Link
                  href={`/admin/quiz/${q.id}/stats`}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-1.5 rounded-lg transition"
                >
                  Natijalarni ko'rish
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      <h2 className="text-xl font-bold mb-6">Yangi test yaratish</h2>

      {success && (
        <div className="bg-green-900/40 border border-green-600 text-green-300 px-4 py-3 rounded-lg mb-6">
          {success}
        </div>
      )}
      {error && (
        <div className="bg-red-900/40 border border-red-600 text-red-300 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Quiz info */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 space-y-4">
          <h2 className="font-semibold text-gray-300">Test ma'lumotlari</h2>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Sarlavha *</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Tavsif</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Vaqt (daqiqa)</label>
            <input
              type="number"
              min={1}
              max={180}
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-32 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {/* Questions */}
        {questions.map((q, qi) => (
          <div key={qi} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-gray-300">{qi + 1}-savol</h3>
              {questions.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeQuestion(qi)}
                  className="text-red-400 hover:text-red-300 text-sm"
                >
                  O'chirish
                </button>
              )}
            </div>
            <textarea
              value={q.text}
              onChange={(e) => updateQuestion(qi, e.target.value)}
              placeholder="Savol matni..."
              rows={2}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 resize-none mb-4"
              required
            />
            <p className="text-xs text-gray-500 mb-2">
              To'g'ri javobni tanlang (radio tugmasi)
            </p>
            <div className="space-y-2">
              {q.choices.map((c, ci) => (
                <div key={ci} className="flex items-center gap-3">
                  <input
                    type="radio"
                    name={`correct-${qi}`}
                    checked={c.is_correct}
                    onChange={() => setCorrect(qi, ci)}
                    className="w-4 h-4 accent-blue-500 flex-shrink-0"
                  />
                  <input
                    value={c.text}
                    onChange={(e) => updateChoice(qi, ci, 'text', e.target.value)}
                    placeholder={`Variant ${ci + 1}`}
                    className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:border-blue-500"
                  />
                </div>
              ))}
            </div>
          </div>
        ))}

        <button
          type="button"
          onClick={addQuestion}
          className="w-full border border-dashed border-gray-600 hover:border-blue-500 text-gray-400 hover:text-blue-400 py-3 rounded-xl transition text-sm"
        >
          + Savol qo'shish
        </button>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white py-3 rounded-xl font-semibold text-lg transition"
        >
          {submitting ? 'Saqlanmoqda...' : 'Testni saqlash'}
        </button>
      </form>
    </div>
  );
}
