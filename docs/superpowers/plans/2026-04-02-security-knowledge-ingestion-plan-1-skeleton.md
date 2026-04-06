# Security Knowledge Ingestion — Plan 1: Plugin Skeleton

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an installable plugin skeleton with SKILL.md entry point that routes to phase files (phase files written in Plan 2).

**Architecture:** Follow existing csa-plugins-official patterns (incident-analysis, cwe-analysis). Plugin has plugin.json, SKILL.md with progressive disclosure, FEEDBACK.md, LICENSE. Registered in marketplace.json and README.md.

**Tech Stack:** Markdown, JSON, shell. No build system.

**Spec:** `docs/superpowers/specs/2026-04-02-security-knowledge-ingestion-design.md`

**Repo:** `/Users/kurt/GitHub/CloudSecurityAlliance/csa-plugins-official`

**Branch:** `plugin/security-knowledge-ingestion`

---

## File Map

### New Files

| File | Responsibility |
|------|---------------|
| `plugins/security-knowledge-ingestion/plugin.json` | Plugin manifest |
| `plugins/security-knowledge-ingestion/FEEDBACK.md` | Issue filing instructions |
| `plugins/security-knowledge-ingestion/LICENSE` | Apache 2.0 |
| `plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion/SKILL.md` | Entry point, progressive disclosure, workflow routing |

### Modified Files

| File | Change |
|------|--------|
| `.claude-plugin/marketplace.json` | Add plugin entry |
| `README.md` | Add to Available Plugins table |

---

## Task 1: Create feature branch

**Files:** None

- [ ] **Step 1: Create branch**

```bash
cd /Users/kurt/GitHub/CloudSecurityAlliance/csa-plugins-official
git checkout -b plugin/security-knowledge-ingestion main
```

- [ ] **Step 2: Create directory structure**

```bash
mkdir -p plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion/phases
mkdir -p plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion/references
mkdir -p plugins/security-knowledge-ingestion/scripts
```

- [ ] **Step 3: Commit**

