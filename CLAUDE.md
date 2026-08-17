# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Claude Code plugin marketplace for the Cloud Security Alliance (CSA). It hosts official CSA plugins that users install via:
```
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
/plugin install {plugin-name}@csa-plugins-official
```

Almost all content is Markdown. There is no build step, no package manager, and no repo-level test runner. The "code" is mostly *methodology* — phased analytical workflows that Claude executes on the user's behalf.

## Repository Layout

- `.claude-plugin/marketplace.json` — Marketplace manifest listing every installable plugin. **Must be updated when adding/removing plugins.**
- `plugins/` — Internal plugins developed by CSA.
- `external_plugins/` — Third-party plugins (placeholder; submission process TBD).
- `docs/superpowers/{specs,plans}/` — Repo-level design specs and implementation plans, date-prefixed (`YYYY-MM-DD-<topic>-design.md`). Per-plugin design docs live in `plugins/{name}/docs/` using the same naming.
- `.superpowers/sdd/` — Spec-driven-development scratch state (review diffs, progress notes). Working artifacts, not documentation.
- `.claude/` is **gitignored** — local permissions in `.claude/settings.local.json` are not shared.

## Plugin Anatomy

```
plugins/{name}/
├── .claude-plugin/plugin.json   # manifest — REQUIRED, and it lives HERE, not at plugin root
├── .mcp.json                    # optional MCP server config
├── skills/{skill-name}/         # auto-discovered by directory name
├── commands/*.md                # optional slash commands
├── agents/*.md                  # optional
├── scripts/                     # optional tooling (validators, data query tools, tests)
├── data/                        # optional bundled data + its own upstream LICENSE + VERSION.txt
├── docs/                        # optional design docs
├── FEEDBACK.md                  # points to repo GitHub Issues; use [plugin-name] title prefix
└── LICENSE
```

Component directories are **auto-discovered by name** — no plugin manifest declares component paths, so don't add such fields. `plugin.json` carries: `name`, `version`, `description`, `author`, and optionally `homepage`, `license`, `dependencies`.

`dependencies` is an array of other plugin names (see `vulnerability-audit`, which depends on `secid` and `cwe-analysis`).

### Metadata that must stay in sync

Adding or changing a plugin touches three files. All three drift silently — there is no validation script.

| Field | `plugin.json` | `marketplace.json` | `README.md` table |
|---|---|---|---|
| `description` | must match ↔ | must match ↔ | shortened is fine |
| `version` | required | required | — |
| `author` | may be an individual (e.g. Kurt Seifried) | always Cloud Security Alliance | — |

Only `description` and `version` must match exactly. `source` paths in marketplace.json are relative (`./plugins/{name}`).

## Skill Architecture

Skills use **progressive disclosure** to protect the context window:

```
skills/{name}/
├── SKILL.md        # YAML frontmatter + scope + routing table only
├── phases/         # phase-N-*.md — read one at a time, when reached
├── references/     # shared frameworks, read when first needed
├── templates/      # output scaffolds (vulnerability-audit)
├── styles/         # per-mode variants (nist-ir-8477-mapping)
└── fixtures/       # test inputs (validate-findings)
```

Rules that make this work, and that new skills must honor:

- **SKILL.md routes; it does not teach.** It holds scope, the phase list, and cross-cutting invariants. Analytical content belongs in a phase file.
- **Never read ahead.** Each phase file assumes only that *prior* phases' outputs exist on disk. Reading phase 4 during phase 1 defeats the design.
- **Paths in skill files are relative to the SKILL.md directory**, except bundled scripts, which use `${CLAUDE_PLUGIN_ROOT}/scripts/...` (an absolute plugin path — the only way a script reference survives installation).
- **The frontmatter `description` is the trigger.** It must state both what the skill does and when to activate, because Claude decides whether to load the skill from that string alone.

## Cross-Cutting Methodology Patterns

These recur across plugins by design. Match them when adding a plugin rather than inventing an alternative.

**Confidence frameworks.** Every analytical plugin has `references/confidence-framework.md` requiring each AI-produced claim to be tagged with an explicit confidence level. They are deliberately *not* shared — each is tuned to its domain (incident-analysis distinguishes Confirmed/Corroborated by source independence; cwe-analysis separates evidence quality from taxonomy precision, adapted from ICD 203). A new analytical plugin needs its own, not a copy.

**Cross-model validation.** Three plugins ship a `scripts/validate-*.sh` that sends completed output to the `codex` and `gemini` CLIs for independent adversarial review — different providers, so provider-specific blind spots don't survive both. Each writes `<input>.codex-review.md` / `<input>.gemini-review.md` beside the input, and exits 0 if at least one review succeeded. (`vulnerability-audit` gets the same effect differently: adversarial skeptic subagents inside its `validate-findings` skill.)

