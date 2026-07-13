'use client';

import React, { useEffect, useState } from 'react';

export default function ThemeToggle() {
  // Don't read localStorage during initial render to avoid hydration mismatches.
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    try {
      const t = localStorage.getItem('pm_theme') as 'light' | 'dark' | null;
      if (t) setTheme(t);
    } catch {}
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
    try {
      localStorage.setItem('pm_theme', theme);
    } catch {}
  }, [theme, mounted]);

  return (
    <button
      aria-label="Toggle theme"
      onClick={() => setTheme((t) => (t === 'light' ? 'dark' : 'light'))}
      style={{ position: 'fixed', right: 12, top: 12, zIndex: 70, padding: 6, borderRadius: 8, background: 'transparent', border: '1px solid var(--stroke)', display: 'flex', alignItems: 'center', gap: 6 }}
    >
      <span style={{ fontSize: 14 }}>{mounted ? (theme === 'dark' ? '🌙' : '☀️') : '●'}</span>
      <span style={{ fontSize: 12, color: 'var(--gray-text)' }}>{mounted ? (theme === 'dark' ? 'Dark' : 'Light') : ''}</span>
    </button>
  );
}
