'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiLogin, apiLogout, apiSignup } from './api';

export interface AuthState {
  isAuthenticated: boolean;
  username: string | null;
  sessionId: string | null;
  showOnboarding: boolean;
}

interface AuthContextType extends AuthState {
  login: (username: string, password: string) => Promise<boolean>;
  signup: (username: string, password: string) => Promise<boolean>;
  completeOnboarding: () => void;
  logout: () => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Store session in localStorage
const SESSION_KEY = 'pm_session';
const USERNAME_KEY = 'pm_username';
const ONBOARDING_KEY = 'pm_show_onboarding';

function saveSession(sessionId: string, username: string, showOnboarding = false) {
  localStorage.setItem(SESSION_KEY, sessionId);
  localStorage.setItem(USERNAME_KEY, username);
  localStorage.setItem(ONBOARDING_KEY, showOnboarding ? 'true' : 'false');
}

function loadSession(): AuthState {
  const sessionId = localStorage.getItem(SESSION_KEY);
  const username = localStorage.getItem(USERNAME_KEY);
  const showOnboarding = localStorage.getItem(ONBOARDING_KEY) === 'true';
  
  if (sessionId && username) {
    return { isAuthenticated: true, username, sessionId, showOnboarding };
  }
  
  return { isAuthenticated: false, username: null, sessionId: null, showOnboarding: false };
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem(USERNAME_KEY);
  localStorage.removeItem(ONBOARDING_KEY);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    username: null,
    sessionId: null,
    showOnboarding: false,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Restore session from localStorage on mount
  useEffect(() => {
    const session = loadSession();
    setAuthState(session);
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    setError(null);
    setIsLoading(true);
    
    try {
      const response = await apiLogin(username, password);
      saveSession(response.session_id, response.username);
      setAuthState({
        isAuthenticated: true,
        username: response.username,
        sessionId: response.session_id,
        showOnboarding: false,
      });
      return true;
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : 'Login failed';
      setError(errorMsg);
      setAuthState({ isAuthenticated: false, username: null, sessionId: null, showOnboarding: false });
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (username: string, password: string): Promise<boolean> => {
    setError(null);
    setIsLoading(true);

    try {
      const response = await apiSignup(username, password);
      saveSession(response.session_id, response.username, true);
      setAuthState({
        isAuthenticated: true,
        username: response.username,
        sessionId: response.session_id,
        showOnboarding: true,
      });
      return true;
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : 'Signup failed';
      setError(errorMsg);
      setAuthState({ isAuthenticated: false, username: null, sessionId: null, showOnboarding: false });
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const completeOnboarding = () => {
    localStorage.setItem(ONBOARDING_KEY, 'false');
    setAuthState((current) => ({ ...current, showOnboarding: false }));
  };

  const logout = async () => {
    try {
      if (authState.sessionId) {
        await apiLogout(authState.sessionId);
      }
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      clearSession();
      setAuthState({ isAuthenticated: false, username: null, sessionId: null, showOnboarding: false });
      setError(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{ ...authState, login, signup, completeOnboarding, logout, isLoading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