```bash
git add plugins/security-knowledge-ingestion/
git commit --allow-empty -m "Create security-knowledge-ingestion plugin directory structure

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Create plugin.json

**Files:**
- Create: `plugins/security-knowledge-ingestion/plugin.json`

- [ ] **Step 1: Write plugin.json**

```json
{
  "name": "security-knowledge-ingestion",
  "description": "Ingest security knowledge documents (standards, regulations, frameworks, controls, capabilities) into structured, machine-readable data. Checks SecID for existing structured data, handles license verification for contributions, produces reproducible conversion recipes, and guides users toward proper data management.",
  "version": "0.1.0",
  "author": {
    "name": "Kurt Seifried",
    "email": "kseifried@cloudsecurityalliance.org"
  },
  "skills": [
    "skills/security-knowledge-ingestion/SKILL.md"
  ]
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool plugins/security-knowledge-ingestion/plugin.json > /dev/null
```

Expected: No output (valid JSON).

- [ ] **Step 3: Commit**

```bash
git add plugins/security-knowledge-ingestion/plugin.json
git commit -m "Add security-knowledge-ingestion plugin.json

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Create FEEDBACK.md and LICENSE

**Files:**
- Create: `plugins/security-knowledge-ingestion/FEEDBACK.md`
- Create: `plugins/security-knowledge-ingestion/LICENSE`

- [ ] **Step 1: Write FEEDBACK.md**

```markdown
# Feedback, Bug Reports, and Feature Requests

**Repository:** https://github.com/CloudSecurityAlliance/csa-plugins-official

This plugin is part of a multi-plugin repository. If you run into a problem, find a bug, have a feature request, or just want to share feedback — we want to hear from you. This tooling is new and your input directly shapes how it improves.

## When to File an Issue

You should file an issue if you experience any of the following:

- **Bug** — something is broken, produces an error, crashes, or doesn't work as expected
- **Flaw** — the output is wrong, misleading, incomplete, or lower quality than it should be
- **Unexpected behavior** — the plugin did something confusing, surprising, or that didn't match what you thought would happen
- **Problem** — something is difficult to use, unclear, frustrating, or feels like it's not working right
- **Missing feature** — there's something you wish it did, a capability gap, or a workflow improvement that would help
- **Feature request** — you have an idea for new functionality, an enhancement, or an improvement
- **Confusion** — the instructions were unclear, the workflow didn't make sense, or you got stuck and didn't know what to do next
- **Methodology discussion** — you disagree with a design decision, think a phase should work differently, or want to propose a structural change. We treat methodology disagreements the same way we treat bugs — they're issues to be investigated, discussed, and resolved.
- **Feedback** — any general thoughts, suggestions, criticism, or observations about your experience

If you're unsure whether something is worth reporting — it is. Even "this felt weird" or "I didn't understand this part" is valuable.

## How to File an Issue

1. Go to: https://github.com/CloudSecurityAlliance/csa-plugins-official/issues
2. Click **"New Issue"**
3. In the **title**, include the plugin name (e.g., `[security-knowledge-ingestion] Brief description of the issue`)
4. In the **body**, tell us:
   - **What happened** — describe the bug, problem, error, or unexpected behavior you encountered
   - **What you expected** — what you thought should have happened instead
   - **Steps to reproduce** (if applicable) — what were you doing when the issue occurred
   - **Any other context** — screenshots, error messages, what phase you were in, or anything else that helps

Including the plugin name in the title is important because this repository contains multiple plugins and it helps us route your issue to the right place.

## What Happens Next

We review all submitted issues. Your bug report, feature request, or feedback helps us identify defects, prioritize improvements, and fix problems. We may ask follow-up questions to better understand the issue.

Thank you for helping make these tools better.
```

- [ ] **Step 2: Copy LICENSE from incident-analysis**

```bash
cp plugins/incident-analysis/LICENSE plugins/security-knowledge-ingestion/LICENSE
```

- [ ] **Step 3: Commit**

```bash
git add plugins/security-knowledge-ingestion/FEEDBACK.md plugins/security-knowledge-ingestion/LICENSE
git commit -m "Add FEEDBACK.md and LICENSE for security-knowledge-ingestion

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Create SKILL.md

**Files:**
- Create: `plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: security-knowledge-ingestion
description: Ingest security knowledge documents (standards, regulations, frameworks, controls, capabilities) into structured, machine-readable data. Checks SecID for existing structured data, produces reproducible conversion recipes, and guides contribution. Use when the user wants to convert a security standard, regulation, framework, or other security knowledge document into structured data, or wants to check if SecID already has structured data for a source.
---

# Security Knowledge Ingestion

You are guiding a user through converting security knowledge documents into structured, machine-readable data. Your job is to help them identify the source, acquire the content, convert and decompose it into individually addressable concepts, capture a reproducible recipe, validate the output, and export it in useful formats.

## Scope

Security knowledge documents: standards (NIST, ISO, BSI), regulations (EU AI Act, GDPR), frameworks (CCM, CSF, ATT&CK), controls, capabilities, best practices, guidance documents. Any document that contains concepts (controls, requirements, outcomes, capabilities, recommendations) that need to be individually addressable.

## How This Works

This skill uses **progressive disclosure**. This file provides the overview and workflow routing. Detailed instructions for each phase are in separate files under `phases/`. Read each phase file when you reach that phase — not before.

Shared reference material (SecID integration, concept types, confidence framework, output formats, license handling, DataSets convention, validation prompt) is in `references/`. Read these when first needed and reference them throughout.

**File paths are relative to this SKILL.md's directory.**

## Teaching Mode

By default, you teach as you work — explain what concept types are, why hierarchy matters, how decomposition decisions affect downstream mapping, why recipes are important. This helps users internalize the methodology.

If the user says **"skip teaching"** or **"expert mode"**, suppress all teaching annotations. Produce only processing output.

## Tool Access

This plugin uses several tool categories:

1. **SecID MCP tools** — `resolve`, `lookup`, `describe` for checking if SecID already has structured data for a source. SecID v2 also serves structured data and recipes directly.
2. **File reading** — examine user-provided documents
3. **Web access** — fetch content from URLs, look up licenses at source sites
4. **Bash** — run conversion tools (marker, pandoc) when available

## Automation Spectrum

Ask the user how they want to work:

- **Interactive** — pause between every phase, teach as you go, review each decision
- **Semi-automated** — run phases 1-5 with minimal pauses, stop at validation for review
- **Fully automated** — run everything, present final output + validation results

Default to interactive for first-time users. If the user says "just do it" or similar, switch to fully automated.

## Workflow

Ask the user what they want to do:

### Option 1: Full Workflow

Walk through all phases start to finish. Read each phase file as you reach it.

1. **Phase 1 — Source Identification**: Read `phases/phase-1-source-identification.md` → identify the document, check SecID
   - **Pause**: "Here's what I found. SecID [has/doesn't have] this. How would you like to proceed?"
2. **Phase 2 — Acquisition**: Read `phases/phase-2-acquisition.md` → get the data into a workable state
3. **Phase 3 — Conversion**: Read `phases/phase-3-conversion.md` → mechanical format conversion (skip if already markdown/structured)
4. **Phase 4 — Profiling & Decomposition**: Read `phases/phase-4-profiling-decomposition.md` and `references/concept-types.md` and `references/confidence-framework.md` → AI-driven comprehension and decomposition
   - **Pause**: "Here's the decomposition — [N] concepts across [M] hierarchy levels. Does this look right?"
5. **Phase 5 — Recipe Capture**: Read `phases/phase-5-recipe-capture.md` → document the full conversion recipe
6. **Phase 6 — Validation**: Read `phases/phase-6-validation.md` and `references/validation-prompt.md` → cross-model adversarial review
   - **Pause**: "Here are the validation findings. Do you want to review any corrections?"
7. **Phase 7 — Export & Contribution**: Read `phases/phase-7-export-contribution.md` and `references/license-handling.md` and `references/output-formats.md` → deliver outputs, guide storage, offer contribution path
   - **Pause**: "Here are your outputs. Would you like to contribute the recipe back to SecID?"

### Option 2: Specific Phase

The user already has work done and wants to jump to a specific phase. Common entry points:

- "I have clean markdown" → start at Phase 4
- "I have structured JSON already" → start at Phase 4 for verification, or Phase 5 for recipe capture
- "I just want to check if SecID has this" → Phase 1 only

Ask which phase, then read that phase file and proceed from there.

### Option 3: Continue Previous Work

The user has a partial ingestion from a prior session. Ask them what they have so far and which phase to resume from.

## Key Rules

1. **User's data is default** — if the user provided a file and SecID has a match, inform them but use their file unless they choose otherwise
2. **Processing is never blocked by license** — only contribution advice is gated by license (Phase 7)
3. **Recipe is a first-class output** — every ingestion produces a recipe alongside the data
4. **Never auto-contribute** — always ask, never push/file/register on the user's behalf. Offer to draft issues.
5. **Tag AI decompositions with confidence** — every AI-produced classification and decomposition decision carries a confidence level. Use `references/confidence-framework.md`.
6. **Blocklist is a hard stop for contribution only** — ISO, IEEE, HITRUST, PCI-DSS full text cannot be contributed. Processing for local use is fine. Recipes can always be contributed.
7. **Storage guidance is a nudge** — recommend good practices (version-controlled repo), don't enforce

## Important

- **Never silently skip content** — if you can't process something (malformed table, image-only page), say so and ask the user
- **Preserve source identifiers exactly** — use the IDs the source uses, don't normalize or rename
- **Pause between phases** — let the user review, correct, and add domain knowledge
- **Structured input is better** — if the user provides raw PDF when structured data exists, note that structured data produces faster, more reliable results. But always respect their choice.

## Feedback and Bug Reports

This plugin is under active development. If the user encounters a bug, error, problem, flaw, unexpected behavior, confusion, or has a feature request, idea, or any feedback at all — let them know they can file an issue. Read `../../FEEDBACK.md` for the full instructions, and share the link with them:

https://github.com/CloudSecurityAlliance/csa-plugins-official/issues

Mention this proactively if something goes wrong, produces an unexpected result, or if the user seems stuck or frustrated. Also mention it at the end of a completed ingestion as an invitation to share their experience.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion/SKILL.md
git commit -m "Add SKILL.md entry point for security-knowledge-ingestion

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Register in marketplace.json and README.md

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`

- [ ] **Step 1: Add plugin to marketplace.json**

Add a new entry to the `plugins` array in `.claude-plugin/marketplace.json`, after the cwe-analysis entry:

```json
    {
      "name": "security-knowledge-ingestion",
      "description": "Ingest security knowledge documents (standards, regulations, frameworks, controls, capabilities) into structured, machine-readable data. Checks SecID for existing structured data, handles license verification for contributions, produces reproducible conversion recipes, and guides users toward proper data management.",
      "author": {
        "name": "Cloud Security Alliance",
        "email": "research@cloudsecurityalliance.org"
      },
      "source": "./plugins/security-knowledge-ingestion",
      "category": "security",
      "homepage": "https://github.com/CloudSecurityAlliance/csa-plugins-official/tree/main/plugins/security-knowledge-ingestion"
    }
```

- [ ] **Step 2: Validate marketplace.json**

```bash
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
```

Expected: No output (valid JSON).

- [ ] **Step 3: Add to README.md Available Plugins table**

Find the Available Plugins table in README.md and add a row for security-knowledge-ingestion. The exact edit depends on the table format — add after the cwe-analysis row:

```
| security-knowledge-ingestion | Ingest security knowledge documents into structured data with reproducible recipes and SecID integration | Security |
```

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json README.md
git commit -m "Register security-knowledge-ingestion in marketplace and README

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Add design spec to repo

**Files:**
- Verify: `docs/superpowers/specs/2026-04-02-security-knowledge-ingestion-design.md` (already created)

- [ ] **Step 1: Verify spec exists**

```bash
ls -la docs/superpowers/specs/2026-04-02-security-knowledge-ingestion-design.md
```

Expected: File exists.

- [ ] **Step 2: Commit spec if not already committed**

```bash
git add docs/superpowers/specs/2026-04-02-security-knowledge-ingestion-design.md
git add docs/superpowers/plans/
git commit -m "Add design spec and plans for security-knowledge-ingestion

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Validate and push

**Files:** None (validation only)

- [ ] **Step 1: Validate all JSON**

```bash
python3 -m json.tool plugins/security-knowledge-ingestion/plugin.json > /dev/null
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
```

Expected: No output for both.

- [ ] **Step 2: Check plugin.json description matches marketplace.json**

```bash
python3 -c "
import json
p = json.load(open('plugins/security-knowledge-ingestion/plugin.json'))
m = json.load(open('.claude-plugin/marketplace.json'))
me = [x for x in m['plugins'] if x['name'] == 'security-knowledge-ingestion'][0]
print('Match' if p['description'] == me['description'] else 'MISMATCH')
print('plugin.json:', p['description'][:80])
print('marketplace:', me['description'][:80])
"
```

Expected: "Match"

- [ ] **Step 3: Check for placeholders**

```bash
rg -n 'TODO|TBD|FIXME' plugins/security-knowledge-ingestion/
```

Expected: No matches.

- [ ] **Step 4: Verify directory structure**

```bash
find plugins/security-knowledge-ingestion -type f | sort
```

Expected: plugin.json, FEEDBACK.md, LICENSE, SKILL.md

- [ ] **Step 5: Push and create PR**

```bash
git push -u origin plugin/security-knowledge-ingestion
```

```bash
gh pr create --title "Add security-knowledge-ingestion plugin skeleton" --body "$(cat <<'EOF'
## Summary

Plugin skeleton for security-knowledge-ingestion — converts security knowledge documents into structured, machine-readable data with reproducible recipes and SecID integration.

This PR creates the installable plugin with SKILL.md routing. Phase files, reference materials, and validation script will follow in subsequent PRs (Plans 2-4).

## What's included

- `plugin.json` — plugin manifest
- `SKILL.md` — entry point with progressive disclosure, 7-phase workflow, three entry points (full/specific/continue), automation spectrum, teaching mode
- `FEEDBACK.md` + `LICENSE` (Apache 2.0)
- Registered in marketplace.json and README.md
- Design spec in `docs/superpowers/specs/`

## What's NOT included (coming in Plans 2-4)

- Phase files (7 phases)
- Reference materials (7 reference docs)
- `validate-decomposition.sh` script

## Test plan

- [x] plugin.json valid JSON
- [x] marketplace.json valid JSON
- [x] Descriptions match between plugin.json and marketplace.json
- [x] No TODO/TBD/FIXME in plugin files
- [x] Directory structure follows csa-plugins-official conventions

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 6: Do not merge — leave for review**
