'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', username: '', password: '', role: 'student' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.post('/auth/register', form);
      router.push('/login');
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
          <h1 className="text-2xl font-bold">Hisob yaratish</h1>
          <p className="text-gray-400 text-sm mt-1">Platformaga qo'shiling</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-6 space-y-4">
          {error && (
            <div className="bg-red-900/30 border border-red-600/50 text-red-300 px-4 py-3 rounded-xl text-sm">
              {error}
            </div>
          )}
          <div className="space-y-1">
            <label className="block text-sm text-gray-400">Email</label>
            <input type="email" value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="input" placeholder="email@example.com" required />
          </div>
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
          <div className="space-y-1">
            <label className="block text-sm text-gray-400">Rol</label>
            <select value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
              className="input">
              <option value="student">O'quvchi</option>
              <option value="admin">Admin (o'qituvchi)</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-2.5 mt-2">
            {loading ? 'Yuklanmoqda...' : "Ro'yxatdan o'tish"}
          </button>
          <p className="text-center text-sm text-gray-500">
            Hisobingiz bormi?{' '}
            <Link href="/login" className="text-blue-400 hover:text-blue-300 transition">Kiring</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
