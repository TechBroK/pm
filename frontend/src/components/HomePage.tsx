'use client';

import { useState } from 'react';
import LoginPage from './LoginPage';

export default function HomePage() {
  const [mode, setMode] = useState<'login' | 'signup' | null>(null);

  if (mode) {
    return <LoginPage initialMode={mode} />;
  }

  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,#f7f8fb_0%,#ffffff_48%,#eef6fb_100%)] text-[#032147]">
      <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-center px-4 py-10 md:px-6 md:py-12">
        <div className="mb-3 h-1 w-20 rounded-full bg-[#ecad0a]" />
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#209dd7]">
          Kanban Studio
        </p>
        <h1 className="mt-3 max-w-3xl font-display text-4xl font-bold leading-tight md:text-5xl">
          Organize the work first, then sign in to open your board.
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-7 text-[#666666]">
          Plan tasks, move cards through your workflow, and keep everything local in one app. Sign in when you’re ready to load your board from the database.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => setMode('login')}
            className="rounded-lg bg-[#753991] px-5 py-2.5 text-sm font-semibold text-white shadow-md transition hover:bg-[#5a2a6d]"
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => setMode('signup')}
            className="rounded-lg border border-(--stroke) bg-white px-5 py-2.5 text-sm font-semibold text-[#032147] transition hover:border-[#209dd7] hover:text-[#209dd7]"
          >
            Create Account
          </button>
          <a
            href="#details"
            className="rounded-lg border border-(--stroke) bg-white px-5 py-2.5 text-sm font-semibold text-[#032147] transition hover:border-[#209dd7] hover:text-[#209dd7]"
          >
            Learn More
          </a>
        </div>

        <div id="details" className="mt-10 grid gap-3 md:grid-cols-3">
          {[
            'One board per user keeps the workspace focused.',
            'Cards and columns are loaded from the database after login.',
            'The board is ready for drag-and-drop work management.',
          ].map((item) => (
            <div key={item} className="rounded-2xl border border-(--stroke) bg-white p-4 shadow-sm">
              <p className="text-sm leading-6 text-[#032147]">{item}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}