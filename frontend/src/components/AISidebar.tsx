'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth-context';

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
      const params = sessionId ? `?session_id=${sessionId}&question=${encodeURIComponent(question)}` : '';
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
        style={{ position: 'fixed', right: 16, bottom: 16, zIndex: 60, padding: 12, borderRadius: 8, background: '#753991', color: 'white', border: 'none' }}
      >
        AI
      </button>

      {open && (
        <div style={{ position: 'fixed', right: 16, bottom: 72, width: 360, maxHeight: '60vh', zIndex: 60, background: 'white', border: '1px solid #e6e6e6', borderRadius: 8, boxShadow: '0 6px 24px rgba(0,0,0,0.12)', padding: 12, overflow: 'auto' }}>
          <h3 style={{ margin: 0, marginBottom: 8 }}>AI Assistant</h3>
          {!isAuthenticated && <div style={{ color: '#666', marginBottom: 8 }}>Sign in to enable session-aware AI features.</div>}
          <textarea placeholder="Ask about your board..." value={question} onChange={(e) => setQuestion(e.target.value)} style={{ width: '100%', minHeight: 80 }} />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button onClick={askAI} disabled={loading || !question} style={{ flex: 1, padding: 8, background: '#209dd7', color: 'white', border: 'none', borderRadius: 6 }}>Ask</button>
            <button onClick={() => { setQuestion(''); setResponse(null); }} style={{ padding: 8 }}>Clear</button>
          </div>

          <div style={{ marginTop: 12 }}>
            <strong>Response</strong>
            <div style={{ marginTop: 8, whiteSpace: 'pre-wrap', color: '#222' }}>{loading ? 'Thinking...' : response ?? 'No response yet'}</div>
          </div>
        </div>
      )}
    </div>
  );
}
