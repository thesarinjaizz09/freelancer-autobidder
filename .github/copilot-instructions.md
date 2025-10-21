<!-- .github/copilot-instructions.md -->
# Repo-specific Copilot instructions

This file tells an AI coding agent how to get productive in this repository. The current workspace contains no detected project files (package manifests, build configs, or source directories). Use these steps to discover the project's shape and to make safe, minimally invasive changes.

1. Quick discovery (run these in PowerShell):
   - Look for common manifests and config files:
     - Node: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `tsconfig.json`
     - Python: `pyproject.toml`, `requirements.txt`, `setup.py`
     - .NET: `*.csproj`, `global.json`
     - Containers: `Dockerfile`, `docker-compose.yml`
   - Example PowerShell commands:
     - `Get-ChildItem -Recurse -Filter package.json -ErrorAction SilentlyContinue`
     - `Get-ChildItem -Recurse -Include pyproject.toml,requirements.txt`

2. If the repository remains empty or lacks build files:
   - Do not invent a project type. Instead, add a small scaffold only after asking the human (see "Ask the user").
   - Create minimal, clearly-named artifacts (for example: `README.md` or `.github/ISSUE_TEMPLATE.md`) and mark them as scaffolding in the commit message.

3. How to infer architecture (when files exist):
   - Trace the main entry points. For Node look for `main` in `package.json` or `src/index.js|ts`. For Python look for top-level packages or a `__main__`.
   - Identify service boundaries by folders (e.g., `api/`, `worker/`, `web/`, `libs/`).
   - Note cross-component communication: look for HTTP clients, message queue libraries (AMQP, SQS), or shared database modules.

4. Testing & build commands (discover, don't assume):
   - Search for npm scripts: `jq -r '.scripts' package.json` (if present) or open `package.json`.
   - For Python, check `tox.ini`, `pytest.ini`, or `pyproject.toml` under `[tool.pytest]`.
   - If no commands are found, ask the user for the canonical build/test command before adding CI or tests.

5. Repo conventions observed here:
   - Currently there are no discoverable source files. Treat any new files as exploratory scaffolding and label commits clearly (e.g., `chore(scaffold): add README and agent instructions`).

6. Safe editing rules for AI agents working here:
   - Limit changes to a single small task per PR (one feature or one refactor). Keep diff readable.
   - Add or modify tests when you add behavior. If you can’t run tests locally because of missing environment, document how you validated changes.
   - Don’t push large dependency upgrades without human approval.

7. Examples to reference when present (use these paths if they appear):
   - `src/` or `lib/` — main application code
   - `tests/`, `__tests__/` — unit/integration tests
   - `Dockerfile`, `.github/workflows/` — CI and containerization

8. Ask the user (required before larger changes):
   - What is the primary language/framework? (Node, Python, .NET, etc.)
   - What are the exact build/test commands and how do you run them locally on Windows PowerShell?
   - Do you want small scaffolding commits committed directly or staged for review as PRs?

If anything in this guidance is unclear or you want the file tuned to a specific stack (for example TypeScript monorepo or Django app), reply with the project type and I will update this file accordingly.
