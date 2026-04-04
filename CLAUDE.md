# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Claude Code plugin marketplace for the Cloud Security Alliance (CSA). It hosts official CSA plugins that users install via:
```
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
/plugin install {plugin-name}@csa-plugins-official
```

## Repository Layout

- `.claude-plugin/marketplace.json` — Marketplace manifest. Lists all installable plugins with metadata. **Must be updated when adding/removing plugins.**
- `plugins/` — Internal plugins developed by CSA. Each has a `plugin.json` and component directories.
- `external_plugins/` — Third-party plugins (placeholder; submission process TBD).

## Plugin Structure Convention

Each plugin lives under `plugins/{name}/` and must have:
- `plugin.json` — Plugin manifest at the plugin root (name, description, version, author, component paths). Note: the README shows `.claude-plugin/plugin.json` but existing plugins use `plugin.json` at the plugin root directly.
- Component directories as needed: `skills/`, `commands/`, `agents/`
- `FEEDBACK.md` — Shared feedback template pointing to the repo's GitHub Issues. Use `[plugin-name]` prefix in issue titles.
- `LICENSE` — Per-plugin license file.

Optional directories:
- `scripts/` — Tooling (validation scripts, data query tools, tests)
- `data/` — Bundled data files (CSVs, etc.) with their own license files
- `docs/` — Design documents and plans

### Skill Architecture

Skills use **progressive disclosure** to manage context window usage:
```
skills/{name}/
├── SKILL.md              # Entry point — YAML frontmatter + workflow routing
├── phases/               # Phase files read on-demand, not upfront
│   ├── phase-1-*.md
│   └── ...
└── references/           # Shared frameworks (confidence, quality, etc.)
    ├── confidence-framework.md
    └── ...
```
SKILL.md provides the overview and routes to phase files. Each phase file is self-contained and read only when that phase is reached. Reference materials are read when first needed.

## Adding a New Plugin

1. Create `plugins/{name}/plugin.json` with required fields (name, description, version, author, component paths)
2. Add component directories and content
3. Add `FEEDBACK.md` and `LICENSE`
4. Register the plugin in `.claude-plugin/marketplace.json` under the `plugins` array (name, description, author, source path, category, homepage)
5. Update the "Available Plugins" table in `README.md`
6. Both manifests and README must stay in sync

## Current Plugins

- **incident-analysis** — Security incident analysis with phased workflow (discovery → collection → source analysis → vendor analysis → timeline → impact → gap analysis → defensive recommendations → report → cross-model validation). Focused on cloud and AI security incidents. Has `scripts/validate-report.sh` for cross-model validation via Codex/Gemini CLIs.
- **cwe-analysis** — CWE assignment and vulnerability chain analysis for CNAs and security researchers. Phased workflow (intake → code analysis → CWE identification → chain analysis → validation → report). Bundles MITRE CWE data in `data/` and includes `scripts/cwe-tool.py` for querying it.

## Testing and Validation

There is no global build or test step. Each plugin may have its own scripts:

- **cwe-analysis**: `python3 plugins/cwe-analysis/scripts/test_cwe_tool.py` and `python3 plugins/cwe-analysis/scripts/test_doc_truth.py` — verify the CWE query tool and documentation accuracy. Uses only Python stdlib (no pip install needed).
- **incident-analysis**: `plugins/incident-analysis/scripts/validate-report.sh <report.md>` — sends a completed report to Codex and/or Gemini CLIs for adversarial review. Requires `codex` and/or `gemini` CLI tools.

## Key Conventions

- Plugin `source` paths in marketplace.json are relative (e.g., `./plugins/incident-analysis`)
- Skill `description` in YAML frontmatter doubles as the trigger description — it must clearly convey when the skill should activate
- Skills reference files with paths relative to the SKILL.md location
- Content is Markdown throughout; no build step
- Scripts use only Python stdlib or shell — no external dependencies to install
- Each plugin's `plugin.json` description must match its entry in `marketplace.json`
