'use client';

import { useAuth } from '@/lib/auth-context';

const workflowSteps = [
  {
    title: 'Capture work',
    body: 'Add cards for tasks, ideas, bugs, research notes, and anything else your project needs to track.',
  },
  {
    title: 'Move through stages',
    body: 'Drag cards across Backlog, Discovery, In Progress, Review, and Done as the work changes state.',
  },
  {
    title: 'Keep the board familiar',
    body: 'Rename columns like Discovery, Review, or Done so the workflow matches the language your team already uses.',
  },
  {
    title: 'Refine card details',
    body: 'Edit any card after creating it. Update the title or details as the work becomes clearer.',
  },
  {
    title: 'Ask the AI sidebar',
    body: 'Use the assistant to discuss the board and prepare card updates while you plan.',
  },
];

const implementationNotes = [
  'The frontend is built with Next.js, React, TypeScript, Tailwind CSS, and dnd-kit.',
  'The backend is a FastAPI app that serves both the API and the built static frontend.',
  'SQLite stores users, boards, columns, cards, and activity data locally.',
  'Each new account receives one board with five default columns.',
  'OpenRouter powers the AI service when an API key is configured; local mock responses are used otherwise.',
];

export default function OnboardingPage() {
  const { username, completeOnboarding, logout } = useAuth();

  return (
    <main className="min-h-screen bg-[var(--surface)] text-[var(--navy-dark)]">
      <section className="border-b border-[var(--stroke)] bg-white">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-5 py-10 md:flex-row md:items-center md:justify-between md:px-8">
          <div className="max-w-3xl">
            <div className="mb-4 h-1 w-24 rounded-full bg-[#ecad0a]" />
            <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-[#209dd7]">
              Welcome{username ? `, ${username}` : ''}
            </p>
            <h1 className="font-display text-4xl font-bold leading-tight text-[#032147] md:text-5xl">
              Learn the workspace before opening your board
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-[#666666]">
              Kanban Studio is a focused project management app for planning work, tracking progress, and keeping project details in one local board.
            </p>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row md:flex-col">
            <button
              type="button"
              onClick={completeOnboarding}
              className="rounded-lg bg-[#753991] px-5 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-[#5a2a6d]"
            >
              Open My Board
            </button>
            <button
              type="button"
              onClick={logout}
              className="rounded-lg border border-[var(--stroke)] bg-white px-5 py-3 text-sm font-semibold text-[#032147] transition hover:border-[#209dd7] hover:text-[#209dd7]"
            >
              Sign Out
            </button>
          </div>
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-5 py-8 md:px-8">
        <div className="grid gap-4 md:grid-cols-5">
          {workflowSteps.map((step, index) => (
            <article
              key={step.title}
              className="rounded-lg border border-[var(--stroke)] bg-white p-5 shadow-sm"
            >
              <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-full bg-[#209dd7] text-sm font-bold text-white">
                {index + 1}
              </div>
              <h2 className="text-lg font-bold text-[#032147]">{step.title}</h2>
              <p className="mt-2 text-sm leading-6 text-[#666666]">{step.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="border-y border-[var(--stroke)] bg-white">
        <div className="mx-auto grid w-full max-w-6xl gap-8 px-5 py-10 md:grid-cols-[1fr_1.1fr] md:px-8">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-[#209dd7]">How to use it</p>
            <h2 className="mt-2 text-3xl font-bold text-[#032147]">Your daily project flow</h2>
            <p className="mt-4 text-sm leading-6 text-[#666666]">
              Start by adding cards to Backlog. Pull the clearest work into Discovery, then move it into active delivery. Use Review to check quality before marking work Done.
            </p>
          </div>
          <div className="grid gap-3">
            {[
              'Create one card per task so progress is easy to scan.',
              'Edit card titles and details whenever scope, notes, or next steps change.',
              'Rename columns like Discovery or Done directly from the column header.',
              'Use card details for context, acceptance notes, blockers, or next steps.',
              'Keep column names short so the board remains readable.',
              'Move cards often; the board is most useful when it reflects reality.',
            ].map((item) => (
              <div key={item} className="border-l-4 border-[#ecad0a] bg-[#f7f8fb] px-4 py-3 text-sm text-[#032147]">
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-8 px-5 py-10 md:grid-cols-[1fr_1.1fr] md:px-8">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-[#209dd7]">Implementation</p>
          <h2 className="mt-2 text-3xl font-bold text-[#032147]">What is running behind the app</h2>
          <p className="mt-4 text-sm leading-6 text-[#666666]">
            The MVP keeps the architecture simple: a static Next.js app, a FastAPI API, and a local SQLite database packaged for local Docker use.
          </p>
        </div>
        <ul className="grid gap-3">
          {implementationNotes.map((note) => (
            <li key={note} className="rounded-lg border border-[var(--stroke)] bg-white px-4 py-3 text-sm leading-6 text-[#032147] shadow-sm">
              {note}
            </li>
          ))}
        </ul>
      </section>

      <section className="bg-[#032147]">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-5 py-8 md:flex-row md:items-center md:justify-between md:px-8">
          <div>
            <h2 className="text-2xl font-bold text-white">Ready to plan your project?</h2>
            <p className="mt-2 text-sm leading-6 text-[#d8e3f2]">
              Open your board, add a first card, and move it as the work progresses.
            </p>
          </div>
          <button
            type="button"
            onClick={completeOnboarding}
            className="rounded-lg bg-[#ecad0a] px-5 py-3 text-sm font-bold text-[#032147] shadow-md transition hover:bg-[#d19a08]"
          >
            Start Using Kanban Studio
          </button>
        </div>
      </section>
    </main>
  );
}
