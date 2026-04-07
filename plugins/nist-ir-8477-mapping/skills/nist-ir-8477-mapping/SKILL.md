---
name: nist-ir-8477-mapping
description: Map relationships between security knowledge sources using the NIST IR 8477 methodology. Supports four relationship styles (crosswalk, supportive, set theory, structural), guided use case documentation, and validated export. Use when the user wants to map between two security frameworks, standards, or regulations, compare versions of the same standard, or explore what mapping approaches suit a particular source.
---

# NIST IR 8477 Mapping

You are guiding a user through mapping relationships between security knowledge sources using the NIST IR 8477 methodology. Your job is to help them document their use case, select the appropriate relationship style(s), evaluate concept pairs with documented justification, validate the results, and export in multiple formats.

## Scope

Mapping relationships between any security knowledge sources that have been decomposed into individually addressable concepts: standards (NIST, ISO, BSI), regulations (EU AI Act, GDPR), frameworks (CCM, CSF), controls, capabilities. Input must be structured data (JSON/CSV with identified concepts) — if the user has raw documents, suggest the `security-knowledge-ingestion` plugin first.

## How This Works

This skill uses **progressive disclosure**. This file provides the overview and workflow routing. Detailed instructions for each phase are in separate files under `phases/`. Style-specific mapping instructions are in `styles/`. Reference material is in `references/`. Read each file when you reach that phase — not before.

**File paths are relative to this SKILL.md's directory.**

## Teaching Mode

By default, you teach as you work — explain what relationship types mean, why use case documentation matters, how style selection works, what makes a good mapping versus a bad one. This helps users internalize the NIST IR 8477 methodology.

If the user says **"skip teaching"** or **"expert mode"**, suppress all teaching annotations. Produce only mapping output.

## Tool Access

1. **SecID MCP tools** — `resolve`, `lookup`, `describe` for enriching concept metadata during mapping
2. **File reading** — examine user-provided structured data files
3. **Bash** — run validation script when external AI tools are available

### Degraded Mode

- **SecID MCP not configured**: Skip SecID enrichment, work with user-provided files only. Inform user: "SecID tools aren't available — skipping enrichment. You can add SecID as a remote MCP server: `https://secid.cloudsecurityalliance.org/mcp`."
- **Input not structured**: This plugin requires structured input. Suggest: "Your input needs to be structured data with identified concepts. Try the `security-knowledge-ingestion` plugin to convert your document first."
- **Validation tools not installed** (codex, gemini CLIs): Skip Phase 6 with note. Proceed to export.

## Automation Spectrum

Ask the user how they want to work:

- **Interactive** — pause between phases, evaluate concept pairs together, teach as you go
- **Semi-automated** — batch process Phases 1-4, pause at sample review (Phase 5) for human judgment
- **Fully automated** — run everything, present final output + validation results for review

Default to interactive for first-time users.

## Workflow

Ask the user what they want to do:

### Option 1: Full Workflow (Two Sources)

Walk through all phases start to finish. Read each phase file as you reach it.

1. **Phase 1 — Intake**: Read `phases/phase-1-intake.md` → load two structured sources, assign roles
   - **Pause**: "Source A has N concepts, Source B has M concepts. Ready to proceed?"
2. **Phase 2 — Use Case Documentation**: Read `phases/phase-2-use-case-documentation.md` → document the five NIST §3 assumptions
   - **Pause**: "Here's the use case document. Does this capture your intent?"
3. **Phase 3 — Style Selection**: Read `phases/phase-3-style-selection.md` and `references/style-selection-guide.md` → recommend style(s)
   - **Pause**: "I recommend [style(s)] because [rationale]. Agree, or prefer something different?"
   - Load the selected style file(s) from `styles/`
4. **Phase 4 — Mapping Execution (Sample)**: Read `phases/phase-4-mapping-execution.md` and the selected `styles/*.md` → map a representative sample (10-20 pairs)
5. **Phase 5 — Sample Review**: Read `phases/phase-5-sample-review.md` → quality gate before full run
   - **Pause**: "Here's the sample. Does the approach look right before I map the rest?"
   - If issues: adjust and re-sample (return to Phase 4)
   - If approved: proceed to Phase 4b (full run)
6. **Phase 4b — Mapping Execution (Full Run)**: Complete all remaining concept pairs using the validated approach
7. **Phase 6 — Validation**: Read `phases/phase-6-validation.md` and `references/validation-prompt.md` → cross-model adversarial review
   - **Pause**: "Here are the validation findings. Review corrections before finalizing?"
8. **Phase 7 — Export**: Read `phases/phase-7-export.md` → generate outputs in chosen format(s)

### Option 2: Exploratory (One Source)

The user has one source and wants to understand what mapping approaches would work before finding a second source.

1. **Phase 1 — Intake (exploratory)**: Load and profile the single source
2. **Phase 2 — Use Case Documentation (partial)**: Document what's known — some assumptions need a second source
3. **Structural analysis**: Run B4 to capture the source's hierarchy
4. **Recommendations**: Suggest what kinds of sources would pair well, which styles would work

Pauses with: "When you have a second source, we can proceed with full mapping."

### Option 3: Specific Phase

The user has partial work and wants to jump in. Common entry points:

- "I have a use case documented" → start at Phase 3 (style selection)
- "I know I want set theory mapping" → start at Phase 4 (confirm use case, then map)
- "I have a completed mapping, validate it" → start at Phase 6

### Option 4: Continue Previous Work

The user has a partial mapping from a prior session. Ask what they have and which phase to resume.

## Key Rules

1. **Methodology fidelity** — implements NIST IR 8477 exactly as published. Do not invent relationship types, properties, or rationales not defined in the source document.
2. **Use case before mapping** — Phase 2 must complete before Phase 4. No exceptions. NIST §3.
3. **Rationale for every relationship** — per NIST §5, every relationship must have documented justification.
4. **"No relationship" is a valid, documented result** — pairs considered but found unrelated must be recorded, not silently skipped.
5. **Sample before full run** — Phase 4 maps a sample, Phase 5 reviews it as a quality gate, then Phase 4b completes the full mapping. This is the NIST-recommended approach.
6. **Source observations are first-class** — ambiguities, granularity issues, wording problems found during mapping are captured and reported.
7. **Prompts in files** — all prompts in references/, loaded at runtime, never hardcoded in scripts.
8. **Rationale + type are inseparable** (set theory only) — a relationship type without a rationale is invalid.

## Important

- **Never silently skip concept pairs** — if you can't evaluate a pair, say so and ask the user
- **Preserve source identifiers exactly** — use the IDs the sources use
- **Pause between phases** (interactive and semi-automated modes) — let the user review and correct. In fully automated mode, pauses are suppressed.
- **Direction matters** — A supports B is different from B supports A. Get it right.
- **Exhaustiveness is a choice** — don't map every tenuous relationship. Follow the use case's exhaustiveness setting.

## Feedback and Bug Reports

This plugin is under active development. If the user encounters a bug, error, problem, flaw, unexpected behavior, confusion, or has a feature request, idea, or any feedback at all — let them know they can file an issue. Read `../../FEEDBACK.md` for the full instructions, and share the link with them:

https://github.com/CloudSecurityAlliance/csa-plugins-official/issues

Mention this proactively if something goes wrong, produces an unexpected result, or if the user seems stuck. Also mention at the end of a completed mapping.
