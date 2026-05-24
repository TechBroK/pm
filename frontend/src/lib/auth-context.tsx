'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authenticate, saveAuthSession, getAuthSession, clearAuthSession, type AuthState } from './auth';

interface AuthContextType extends AuthState {
  login: (username: string, password: string) => boolean;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({ isAuthenticated: false, username: null });
  const [isLoading, setIsLoading] = useState(true);

  // Restore session from localStorage on mount
  useEffect(() => {
    const session = getAuthSession();
    setAuthState(session);
    setIsLoading(false);
  }, []);

  const login = (username: string, password: string): boolean => {
    if (authenticate(username, password)) {
      saveAuthSession(username);
      setAuthState({ isAuthenticated: true, username });
      return true;
    }
    return false;
  };

  const logout = () => {
    clearAuthSession();
    setAuthState({ isAuthenticated: false, username: null });
  };

  return (
    <AuthContext.Provider value={{ ...authState, login, logout, isLoading }}>
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
