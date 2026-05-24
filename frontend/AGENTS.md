# Frontend Architecture Documentation

## Overview

The PM frontend is a Next.js 16 application built with React 19 and TypeScript. It implements a drag-and-drop Kanban board with support for card management (create, edit, delete). The current implementation uses local state management and does not connect to a backend.

## Project Structure

```
frontend/
├── src/
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── lib/              # Utility functions and logic
│   └── test/             # Test setup files
├── tests/                # E2E tests (Playwright)
├── public/               # Static assets
└── [config files]        # TypeScript, ESLint, Next.js configs
```

## Key Dependencies

- **Next.js 16.1.6**: Framework and build tooling
- **React 19.2.3 & React DOM 19.2.3**: UI rendering
- **@dnd-kit 6.3.1+**: Drag-and-drop functionality (pointerSensor, sortable utilities)
- **Tailwind CSS 4**: Styling framework
- **TypeScript 5**: Static typing
- **Vitest 3.2.4**: Unit testing framework
- **@testing-library/react 16.3.2**: Component testing utilities
- **@testing-library/user-event 14.6.1**: User interaction simulation
- **Playwright 1.58.0**: E2E testing
- **ESLint 9**: Code linting

## Components

### KanbanBoard (`src/components/KanbanBoard.tsx`)

**Responsibility**: Main board container and state management

**Features**:

- Manages board state: columns and cards
- Handles drag-and-drop via `@dnd-kit/core`
- Initializes with sample data from `initialData`
- Renders columns and cards
- Manages card lifecycle (add, delete, rename column)
- Implements optimistic updates for UI responsiveness

**State**:

- `board: BoardData` - Current board state (columns and cards)
- `activeCardId: string | null` - Card being dragged

**Key Methods**:

- `handleDragStart()` - Track active card during drag
- `handleDragEnd()` - Apply card movement logic
- `handleRenameColumn()` - Update column title
- `handleAddCard()` - Create new card
- `handleDeleteCard()` - Remove card from board

**Props**: None (uses local state)

**Tests**: [KanbanBoard.test.tsx](src/components/KanbanBoard.test.tsx)

- Renders 5 columns
- Renames columns
- Adds and deletes cards

---

### KanbanColumn (`src/components/KanbanColumn.tsx`)

**Responsibility**: Renders a single column with cards and controls

**Features**:

- Displays column title with editable input
- Shows all cards in the column
- Provides "Add Card" button
- Receives drag-drop events
- Highlights when card is being dragged over

**Props**:

- `column: Column` - Column data
- `cards: Record<string, Card>` - All cards (referenced by ID)
- `onRenameColumn(title: string)` - Callback to rename column
- `onAddCard(title: string, details: string)` - Callback to create card
- `onDeleteCard(cardId: string)` - Callback to delete card
- `isOverColumn: boolean` - Visual feedback during drag over

**State**: None (fully controlled by parent)

**Typical Structure**: Title input, card list, add card form

---

### KanbanCard (`src/components/KanbanCard.tsx`)

**Responsibility**: Renders a single draggable card

**Features**:

- Displays card title and details
- Provides delete button
- Supports drag-and-drop
- Shows active state during drag

**Props**:

- `card: Card` - Card data
- `isActive: boolean` - Whether currently being dragged
- `onDelete()` - Callback to delete card

**State**: None (fully controlled)

---

### KanbanCardPreview (`src/components/KanbanCardPreview.tsx`)

**Responsibility**: Visual preview of card during drag operations

**Features**:

- Displays card content in a "ghost" style
- Shown during drag overlay

**Props**:

- `card: Card | null` - Card being dragged

**Usage**: Used with `DragOverlay` from `@dnd-kit/core`

---

### NewCardForm (`src/components/NewCardForm.tsx`)

**Responsibility**: Form for creating new cards

**Features**:

- Title input field (required)
- Details textarea (optional)
- Submit button
- Cancel button
- Form validation

**Props**:

- `onSubmit(title: string, details: string)` - Callback on form submit
- `onCancel()` - Callback to close form

**State**: Form input values (title, details)

---

## Utilities & Types

### kanban.ts (`src/lib/kanban.ts`)

**Purpose**: Business logic for Kanban operations

**Types**:

```typescript
type Card = {
  id: string;
  title: string;
  details: string;
};

type Column = {
  id: string;
  title: string;
  cardIds: string[];
};

type BoardData = {
  columns: Column[];
  cards: Record<string, Card>; // For O(1) card lookups
};
```

**Key Functions**:

- **`initialData: BoardData`**: Sample board with 5 columns and 8 cards (hardcoded for MVP)

