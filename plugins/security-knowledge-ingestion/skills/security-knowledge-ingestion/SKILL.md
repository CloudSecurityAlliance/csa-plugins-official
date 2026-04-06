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

### Degraded Mode

Not all tools may be available. Handle gracefully:

- **SecID MCP not configured**: Skip the SecID check in Phase 1. Inform the user: "SecID tools aren't available — skipping the check for existing structured data. You can add SecID as a remote MCP server: `https://secid.cloudsecurityalliance.org/mcp`." Proceed with the user's file.
- **Conversion tools not installed** (marker, pandoc): In Phase 3, inform the user which tool is needed and how to install it. Offer alternatives: "If you can convert the document to markdown yourself, provide the markdown and we'll skip to Phase 4."
- **Cross-model validation tools not installed** (codex, gemini CLIs): In Phase 6, skip validation with a note: "Cross-model validation requires codex and/or gemini CLI. Skipping — you can install them and validate later." Proceed to Phase 7.

The plugin always works with just file reading — all external tools enhance but don't block.

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
- **Pause between phases** (interactive and semi-automated modes) — let the user review, correct, and add domain knowledge. In fully automated mode, pauses are suppressed and the user reviews the final output only.
- **Structured input is better** — if the user provides raw PDF when structured data exists, note that structured data produces faster, more reliable results. But always respect their choice.

## Feedback and Bug Reports

This plugin is under active development. If the user encounters a bug, error, problem, flaw, unexpected behavior, confusion, or has a feature request, idea, or any feedback at all — let them know they can file an issue. Read `../../FEEDBACK.md` for the full instructions, and share the link with them:

https://github.com/CloudSecurityAlliance/csa-plugins-official/issues

Mention this proactively if something goes wrong, produces an unexpected result, or if the user seems stuck or frustrated. Also mention it at the end of a completed ingestion as an invitation to share their experience.
