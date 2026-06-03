import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import clsx from "clsx";
import type { Card } from "@/lib/kanban";
import { useState } from "react";

type KanbanCardProps = {
  card: Card;
  onDelete: (cardId: string) => void;
  onEdit?: (card: Card) => void;
};

const priorityColors = {
  low: "#209dd7",      // Blue
  medium: "#ecad0a",   // Yellow
  high: "#e74c3c",     // Red
};

const getPriorityBgColor = (priority?: string) => {
  switch (priority) {
    case "high":
      return "bg-red-100 text-red-800";
    case "medium":
      return "bg-yellow-100 text-yellow-800";
    case "low":
      return "bg-blue-100 text-blue-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const isOverdue = (dueDate?: string) => {
  if (!dueDate) return false;
  const due = new Date(dueDate);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  due.setHours(0, 0, 0, 0);
  return due < today;
};

export const KanbanCard = ({ card, onDelete, onEdit }: KanbanCardProps) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: card.id });
  const [showDetails, setShowDetails] = useState(false);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const overdue = isOverdue(card.due_date);

  return (
    <>
      <article
        ref={setNodeRef}
        style={style}
        className={clsx(
          "w-full rounded-2xl border border-transparent bg-white px-3 py-3 sm:px-4 sm:py-4 shadow-[0_12px_24px_rgba(3,33,71,0.08)]",
          "transition-all duration-150 cursor-pointer hover:shadow-[0_16px_32px_rgba(3,33,71,0.12)]",
          isDragging && "opacity-60 shadow-[0_18px_32px_rgba(3,33,71,0.16)]"
        )}
        {...attributes}
        {...listeners}
        data-testid={`card-${card.id}`}
        onClick={() => setShowDetails(!showDetails)}
      >
        <div className="flex items-start gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <h4
                className="font-display text-xs sm:text-base font-semibold text-[var(--navy-dark)]"
                style={{ letterSpacing: "normal", wordBreak: "break-word", whiteSpace: "normal" }}
              >
                {card.title}
              </h4>
              {card.priority && card.priority !== "medium" && (
                <span className={clsx(
                  "inline-block px-2 py-1 text-xs font-semibold rounded-full whitespace-nowrap",
                  getPriorityBgColor(card.priority)
                )}>
                  {card.priority.charAt(0).toUpperCase() + card.priority.slice(1)}
                </span>
              )}
            </div>
            
            {card.details && (
              <p
                className="mt-2 text-xxs sm:text-sm leading-6 text-[var(--gray-text)]"
                style={{ letterSpacing: "normal", wordBreak: "break-word", whiteSpace: "normal" }}
              >
                {card.details}
              </p>
            )}

            {/* Card metadata row */}
            <div className="mt-3 flex items-center gap-3 flex-wrap">
              {card.due_date && (
                <span className={clsx(
                  "text-xs font-medium",
                  overdue ? "text-red-600" : "text-[var(--gray-text)]"
                )}>
                  📅 {new Date(card.due_date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
                  {overdue && " ⚠️ Overdue"}
                </span>
              )}
              {card.assignee && (
                <span className="text-xs font-medium text-[#209dd7]">
                  👤 {card.assignee}
                </span>
              )}
            </div>
          </div>

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(card.id);
            }}
            className="flex-shrink-0 rounded-full border border-transparent px-2 py-1 text-xs font-semibold text-[var(--gray-text)] transition hover:border-[var(--stroke)] hover:text-[var(--navy-dark)]"
            aria-label={`Delete ${card.title}`}
          >
            Remove
          </button>
        </div>
      </article>

      {/* Card details popup (optional for MVP) */}
      {showDetails && (
        <div className="mt-2 text-xs text-[var(--gray-text)]">
          <p>Click card to edit details</p>
        </div>
      )}
    </>
  );
};
