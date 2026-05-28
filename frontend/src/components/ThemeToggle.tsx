'use client';

import React, { useEffect, useState } from 'react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    try {
      const t = localStorage.getItem('pm_theme');
      return (t as 'light' | 'dark') || 'light';
    } catch {
      return 'light';
    }
  });

  useEffect(() => {
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
    try {
      localStorage.setItem('pm_theme', theme);
    } catch {}
  }, [theme]);

  return (
    <button
      aria-label="Toggle theme"
      onClick={() => setTheme((t) => (t === 'light' ? 'dark' : 'light'))}
      style={{ position: 'fixed', right: 16, top: 16, zIndex: 70, padding: 8, borderRadius: 8, background: 'transparent', border: '1px solid var(--stroke)', display: 'flex', alignItems: 'center', gap: 8 }}
    >
      <span style={{ fontSize: 14 }}>{theme === 'dark' ? '🌙' : '☀️'}</span>
      <span style={{ fontSize: 13, color: 'var(--gray-text)' }}>{theme === 'dark' ? 'Dark' : 'Light'}</span>
    </button>
  );
}
