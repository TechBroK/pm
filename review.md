**Repository Review — Deployment Readiness**

Summary

- **Scope**: quick audit for deployment readiness, redundancies, ignored/test-only files, and actionable fixes.

**Areas Needing Adjustment**

- **Frontend Build & CI**: Ensure `frontend/dist` is produced by CI. Add a GitHub Action (or similar) to run `npm ci && npm run build` and publish artifacts.
- **Dockerfile (multi-stage)**: Consider a multi-stage Dockerfile that builds the Next frontend (Node stage) and copies only the production build into a slim Python image to avoid shipping dev deps.
- **Env handling & secrets**: Move secrets out of repo; ensure `.env` is not committed. Use secret management for production (Docker secrets, env vars in CI/CD).
- **AI error handling & rate-limits**: Add hardened error handling and retries with backoff in `backend/ai_service.py`; add rate limiting or request queuing to avoid abuse.
- **Logging & monitoring**: Add structured logs and health endpoints for container orchestration; integrate basic metrics (request counts, error rates).
- **Database migrations**: Add a migration strategy (Alembic or similar) and do not commit runtime DB file (e.g., `backend/kanban.db`) into source control.
- **Tests & E2E stability**: Add CI steps to run both unit tests (`vitest`, `pytest`) and Playwright E2E; stabilize flaky tests and pin node/python lockfiles.

**Redundancies & Duplicates**

- Multiple `AGENTS.md` files found at root and in `backend/`, `frontend/`, `scripts/` — consolidate if they duplicate content.
- Duplicate dev/start scripts: both `.bat` and `.sh` variants exist in `scripts/`; keep both if cross-platform support is required, otherwise centralize.
- Coverage and build artifacts: `frontend/coverage/` and `coverage/` exist — ensure CI artifacts go to a single location and add them to `.gitignore` if generated.

**Files Used Only For Local Testing / Debugging**

- `comprehensive_demo.py`, `debug_move_card.py`, `check_db.py` — useful for local smoke tests and debugging but not required at runtime. Recommendation: move to `tools/` or keep but exclude from Docker image via `.dockerignore`.
- Root-level test scripts (`test_*.py`) are for CI/verification — keep in repo but ensure CI runs them; they are not needed inside runtime containers.

**Ignored Files & Missing Ignores**

- `.gitignore` already ignores `.env`, `.venv`, `db.sqlite3` etc. Verify `backend/kanban.db` (runtime DB) is not committed; add it to `.gitignore` if present.
- `.dockerignore` should exclude test artifacts and local-only scripts (add `comprehensive_demo.py`, `debug_move_card.py`, `check_db.py`, `frontend/.next/`, `frontend/node_modules/` if not already excluded).

**Quick Action Items (priority)**

- Add `review.md` to the repo (this file).
- Add CI workflow: `install -> lint -> test -> build frontend -> build backend image`.
- Update `Dockerfile` to multi-stage build for frontend or add a separate `Dockerfile.frontend` step in CI.
- Move or ignore local debug scripts; add them to `.dockerignore`.
- Add migration tooling and ensure DB file is not in repo.

If you want, I can implement the CI workflow or convert the `Dockerfile` into a multi-stage build next.
