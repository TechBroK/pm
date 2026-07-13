'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
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

function onboardingKey(username: string) {
  return `pm_onboarding_complete_${username}`;
}

function readOnboardingComplete(username: string) {
  try {
    return localStorage.getItem(onboardingKey(username)) === 'true';
  } catch {
    return true;
  }
}

function writeOnboardingComplete(username: string, complete: boolean) {
  try {
    localStorage.setItem(onboardingKey(username), complete ? 'true' : 'false');
  } catch {}
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    username: null,
    sessionId: null,
    showOnboarding: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (username: string, password: string): Promise<boolean> => {
    setError(null);
    setIsLoading(true);
    
    try {
      const response = await apiLogin(username, password);
      setAuthState({
        isAuthenticated: true,
        username: response.username,
        sessionId: response.session_id,
        showOnboarding: !readOnboardingComplete(response.username),
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
      setAuthState({
        isAuthenticated: true,
        username: response.username,
        sessionId: response.session_id,
        showOnboarding: true,
      });
      writeOnboardingComplete(response.username, false);
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
    if (authState.username) {
      writeOnboardingComplete(authState.username, true);
    }
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
