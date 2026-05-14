'use client';

import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { getUser, logout, AuthUser } from '@/lib/auth';

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => { setUser(getUser()); }, [pathname]);

  const handleLogout = () => {
    logout();
    setUser(null);
    router.push('/login');
  };

  return (
    <nav className="bg-gray-900/80 backdrop-blur-md border-b border-gray-800 sticky top-0 z-50 px-4 py-3">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white text-sm group-hover:bg-blue-500 transition">Q</div>
          <span className="font-bold text-white tracking-tight">QuizPlatform</span>
        </Link>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <div className="flex items-center gap-2 bg-gray-800 rounded-xl px-3 py-1.5 text-sm">
                <div className="w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xs">
                  {user.username[0].toUpperCase()}
                </div>
                <span className="text-gray-200 hidden sm:block">{user.username}</span>
                {user.role === 'admin' && (
                  <span className="bg-blue-500/20 text-blue-400 text-xs px-1.5 py-0.5 rounded-md border border-blue-500/30">
                    Admin
                  </span>
                )}
              </div>

              <Link href="/results" className="text-gray-400 hover:text-white text-sm transition px-2 py-1 rounded-lg hover:bg-gray-800">
                Natijalar
              </Link>
              {user.role === 'admin' && (
                <Link href="/admin" className="text-gray-400 hover:text-white text-sm transition px-2 py-1 rounded-lg hover:bg-gray-800">
                  Boshqaruv
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="text-red-400 hover:text-white hover:bg-red-600 border border-red-600/30 hover:border-red-600 text-sm px-3 py-1.5 rounded-lg transition-all duration-150"
              >
                Chiqish
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-gray-400 hover:text-white text-sm transition px-3 py-1.5 rounded-lg hover:bg-gray-800">
                Kirish
              </Link>
              <Link href="/register" className="bg-blue-600 hover:bg-blue-500 text-white text-sm px-4 py-1.5 rounded-lg transition font-medium">
                Ro'yxatdan o'tish
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
