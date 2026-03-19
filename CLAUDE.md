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
- `plugins/` — Internal plugins developed by CSA. Each has a `plugin.json` and component directories (skills, commands, agents).
- `external_plugins/` — Third-party plugins (placeholder; submission process TBD).

## Plugin Structure Convention

Each plugin lives under `plugins/{name}/` and must have:
- `plugin.json` — Plugin manifest (name, description, version, author, component paths)
- Component directories as needed: `skills/`, `commands/`, `agents/`

Skills use progressive disclosure: a top-level `SKILL.md` with YAML frontmatter (name, description) routes to phase files and reference material in subdirectories. Phase files are read on-demand, not upfront.

## Adding a New Plugin

1. Create `plugins/{name}/plugin.json` with required fields (name, description, version, author, component paths)
2. Add component directories and content
3. Register the plugin in `.claude-plugin/marketplace.json` under the `plugins` array (name, description, author, source path, category, homepage)
4. Both manifests must stay in sync

## Current Plugins

- **incident-analysis** — Security incident analysis skill with phased workflow (discovery → collection → source analysis → vendor analysis → timeline → impact assessment → gap analysis → defensive recommendations → report). Focused on cloud and AI security incidents.

## Key Conventions

- Plugin `source` paths in marketplace.json are relative (e.g., `./plugins/incident-analysis`)
- Skill `description` in YAML frontmatter doubles as the trigger description — it must clearly convey when the skill should activate
- Skills reference files with paths relative to the SKILL.md location
- Content is Markdown throughout; no build step
