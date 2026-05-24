/**
 * Authentication utilities
 * Handles hardcoded user authentication with localStorage persistence
 */

export interface AuthState {
  isAuthenticated: boolean;
  username: string | null;
}

const STORAGE_KEY = 'pm_auth';
const VALID_USERNAME = 'user';
const VALID_PASSWORD = 'password';

export function authenticate(username: string, password: string): boolean {
  return username === VALID_USERNAME && password === VALID_PASSWORD;
}

export function saveAuthSession(username: string): void {
  const authData = { username, timestamp: Date.now() };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(authData));
}

export function getAuthSession(): AuthState {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try {
      const data = JSON.parse(stored);
      return {
        isAuthenticated: true,
        username: data.username,
      };
    } catch {
      clearAuthSession();
      return { isAuthenticated: false, username: null };
    }
  }
  return { isAuthenticated: false, username: null };
}

export function clearAuthSession(): void {
  localStorage.removeItem(STORAGE_KEY);
}
