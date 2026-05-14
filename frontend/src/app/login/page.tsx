'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { setToken, setUser } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const { access_token } = await api.post<{ access_token: string }>('/auth/login', form);
      setToken(access_token);
      const user = await api.get<{ id: number; email: string; username: string; role: string }>('/auth/me');
      setUser(user);
      router.push('/');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Xato yuz berdi');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center font-black text-white text-xl mx-auto mb-4">Q</div>
          <h1 className="text-2xl font-bold">Xush kelibsiz</h1>
          <p className="text-gray-400 text-sm mt-1">Hisobingizga kiring</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          {error && (
            <div className="bg-red-900/30 border border-red-600/50 text-red-300 px-4 py-3 rounded-xl text-sm">
              {error}
            </div>
          )}
          <div className="space-y-1">
            <label className="block text-sm text-gray-400">Username</label>
            <input type="text" value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              className="input" placeholder="username" required />
          </div>
          <div className="space-y-1">
            <label className="block text-sm text-gray-400">Parol</label>
            <input type="password" value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="input" placeholder="••••••••" required />
          </div>
          <button type="submit" disabled={loading}
            className="btn-primary w-full py-2.5 mt-2">
            {loading ? 'Yuklanmoqda...' : 'Kirish'}
          </button>
          <p className="text-center text-sm text-gray-500">
            Hisobingiz yo'qmi?{' '}
            <Link href="/register" className="text-blue-400 hover:text-blue-300 transition">
              Ro'yxatdan o'ting
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
