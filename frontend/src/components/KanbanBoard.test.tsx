import { render, screen, within, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, beforeEach, afterEach } from "vitest";
import { KanbanBoard } from "@/components/KanbanBoard";
import * as api from "@/lib/api";

const mockLogout = vi.fn();

vi.mock("@/lib/auth-context", () => ({
  useAuth: () => ({
    username: "testuser",
    sessionId: "test-session-id",
    logout: mockLogout,
  }),
}));

// Mock API module
vi.mock("@/lib/api", () => ({
  apiGetBoard: vi.fn(),
  apiAddCard: vi.fn(),
  apiMoveCard: vi.fn(),
  apiDeleteCard: vi.fn(),
  apiRenameColumn: vi.fn(),
}));

const mockBoardData = {
  id: 1,
  title: "Test Board",
  columns: [
    {
      id: 1,
      title: "Backlog",
      position: 0,
      cards: [
        { id: 1, title: "Card 1", details: "Details 1", position: 0, column_id: 1 },
      ],
    },
    {
      id: 2,
      title: "Discovery",
      position: 1,
      cards: [],
    },
    {
      id: 3,
      title: "In Progress",
      position: 2,
      cards: [],
    },
    {
      id: 4,
      title: "Review",
      position: 3,
      cards: [],
    },
    {
      id: 5,
      title: "Done",
      position: 4,
      cards: [],
    },
  ],
};

const getFirstColumn = () => screen.getAllByTestId(/column-/i)[0];

const renderWithAuth = (component: React.ReactElement) => {
  return render(component);
};

beforeEach(() => {
  vi.clearAllMocks();
  localStorage.clear();
  mockLogout.mockResolvedValue(undefined);
  (api.apiGetBoard as any).mockResolvedValue(mockBoardData);
  (api.apiAddCard as any).mockResolvedValue({
    id: 999,
    title: "New card",
    details: "Notes",
  });
  (api.apiMoveCard as any).mockResolvedValue(undefined);
  (api.apiDeleteCard as any).mockResolvedValue(undefined);
  (api.apiRenameColumn as any).mockResolvedValue(undefined);
});

afterEach(() => {
  localStorage.clear();
});

describe("KanbanBoard", () => {
  it("renders five columns", async () => {
    renderWithAuth(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });
  });

  it("renames a column", async () => {
    renderWithAuth(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });
    const column = getFirstColumn();
    const input = within(column).getByLabelText(/edit backlog column title/i);
    await userEvent.clear(input);
    await userEvent.type(input, "New Name");
    expect(input).toHaveValue("New Name");
  });

  it("adds and removes a card", async () => {
    renderWithAuth(<KanbanBoard />);
    await waitFor(() => {
      expect(screen.getAllByTestId(/column-/i)).toHaveLength(5);
    });
    const column = getFirstColumn();
    const addButton = within(column).getByRole("button", {
      name: /add a card/i,
    });
    await userEvent.click(addButton);

    const titleInput = within(column).getByPlaceholderText(/card title/i);
    await userEvent.type(titleInput, "New card");
    const detailsInput = within(column).getByPlaceholderText(/details/i);
    await userEvent.type(detailsInput, "Notes");

    const submitButton = within(column).getByRole("button", { name: /add card/i });
    await userEvent.click(submitButton);

    // Wait for optimistic update and API response
    await waitFor(
      () => {
        expect(within(column).getByText("New card")).toBeInTheDocument();
      },
      { timeout: 3000 }
    );

    // Find the delete button for the new card
    const cards = within(column).getAllByTestId(/card-/);
    const lastCard = cards[cards.length - 1];
    const deleteButton = within(lastCard).getByRole("button", {
      name: /delete/i,
    });
    await userEvent.click(deleteButton);

    await waitFor(() => {
      expect(within(column).queryByText("New card")).not.toBeInTheDocument();
    });
  });
});
