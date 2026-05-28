'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth-context';

function BotAvatar({ size = 20 }: { size?: number }) {
  const s = size;
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: s, height: s, borderRadius: s, background: 'var(--primary-blue)', color: 'white', fontSize: Math.max(12, s - 6) }}>
      🤖
    </span>
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
        style={{ position: 'fixed', right: 16, bottom: 16, zIndex: 60, padding: '10px 14px', borderRadius: 10, background: 'var(--secondary-purple)', color: 'white', border: 'none', display: 'flex', alignItems: 'center', gap: 8 }}
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
