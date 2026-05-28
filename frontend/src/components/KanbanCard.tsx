import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import clsx from "clsx";
import type { Card } from "@/lib/kanban";

type KanbanCardProps = {
  card: Card;
  onDelete: (cardId: string) => void;
};

export const KanbanCard = ({ card, onDelete }: KanbanCardProps) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } =
    useSortable({ id: card.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <article
      ref={setNodeRef}
      style={style}
      className={clsx(
        "w-full rounded-2xl border border-transparent bg-white px-3 py-3 sm:px-4 sm:py-4 shadow-[0_12px_24px_rgba(3,33,71,0.08)]",
        "transition-all duration-150",
        isDragging && "opacity-60 shadow-[0_18px_32px_rgba(3,33,71,0.16)]"
      )}
      {...attributes}
      {...listeners}
      data-testid={`card-${card.id}`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <h4
            className="font-display text-xs sm:text-base font-semibold text-[var(--navy-dark)]"
            style={{ letterSpacing: "normal", wordBreak: "normal", whiteSpace: "normal" }}
          >
            {card.title}
          </h4>
          <p
            className="mt-2 text-xxs sm:text-sm leading-6 text-[var(--gray-text)]"
            style={{ letterSpacing: "normal", wordBreak: "normal", whiteSpace: "normal" }}
          >
            {card.details}
          </p>
        </div>
        <button
          type="button"
          onClick={() => onDelete(card.id)}
          className="flex-shrink-0 rounded-full border border-transparent px-2 py-1 text-xs font-semibold text-[var(--gray-text)] transition hover:border-[var(--stroke)] hover:text-[var(--navy-dark)]"
          aria-label={`Delete ${card.title}`}
        >
          Remove
        </button>
      </div>
    </article>
  );
};
