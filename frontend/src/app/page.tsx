"use client";

import HomePage from "@/components/HomePage";
import { KanbanBoard } from "@/components/KanbanBoard";
import OnboardingPage from "@/components/OnboardingPage";
import { useAuth } from "@/lib/auth-context";

export default function Home() {
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
    return <HomePage />;
  }

  if (showOnboarding) {
    return <OnboardingPage />;
  }

  return (
    <KanbanBoard />
  );
}
