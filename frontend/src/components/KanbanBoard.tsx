"use client";

import { useEffect, useMemo, useState } from "react";
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
  type DragEndEvent,
  type DragStartEvent,
} from "@dnd-kit/core";
import { KanbanColumn } from "@/components/KanbanColumn";
import { KanbanCardPreview } from "@/components/KanbanCardPreview";
import { createId, initialData, moveCard, type BoardData, type Column, type Card } from "@/lib/kanban";
import { useAuth } from "@/lib/auth-context";
import {
  apiGetBoard,
  apiAddCard,
  apiMoveCard,
  apiDeleteCard,
  apiRenameColumn,
  type Column as ApiColumn,
  type Card as ApiCard,
} from "@/lib/api";

export const KanbanBoard = () => {
  const [board, setBoard] = useState<BoardData>(() => initialData);
  const [activeCardId, setActiveCardId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { username, logout, sessionId } = useAuth();

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: { distance: 6 },
    })
  );

  // Load board from API on mount
  useEffect(() => {
    const loadBoard = async () => {
      if (!sessionId) {
        setError("Not authenticated");
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const apiBoard = await apiGetBoard(sessionId);
        
        // Convert API board format to local board format
        const cardsRecord: Record<string, Card> = {};
        const columns: Column[] = apiBoard.columns.map((col: ApiColumn) => {
          const cardIds: string[] = [];
          col.cards.forEach((card: ApiCard) => {
            const cardId = card.id.toString();
            cardIds.push(cardId);
            cardsRecord[cardId] = {
              id: cardId,
              title: card.title,
              details: card.details || "",
            };
          });
          return {
            id: col.id.toString(),
            title: col.title,
            cardIds,
          };
        });

        const boardData: BoardData = {
          columns,
          cards: cardsRecord,
        };

        setBoard(boardData);
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Failed to load board";
        setError(msg);
        console.error("Board load error:", err);
      } finally {
        setIsLoading(false);
      }
    };

    loadBoard();
  }, [sessionId]);

  const cardsById = useMemo(() => board.cards, [board.cards]);

  const handleDragStart = (event: DragStartEvent) => {
    setActiveCardId(event.active.id as string);
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveCardId(null);

    if (!over || active.id === over.id || !sessionId) {
      return;
    }

    // Use moveCard to update the local state optimistically
    const newColumns = moveCard(board.columns, active.id as string, over.id as string);

    setBoard((prev) => ({
      ...prev,
      columns: newColumns,
    }));

    // Find the target column and position for the API call
    const activeColumn = newColumns.find((col) =>
      col.cardIds.includes(active.id as string)
    );
    const cardId = parseInt(active.id as string);
    const targetColumnId = activeColumn ? parseInt(activeColumn.id) : 0;
    const position = activeColumn?.cardIds.indexOf(active.id as string) ?? 0;

    // Call API to persist change
    try {
      await apiMoveCard(sessionId, cardId, targetColumnId, position);
    } catch (err) {
      setError("Failed to move card");
      console.error("Move card error:", err);
      // Reload board on error
      try {
        const apiBoard = await apiGetBoard(sessionId);
        const cardsRecord: Record<string, Card> = {};
        const columns: Column[] = apiBoard.columns.map((col: ApiColumn) => {
          const cardIds: string[] = [];
          col.cards.forEach((card: ApiCard) => {
            const cardId = card.id.toString();
            cardIds.push(cardId);
            cardsRecord[cardId] = {
              id: cardId,
              title: card.title,
              details: card.details || "",
            };
          });
          return {
            id: col.id.toString(),
            title: col.title,
            cardIds,
          };
        });

        const boardData: BoardData = {
          columns,
          cards: cardsRecord,
        };
        setBoard(boardData);
      } catch (reloadErr) {
        console.error("Failed to reload board:", reloadErr);
      }
    }
  };

  const handleRenameColumn = async (columnId: string, title: string) => {
    if (!sessionId) return;

    // Optimistic update
    setBoard((prev) => ({
      ...prev,
      columns: prev.columns.map((column) =>
        column.id === columnId ? { ...column, title } : column
      ),
    }));

    try {
      await apiRenameColumn(sessionId, parseInt(columnId), title);
    } catch (err) {
      setError("Failed to rename column");
      console.error("Rename column error:", err);
    }
  };

  const handleAddCard = async (columnId: string, title: string, details: string) => {
    if (!sessionId) return;

    const tempId = createId("card");

    // Optimistic update
    setBoard((prev) => ({
      ...prev,
      columns: prev.columns.map((column) =>
        column.id === columnId
          ? { ...column, cardIds: [...column.cardIds, tempId] }
          : column
      ),
      cards: {
        ...prev.cards,
        [tempId]: { id: tempId, title, details },
      },
    }));

    try {
      const newCard = await apiAddCard(sessionId, parseInt(columnId), title, details);
      const newCardId = newCard.id.toString();

      // Replace temp card with real card from API
      setBoard((prev) => ({
        ...prev,
        columns: prev.columns.map((column) =>
          column.id === columnId
            ? {
                ...column,
                cardIds: column.cardIds.map((id) => (id === tempId ? newCardId : id)),
              }
            : column
        ),
        cards: Object.fromEntries(
          Object.entries(prev.cards).map(([id, card]) =>
            id === tempId
              ? [
                  newCardId,
                  {
                    id: newCardId,
                    title: newCard.title,
                    details: newCard.details || "",
                  },
                ]
              : [id, card]
          )
        ),
      }));
    } catch (err) {
      // Revert optimistic update on error
      setBoard((prev) => ({
        ...prev,
        columns: prev.columns.map((column) =>
          column.id === columnId
            ? { ...column, cardIds: column.cardIds.filter((id) => id !== tempId) }
            : column
        ),
        cards: Object.fromEntries(
          Object.entries(prev.cards).filter(([id]) => id !== tempId)
        ),
      }));
      setError("Failed to add card");
      console.error("Add card error:", err);
    }
  };

  const handleDeleteCard = async (columnId: string, cardId: string) => {
    if (!sessionId) return;

    // Optimistic update
    setBoard((prev) => ({
      ...prev,
      columns: prev.columns.map((column) =>
        column.id === columnId
          ? { ...column, cardIds: column.cardIds.filter((id) => id !== cardId) }
          : column
      ),
      cards: Object.fromEntries(
        Object.entries(prev.cards).filter(([id]) => id !== cardId)
      ),
    }));

    try {
      await apiDeleteCard(sessionId, parseInt(cardId));
    } catch (err) {
      setError("Failed to delete card");
      console.error("Delete card error:", err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="mb-4 w-16 h-16 border-4 border-[#209dd7] border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-[#888888]">Loading board...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center max-w-md">
          <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <p className="text-red-700 font-medium">Error</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-[#753991] text-white rounded-lg hover:bg-[#5a2a6d] transition-colors"
          >
            Reload
          </button>
        </div>
      </div>
    );
  }

  const activeCard = activeCardId ? cardsById[activeCardId] : null;

  return (
    <div className="relative overflow-hidden">
      <div className="pointer-events-none absolute left-0 top-0 h-[420px] w-[420px] -translate-x-1/3 -translate-y-1/3 rounded-full bg-[radial-gradient(circle,_rgba(32,157,215,0.25)_0%,_rgba(32,157,215,0.05)_55%,_transparent_70%)]" />
      <div className="pointer-events-none absolute bottom-0 right-0 h-[520px] w-[520px] translate-x-1/4 translate-y-1/4 rounded-full bg-[radial-gradient(circle,_rgba(117,57,145,0.18)_0%,_rgba(117,57,145,0.05)_55%,_transparent_75%)]" />

      <main className="relative mx-auto flex min-h-screen max-w-[1500px] flex-col gap-10 px-4 sm:px-6 pb-16 pt-12">
        <header className="flex flex-col gap-6 rounded-[32px] border border-[var(--stroke)] bg-white/80 p-8 shadow-[var(--shadow)] backdrop-blur">
          <div className="flex flex-wrap md:flex-nowrap items-start justify-between gap-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.35em] text-[var(--gray-text)]">
                Single Board Kanban
              </p>
              <h1 className="mt-3 font-display text-4xl font-semibold text-[var(--navy-dark)]">
                Kanban Studio
              </h1>
              <p className="mt-3 max-w-xl text-sm leading-6 text-[var(--gray-text)]">
                Keep momentum visible. Rename columns, drag cards between stages,
                and capture quick notes without getting buried in settings.
              </p>
            </div>
            <div className="flex flex-col gap-4">
              <div className="rounded-2xl border border-[var(--stroke)] bg-[var(--surface)] px-5 py-4">
                <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--gray-text)]">
                  Focus
                </p>
                <p className="mt-2 text-lg font-semibold text-[var(--primary-blue)]">
                  One board. Five columns. Zero clutter.
                </p>
              </div>
              <div className="flex items-center justify-between rounded-2xl border border-[var(--stroke)] bg-[var(--surface)] px-5 py-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--gray-text)]">
                    Signed in as
                  </p>
                  <p className="mt-1 font-medium text-[var(--navy-dark)]">{username}</p>
                </div>
                <button
                  onClick={logout}
                  className="ml-4 rounded-lg bg-[#753991] px-4 py-2 text-sm font-medium text-white hover:bg-[#5a2a6d] transition-colors"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            {board.columns.map((column) => (
              <div
                key={column.id}
                className="flex items-center gap-2 rounded-full border border-[var(--stroke)] px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-[var(--navy-dark)]"
              >
                <span className="h-2 w-2 rounded-full bg-[var(--accent-yellow)]" />
                {column.title}
              </div>
            ))}
          </div>
        </header>

        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <section className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 auto-rows-min">
            {board.columns.map((column) => (
              <KanbanColumn
                key={column.id}
                column={column}
                cards={column.cardIds.map((cardId) => board.cards[cardId])}
                onRename={handleRenameColumn}
                onAddCard={handleAddCard}
                onDeleteCard={handleDeleteCard}
              />
            ))}
          </section>
          <DragOverlay>
            {activeCard ? (
              <div className="w-[220px] sm:w-[260px] md:w-[300px]">
                <KanbanCardPreview card={activeCard} />
              </div>
            ) : null}
          </DragOverlay>
        </DndContext>
      </main>
    </div>
  );
};
