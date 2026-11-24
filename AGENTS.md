# Chunkflow Core — Workspace Rules

Stack: Python

## 1. Subsystem Boundaries & Verification
Use root automation to execute standard quality gates across subsystems:
- **Full-Suite Check**: Run tests with `uv run python -m unittest discover tests`.
- **Generated Types Are Read-Only**: Never edit generated types directly. Update schemas/migrations and run the generator command.

## 2. Documentation Guidelines
- **Doc-First Discovery**: Before analyzing code or wandering through files to figure out the structure or purpose of an unfamiliar subsystem/file, search documentation first under `docs/`. They contain curated architectural context, schema summaries, and module responsibilities.
- **Macro Dossier (`docs/systems/*.md`, `docs/systems/workflows/*.md`)**: Consult as an advisory reference when exploring unfamiliar architecture. Update only when altering cross-cutting system designs, schemas, or end-to-end user workflows. Minor bug fixes, UI styling, and local refactors do not require macro-doc edits.
- **Developmental Plans & Roadmaps (`docs/plans/`)**: Feature overhauls, milestones, and architectural phases must be planned in `docs/plans/`. Plan filenames MUST be prefixed with their creation timestamp (`YYYY-MM-DD_HHMMSS_<slug>.md`) to record developmental history. Each plan maintains lifecycle status badges (`🔴 INCOMPLETE / PLANNED`, `🟡 IN PROGRESS`, `🟢 COMPLETED`) and an interactive objective checklist. Keep `docs/plans/README.md` synchronized.

## 3. Ongoing Documentation Maintenance Protocol (Agent Operational Rules)
When implementing features or refactoring code during conversation turns, follow this maintenance lifecycle:
1. **On Milestone & Phase Progress (`docs/plans/`)**:
   - Check off completed deliverables in the active plan (`- [ ]` -> `- [x]`).
   - When all objectives pass verification, update the status badge to `🟢 COMPLETED` and run `python ~/.gemini/config/plugins/workspace-docs/skills/workspace-docs/scripts/manage_plans.py update <plan_name> --status completed` to sync `docs/plans/README.md`.
2. **On Cross-Cutting Architectural Shifts (`docs/systems/`)**:
   - Update `docs/systems/*.md` only when changing system topologies, introducing new services, altering database schemas, or modifying wire communication protocols.

## 4. Workspace Conventions
- **Git**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
- **Logs**: Filter logs by level or request ID. Use project logger; avoid unstructured stdout/print.
- **Scratch**: Use `./.scratch/` for temp scripts (gitignored).


## Documentation Layer Separation & Conversation-Time Arbitration

This workspace maintains potentially overlapping documentation types. To prevent drift, circular debates, and redundant writes during conversations, adhere to these pre-compiled arbitration gotchas:
