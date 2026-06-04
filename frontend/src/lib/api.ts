/**
 * API Client for Kanban backend
 * Handles all communication with the FastAPI backend
 */

export interface ApiError {
  status: number;
  message: string;
  detail?: string;
}

export interface Board {
  id: number;
  user_id: number;
  title: string;
  created_at: string;
  updated_at: string;
  columns: Column[];
}

export interface Column {
  id: number;
  board_id: number;
  title: string;
  position: number;
  created_at: string;
  updated_at: string;
  cards: Card[];
}

export interface Card {
  id: number;
  column_id: number;
  title: string;
  details?: string;
  position: number;
  priority?: "low" | "medium" | "high";
  due_date?: string | null;
  assignee?: string | null;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  session_id: string;
  username: string;
}

const API_BASE = "/api";

/**
 * Make API request with session handling
 */
async function apiCall<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE" = "GET",
  body?: Record<string, unknown>,
  sessionId?: string
): Promise<T> {
  // Handle both relative and absolute URLs
  const urlString = API_BASE.startsWith("http") 
    ? `${API_BASE}${endpoint}` 
    : `${window.location.origin}${API_BASE}${endpoint}`;
  
  const url = new URL(urlString);

  // Add session_id as query param if provided
  if (sessionId) {
    url.searchParams.set("session_id", sessionId);
  }

  const options: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url.toString(), options);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw {
        status: response.status,
        message: `HTTP ${response.status}`,
        detail: errorData.detail || response.statusText,
      } as ApiError;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      throw {
        status: 0,
        message: "Network error",
        detail: error.message,
      } as ApiError;
    }
    throw error;
  }
}

/**
 * Login with username and password
 */
export async function apiLogin(
  username: string,
  password: string
): Promise<LoginResponse> {
  return apiCall<LoginResponse>("/auth/login", "POST", {
    username,
    password,
  });
}

/**
 * Create a new user account
 */
export async function apiSignup(
  username: string,
  password: string
): Promise<LoginResponse> {
  return apiCall<LoginResponse>("/auth/signup", "POST", {
    username,
    password,
  });
}

/**
 * Logout and clear session
 */
export async function apiLogout(sessionId: string): Promise<void> {
  return apiCall("/auth/logout", "POST", {}, sessionId);
}

/**
 * Get current user's board with all columns and cards
 */
export async function apiGetBoard(sessionId: string): Promise<Board> {
  return apiCall<Board>("/board", "GET", undefined, sessionId);
}

/**
 * Add new card to column
 */
export async function apiAddCard(
  sessionId: string,
  columnId: number,
  title: string,
  details?: string
): Promise<Card> {
  const url = `/board/cards?column_id=${columnId}`;
  return apiCall<Card>(url, "POST", { title, details }, sessionId);
}

/**
 * Move card to new column and position
 */
export async function apiMoveCard(
  sessionId: string,
  cardId: number,
  columnId: number,
  position: number
): Promise<Card> {
  return apiCall<Card>(
    `/board/cards/${cardId}`,
    "PUT",
    { column_id: columnId, position },
    sessionId
  );
}

/**
 * Delete card
 */
export async function apiDeleteCard(
  sessionId: string,
  cardId: number
): Promise<void> {
  return apiCall(`/board/cards/${cardId}`, "DELETE", undefined, sessionId);
}

/**
 * Update card title and details
 */
export async function apiUpdateCard(
  sessionId: string,
  cardId: number,
  title: string,
  details: string
): Promise<Card> {
  return apiCall<Card>(
    `/board/cards/${cardId}`,
    "PATCH",
    { title, details },
    sessionId
  );
}

/**
 * Rename column
 */
export async function apiRenameColumn(
  sessionId: string,
  columnId: number,
  title: string
): Promise<Column> {
  return apiCall<Column>(
    `/board/columns/${columnId}`,
    "POST",
    { title },
    sessionId
  );
}