- **`moveCard(columns: Column[], activeId: string, overId: string): Column[]`**
  - Moves a card from one position to another
  - Supports reordering within same column
  - Supports moving between columns
  - Handles drag-over-column case (appends to end)
  - Returns new column array (immutable)

- **`createId(prefix: string): string`**
  - Generates unique IDs for cards/columns
  - Format: `${prefix}-${timestamp}-${random}`

- **`findColumnId(columns: Column[], id: string): string | undefined`**
  - Finds column ID given a card ID or column ID
  - Returns undefined if not found

- **`isColumnId(columns: Column[], id: string): boolean`**
  - Checks if ID is a column (vs a card)

**Tests**: [kanban.test.ts](src/lib/kanban.test.ts)

- Move cards within column (reorder)
- Move cards between columns
- Drop cards to column end

---

### Test Setup

**Vitest Configuration** (`vitest.config.ts`):

- Environment: jsdom
- Coverage: v8
- Testing library plugins enabled

**Test Setup** (`src/test/setup.ts`):

- Global test utilities setup
- Jest DOM matchers

**Test Patterns**:

- Component tests use `@testing-library/react`
- User interactions via `@testing-library/user-event`
- Snapshot testing not currently used
- Focus on behavior testing

---

## Styling

**Approach**: Tailwind CSS 4 with custom design tokens

**Color Scheme**:

- Accent Yellow: `#ecad0a`
- Blue Primary: `#209dd7`
- Purple Secondary: `#753991`
- Dark Navy: `#032147`
- Gray Text: `#888888`

**Current State**:

- Global styles in `src/app/globals.css`
- Component-level styling via Tailwind classes
- Responsive design using Tailwind breakpoints

---

## Testing

### Unit Tests (Vitest)

**Current Coverage**:

- `kanban.ts`: Move logic thoroughly tested
- `KanbanBoard.tsx`: Component rendering and interactions
- Basic event handling

**Gap Identified**:

- No tests for column rename edge cases
- Limited error boundary testing
- No accessibility tests yet

### E2E Tests (Playwright)

**Location**: `tests/kanban.spec.ts`

**Current Tests**:

- [To be documented - check test file]

### NPM Scripts

```json
"test": "vitest run",              // Run all unit tests once
"test:unit": "vitest run",         // Same as test
"test:unit:watch": "vitest",       // Watch mode for development
"test:e2e": "playwright test",     // Run E2E tests
"test:all": "npm run test:unit && npm run test:e2e"  // Both
```

---

## State Management

**Current Approach**: Local React state via `useState`

**Data Flow**:

- KanbanBoard holds board state (columns + cards)
- Child components receive slices of state
- User actions call callbacks up to KanbanBoard
- KanbanBoard updates state immutably

**Limitations** (MVP stage):

- No persistence (resets on page reload)
- No sync with backend (all data local)
- No undo/redo functionality
- No optimistic updates for async operations

---

## Known Issues & TODOs

- [ ] No error boundaries implemented
- [ ] No loading states for async operations (will be added in Part 7)
- [ ] No session management yet (will be added in Part 4)
- [ ] CSS class names not yet using BEM or other convention
- [ ] No keyboard navigation for accessibility
- [ ] Mobile responsiveness needs review
- [ ] No undo/redo functionality

---

## Integration Points (Planned)

**Part 4**: Authentication

- Add login page
- Protect board route
- Persist auth session

**Part 7**: Backend API

- Replace local state with API calls
- Add error handling for network failures
- Implement optimistic updates
- Add loading states

**Part 10**: AI Chat

- Add sidebar chat component
- Connect to AI API
- Allow AI to update board

---

## Development Commands

```bash
# Install dependencies
npm install

# Development server (hot reload)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Run all tests
npm run test:all

# Run tests in watch mode (development)
npm run test:unit:watch

# Run E2E tests
npm run test:e2e
```

---

## Code Quality Standards

1. **TypeScript**: Strict mode enabled, all types explicitly defined
2. **Naming**: Descriptive component names, camelCase for functions/variables
3. **Simplicity**: Favor clarity over clever code
4. **Immutability**: State updates create new objects/arrays
5. **Testing**: Unit tests for logic, component tests for UI

---

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- No IE11 support (uses ES2020+ features)

---

## Performance Considerations

- Kanban board uses React keys for list rendering
- Drag-and-drop uses `@dnd-kit` (optimized for performance)
- No memoization currently (may add if performance issues arise)
- CSS-in-JS: Tailwind is compiled to static CSS (good performance)

---

## Next Steps

1. **Part 1 (Planning)**: ✓ Complete - This documentation serves as Part 1 frontend documentation
2. **Part 4 (Auth)**: Add login page and session management
3. **Part 7 (API)**: Connect to backend API for persistence
4. **Part 10 (AI Chat)**: Add chat sidebar with AI integration