The current convention: the review prompt is **not hardcoded**. It lives in the skill's `references/validation-prompt.md` and the script extracts the first fenced code block:
```bash
REVIEW_PROMPT="$(sed -n '/^```$/,/^```$/p' "$PROMPT_FILE" | sed '1d;$d')"
```
So prompt changes are edits to a reference file a reviewer can read, not to shell. `incident-analysis/scripts/validate-report.sh` predates this and still uses an inline heredoc — follow the newer plugins.

**Disk-backed checkpointing.** `vulnerability-audit` runs audits longer than one context window. `scripts/checkpoint.py` (`save|shard|done|load|append|reset`) owns a state directory (`./.audit-state`, `./.validate-state`); skill files must go through it rather than writing state by hand, so a resumed session can reconstruct where it was.

## Two Kinds of Plugin

Worth knowing before editing, because the failure modes differ:

- **Methodology plugins** (`incident-analysis`, `cwe-analysis`, `security-knowledge-ingestion`, `nist-ir-8477-mapping`, `vulnerability-audit`) — Markdown workflows plus stdlib-only helper scripts. Nothing to install; bugs are analytical, and are caught by review and cross-model validation.
- **Code plugins** (`secid`) — a real runtime. `server.py` is a FastMCP server wrapping the SecID REST API, launched via `.mcp.json` as `python3 ${CLAUDE_PLUGIN_ROOT}/server.py`, and it **requires `pip install mcp httpx`** (the only external dependency in the repo). Accepts `--base-url` for internal resolvers. Its `skills/` and `agents/` hold only placeholder READMEs.

## Testing and Validation

No global build or test step. Run per-plugin suites from the repo root:

```bash
# cwe-analysis — 30 tests for the query tool, 6 verifying docs match real data output
python3 plugins/cwe-analysis/scripts/test_cwe_tool.py
python3 plugins/cwe-analysis/scripts/test_doc_truth.py

# vulnerability-audit — 7 unittest cases for checkpoint state handling
python3 plugins/vulnerability-audit/scripts/test_checkpoint.py
```

`test_doc_truth.py` is the unusual one: it asserts that examples written in the skill's Markdown still match what `cwe-tool.py` actually returns. Editing CWE prose or bumping bundled data can break it.

**Running a single test.** Only `test_checkpoint.py` supports it, and only from its own directory (the scripts dirs are not importable packages):

```bash
cd plugins/vulnerability-audit/scripts
python3 -m unittest test_checkpoint.CheckpointTest.test_done_marks_complete
```

The two cwe-analysis runners are hand-rolled — a hardcoded list of plain functions with no argv parsing, so there is no filter flag. To run one in isolation, temporarily trim the `tests = [...]` list at the bottom of the file. Both exit non-zero on failure.

Query the bundled CWE data with `python3 plugins/cwe-analysis/scripts/cwe-tool.py {lookup,search,candidates,children,chain,ai-relevant,version,similar}`. Data version is pinned in `data/VERSION.txt` (currently CWE 4.16, 944 rows).

Cross-model validators (require `codex` and/or `gemini` CLIs installed):
```bash
plugins/incident-analysis/scripts/validate-report.sh <report.md>
plugins/security-knowledge-ingestion/scripts/validate-decomposition.sh <output.json> [source.md]
plugins/nist-ir-8477-mapping/scripts/validate-mapping.sh <mapping.json> [focal.json] [reference.json]
```

## Adding a New Plugin

1. `plugins/{name}/.claude-plugin/plugin.json` — name, version, description, author.
2. Component directories (`skills/`, `commands/`, `agents/`) — no manifest registration needed.
3. `FEEDBACK.md` and `LICENSE`.
4. Register in `.claude-plugin/marketplace.json` under `plugins` (name, description, author, version, source, category, homepage).
5. Add a row to the README "Available Plugins" table.
6. Verify description and version match across plugin.json and marketplace.json.

## Current Plugins

| Plugin | Distinctive to it |
|---|---|
| `incident-analysis` | 10 phases, cloud/AI incidents; older heredoc-style validator |
| `cwe-analysis` | Bundles MITRE CWE 4.16 data + `cwe-tool.py`; the only plugin with real unit tests over data |
| `security-knowledge-ingestion` | Converts standards/regulations to structured data; checks SecID first; license verification before contribution |
| `nist-ir-8477-mapping` | Four relationship styles in `styles/`; OLIR/CPRT JSON + Excel export; consumes ingestion output |
| `secid` | MCP server (`server.py`) + slash commands; needs `mcp`/`httpx` |
| `vulnerability-audit` | Two skills (`audit`, `validate-findings`); `checkpoint.py` state machine; `dependencies` on secid + cwe-analysis; static-only |

## Other Conventions

- Scripts use only Python stdlib or POSIX shell. The single exception is `secid/server.py`. Keep it that way — users install plugins, they don't run `pip install -r`.
- Bundled data carries the upstream license file alongside it (`data/MITRE-CWE-LICENSE.txt`) plus a `VERSION.txt` recording version, export date, row count, and source URL.
- Plugins reference each other by name in prose to chain workflows (ingestion → mapping; audit → cwe-analysis). Prefer suggesting a sibling plugin over duplicating its methodology.
