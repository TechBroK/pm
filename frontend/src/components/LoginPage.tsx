'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/lib/auth-context';

interface LoginPageProps {
  initialMode?: 'login' | 'signup';
}

export default function LoginPage({ initialMode = 'login' }: LoginPageProps) {
  const { login, signup } = useAuth();
  const [mode, setMode] = useState<'login' | 'signup'>(initialMode);
  const [username, setUsername] = useState(initialMode === 'login' ? 'user' : '');
  const [password, setPassword] = useState(initialMode === 'login' ? 'password' : '');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const usernameInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    usernameInputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (mode === 'login' && !username) {
      setUsername('user');
    }
    if (mode === 'login' && !password) {
      setPassword('password');
    }
  }, [mode, username, password]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    if (!username.trim() || !password.trim()) {
      setError('Username and password are required');
      setIsLoading(false);
      return;
    }

    const success = mode === 'login'
      ? await login(username, password)
      : await signup(username, password);
    
    if (!success) {
      setError(mode === 'login' ? 'Invalid username or password' : 'Could not create that account');
      setPassword('');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100 p-3 sm:p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl p-5 sm:p-6 relative overflow-hidden">
          {/* Accent bar */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-linear-to-r from-[#209dd7] via-[#ecad0a] to-[#753991]" />
          
          {/* Header */}
          <div className="text-center mb-5 sm:mb-6">
            <div className="inline-block mb-2 sm:mb-3">
              <div className="w-12 h-12 rounded-lg bg-linear-to-br from-[#209dd7] to-[#753991] flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
            <h1 className="text-3xl sm:text-4xl font-bold text-[#032147] mb-2">Kanban Studio</h1>
            <p className="text-[#888888]">
              {mode === 'login' ? 'Sign in to your project board' : 'Create a test account for your board'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-[#032147] mb-1.5 sm:mb-2">
                Username
              </label>
              <input
                ref={usernameInputRef}
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder={mode === 'login' ? 'user' : 'choose a username'}
                disabled={isLoading}
                autoComplete="username"
                className="w-full px-3.5 py-2.5 border-2 border-[#ccc] rounded-lg focus:outline-none focus:border-[#209dd7] focus:shadow-[0_0_0_3px_rgba(32,157,215,0.1)] transition-all disabled:bg-gray-100 disabled:text-gray-500"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-[#032147] mb-1.5 sm:mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="password"
                  disabled={isLoading}
                  autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
                  className="w-full px-3.5 py-2.5 border-2 border-[#ccc] rounded-lg focus:outline-none focus:border-[#209dd7] focus:shadow-[0_0_0_3px_rgba(32,157,215,0.1)] transition-all disabled:bg-gray-100 disabled:text-gray-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#888888] hover:text-[#032147] disabled:opacity-50 transition-colors"
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-4.803m5.596-3.856a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border-l-4 border-red-500 rounded">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2.5 px-4 bg-[#753991] hover:bg-[#5a2a6d] text-white font-medium rounded-lg transition-all disabled:bg-gray-400 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
            >
              {isLoading
                ? (mode === 'login' ? 'Signing in...' : 'Creating account...')
                : (mode === 'login' ? 'Sign In' : 'Create Account')}
            </button>

            <button
              type="button"
              onClick={() => {
                setMode(mode === 'login' ? 'signup' : 'login');
                setError('');
                setUsername(mode === 'login' ? '' : 'user');
                setPassword(mode === 'login' ? '' : 'password');
              }}
              disabled={isLoading}
              className="w-full py-2 text-sm font-medium text-[#209dd7] hover:text-[#032147] disabled:text-[#888888] transition-colors"
            >
              {mode === 'login' ? 'Create a test account' : 'Already have an account? Sign in'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
