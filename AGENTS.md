# Repository Guidelines

## Project Structure & Module Organization
- Place application code in `src/` with clear module folders (`src/core`, `src/api`, `src/ui`, etc.). Keep shared utilities in `src/lib`.
- Mirror code layout in `tests/` (e.g., `tests/core/test_*.py` or `tests/api/*.spec.ts`). Integration fixtures can live in `tests/fixtures/`.
- Store scripts and one-off tooling in `scripts/`; keep long-form notes in `docs/`. Check in sample configs as `.env.example`.
- Binary assets (images, fonts) should live in `assets/` with optimized versions when possible.

## Build, Test, and Development Commands
- Prefer Make targets as entry points; add them if missing:
  - `make install` – install dependencies (pin versions and vendor lockfiles where applicable).
  - `make lint` – run linters/formatters; fail on warnings.
  - `make test` – execute the full test suite; keep it fast for CI.
  - `make dev` – start the local app/server with live reload where supported.

## Coding Style & Naming Conventions
- Follow language defaults: 4-space indent for Python, 2-space for JS/TS; avoid tab characters.
- Filenames: snake_case for Python modules, kebab-case for scripts, PascalCase only for React components or classes.
- Keep functions small and pure where practical; document non-obvious decisions inline. Prefer composition over deep inheritance.
- Run formatters (e.g., `ruff format`/`black` for Python, `prettier` for JS/TS) before pushing.

## Testing Guidelines
- Co-locate fast unit tests under `tests/` with names like `test_feature.py` or `feature.spec.ts`. Integration/e2e tests belong in `tests/integration/` to allow selective runs.
- Aim for meaningful coverage (functionality over percentage). Add regression tests for every bug fix.
- Use deterministic data; seed randomness. For network/file system boundaries, provide fakes or fixtures rather than hitting live services.

## Commit & Pull Request Guidelines
- Commits: short imperative subject (`feat: add auth guard`), wrap body at ~72 chars, and explain “what” plus “why.” Keep changes focused; avoid mixing refactors with feature work.
- Pull Requests: include a concise summary, linked issue, screenshots for UI changes, and a test plan showing exact commands run (e.g., `make test`, `make lint`). Note any follow-ups or known gaps.
- Ensure new files include headers or docstrings where needed and that CI targets pass locally before requesting review.

## Security & Configuration Tips
- Never commit secrets; use environment variables with a checked-in `.env.example`. Rotate keys immediately if exposed.
- Lock dependencies and update regularly; prefer minimal privilege for any credentials used in local testing.
