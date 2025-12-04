# Copilot instructions for WPG-Solver

Short goal: quickly become productive by discovering language, build/test commands, entrypoints, and the project's conventions.

1. Detect language & authoritative manifests
   - Check for: package.json, pyproject.toml, setup.py, requirements.txt, Cargo.toml, go.mod, CMakeLists.txt, Makefile.
   - Also inspect README.md and .github/workflows/ for canonical commands and CI steps.

2. Identify entrypoints and runtime shapes
   - Look for CLI code in src/ or cmd/, web APIs in api/ or server/, and core solver logic in directories named solver, core, engine, or wpg.
   - Example heuristic: if package.json contains "bin" or "scripts.start" use `npm run start`; if pyproject.toml lists [tool.poetry.scripts] use `poetry run <script>`.

3. Build / test / debug commands (extract from manifests & CI)
   - JavaScript/TypeScript: prefer npm ci && npm test (or yarn install && yarn test).
   - Python: prefer virtualenv or poetry; use requirements.txt or pyproject.toml to install, run tests with pytest.
   - C/C++: follow CMakeLists.txt / Makefile; CI often shows the exact flags.
   - Always mirror the CI YAML step when unsure.

4. Repository conventions to follow
   - Config: look for .env, config.yml, or settings.py — these are the canonical runtime config locations.
   - Tests: tests/ or __tests__/ should run with pytest, jest, or similar test runner based on manifest.
   - Expose public API from index.py/index.ts or package "main" field — modify these with care.

5. Integration & dependency signals
   - Inspect requirements.txt/package.json/go.mod to list critical libraries (solver engines, numeric libs).
   - For external services, search for hostnames, API keys, or RPC clients in config files and .github/workflows.

6. Code style & PR guidance
   - Follow existing lint config files: .eslintrc.*, pyproject.toml [tool.black]/[tool.flake8], .clang-format, etc.
   - Mirror formatting and test patterns found in the repo; running the same lint/test steps as CI is required before proposing code changes.

7. Examples (how to discover actionable commands)
   - If package.json exists:
     - `cat package.json` → use "scripts" values; prefer `npm ci` for reproducible installs.
   - If pyproject.toml exists:
     - `poetry install` / `poetry run pytest` or fallback to `pip install -r requirements.txt` then `pytest`.
   - If .github/workflows/ contains build steps:
     - Copy the exact commands from the workflow for local dev and tests.

8. When modifying files
   - Preserve top-level exports/entrypoints.
   - Update tests that reference changed public behavior.
   - If adding new dependencies, add them to the authoritative manifest (package.json/pyproject.toml/requirements.txt).

9. Merging guidance
   - If a .github/copilot-instructions.md already exists, merge preserving repository-specific sections (commands, CI snippets). Add missing detection heuristics above.

If any part of the repository layout or CI is unclear, tell me which files you want me to inspect and I will re-generate or refine these instructions.
