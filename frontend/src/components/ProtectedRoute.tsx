'use client';

import { ReactNode } from 'react';
import { useAuth } from '@/lib/auth-context';
import LoginPage from './LoginPage';
import OnboardingPage from './OnboardingPage';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, showOnboarding } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-primary mx-auto mb-4"></div>
          <p className="text-gray-text">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  if (showOnboarding) {
    return <OnboardingPage />;
  }

  return <>{children}</>;
}
