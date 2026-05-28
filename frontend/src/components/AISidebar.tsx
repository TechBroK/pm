'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth-context';

function BotAvatar({ size = 20 }: { size?: number }) {
  const s = size;
  return (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
      <rect width="24" height="24" rx="6" fill="var(--primary-blue)" />
      <circle cx="8.5" cy="11" r="1.5" fill="white" />
      <circle cx="15.5" cy="11" r="1.5" fill="white" />
      <rect x="7" y="14" width="10" height="1.6" rx="0.8" fill="white" />
      <rect x="9" y="4" width="6" height="3" rx="1" fill="rgba(255,255,255,0.06)" />
    </svg>
  );
}

export default function AISidebar() {
  const { sessionId, isAuthenticated } = useAuth();
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function askAI() {
    setLoading(true);
    setResponse(null);
    try {
      const params = sessionId ? `?session_id=${sessionId}&question=${encodeURIComponent(question)}` : `?question=${encodeURIComponent(question)}`;
      const res = await fetch(`/api/ai/ask${params}`, {
        method: 'POST',
      });
      const data = await res.json();
      setResponse(data.response || JSON.stringify(data));
    } catch (e) {
      setResponse('Error contacting AI service');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        aria-label="Toggle AI sidebar"
        onClick={() => setOpen(!open)}
        style={{ position: 'fixed', right: 16, bottom: 16, zIndex: 60, padding: '10px 14px', borderRadius: 10, background: 'var(--secondary-purple)', color: 'white', border: 'none', display: 'flex', alignItems: 'center', gap: 8, boxShadow: 'var(--ai-button-shadow)' }}
      >
        <BotAvatar size={20} />
        <span style={{ fontWeight: 600 }}>Ask AI</span>
      </button>

      {open && (
        <div style={{ position: 'fixed', right: 16, bottom: 72, width: 380, maxHeight: '60vh', zIndex: 60, background: 'var(--surface-strong)', border: '1px solid var(--stroke)', borderRadius: 8, boxShadow: 'var(--shadow)', padding: 12, overflow: 'auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
            <BotAvatar size={28} />
            <h3 style={{ margin: 0 }}>Ask AI</h3>
          </div>
          {!isAuthenticated && <div style={{ color: '#666', marginBottom: 8 }}>Sign in to enable session-aware AI features.</div>}
          <textarea placeholder="Ask about your board..." value={question} onChange={(e) => setQuestion(e.target.value)} style={{ width: '100%', minHeight: 88, padding: 8, borderRadius: 6, border: '1px solid var(--stroke)' }} />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button onClick={askAI} disabled={loading || !question} style={{ flex: 1, padding: 8, background: 'var(--primary-blue)', color: 'white', border: 'none', borderRadius: 6 }}>Ask</button>
            <button onClick={() => { setQuestion(''); setResponse(null); }} style={{ padding: 8 }}>Clear</button>
          </div>

          <div style={{ marginTop: 12 }}>
            <strong>Response</strong>
            <div style={{ marginTop: 8, whiteSpace: 'pre-wrap', color: 'var(--navy-dark)' }}>{loading ? 'Thinking...' : response ?? 'No response yet'}</div>
          </div>
        </div>
      )}
    </div>
  );
}
