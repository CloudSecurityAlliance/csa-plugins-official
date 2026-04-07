---
title: "NIST IR 8477 Mapping Plugin"
document-status: DRAFT
date: 2026-04-06
author: "Kurt Seifried + AI assistance"
status: "Decided"
type: "Design spec"
tags:
  - plugin
  - nist-ir-8477
  - mapping
  - relationship-styles
  - crosswalk
  - supportive
  - set-theory
  - structural
builds-on:
  - docs/superpowers/specs/2026-04-02-security-knowledge-ingestion-design.md
---

# NIST IR 8477 Mapping Plugin — Design Spec

## Summary

A Claude Code plugin for the CSA marketplace that maps relationships between security knowledge sources using the NIST IR 8477 methodology. Supports four relationship styles (crosswalk, supportive, set theory, structural), guided use case documentation, cross-model validation, and multiple output formats.

**Plugin name**: `nist-ir-8477-mapping`

**Marketplace**: `CloudSecurityAlliance/csa-plugins-official`

**Install**: `/plugin install nist-ir-8477-mapping@csa-plugins-official`

## Motivation

NIST IR 8477 defines a rigorous methodology for characterizing relationships between concepts in security knowledge. It's the clearest external specification for mapping and produces NIST-compatible outputs (OLIR/CPRT). This plugin makes the methodology executable — guiding users through use case documentation, style selection, relationship evaluation, and validated export.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Single plugin vs four | Single plugin with style selection | NIST treats the four styles as options within one methodology that compose together |
| Use case before mapping | Mandatory Phase 2 | NIST §3 requires documented assumptions before any mapping. No exceptions. |
| Sample before full run | Phase 4 maps sample first, Phase 5 reviews, then Phase 4 completes | NIST §5 recommends representative sample review before full mapping. True quality gate, not post-hoc audit. |
| Prompts in files | All prompts in references/, loaded at runtime | Avoids hardcoded prompts, enables editing without touching scripts. Lesson from security-knowledge-ingestion review. |
| Output formats | Rich internal + OLIR/CPRT JSON + Excel + claims-based + markdown | One rich representation, multiple projections. JSON is canonical lossless. |
| Style-specific phase files | Loaded on demand based on Phase 3 selection | Progressive disclosure — don't load crosswalk instructions when doing set theory mapping |

## Plugin Structure

```
plugins/nist-ir-8477-mapping/
  plugin.json
  FEEDBACK.md
  LICENSE
  scripts/
    validate-mapping.sh
  skills/
    nist-ir-8477-mapping/
      SKILL.md
      phases/
        phase-1-intake.md
        phase-2-use-case-documentation.md
        phase-3-style-selection.md
        phase-4-mapping-execution.md
        phase-5-sample-review.md
        phase-6-validation.md
        phase-7-export.md
      styles/
        crosswalk.md
        supportive.md
        set-theory.md
        structural.md
      references/
        relationship-types.md
        style-selection-guide.md
        style-conversion.md
        quality-criteria.md
        confidence-framework.md
        validation-prompt.md
        output-formats/
          olir-cprt-format.md
          excel-format.md
          claims-format.md
          internal-format.md
```

## Phase Architecture

### Phase 1: Intake

**Purpose**: Load source(s) and establish mapping context.

**Two modes**:

**Exploratory mode (one source)**: The user has one source and wants to understand it before mapping. Profile the source (hierarchy, concept types, granularity), recommend what styles would work, suggest what kinds of sources would pair well with it, and run structural analysis (B4) to capture the hierarchy. Pauses with: "Here's what I found. When you have a second source, we can proceed with mapping."

Exploratory mode supports Phase 1 + partial Phase 2 (some use case assumptions can be documented with one source) + structural mapping (B4). Phases 3-7 require two sources.

**Mapping mode (two sources)**: Full mapping engagement. Proceed through all phases.

**Steps (mapping mode)**:
1. Accept two structured data files (JSON from security-knowledge-ingestion, SecID v2, or user-provided)
2. Verify each has: identified concepts, hierarchy, concept types
3. If not structured: suggest running security-knowledge-ingestion first
4. Establish roles: which is the focal document, which is the reference document
5. Summary: "Source A has N concepts (type: controls), Source B has M concepts (type: requirements). Ready to proceed?"

**Output**: Validated source file(s) with roles assigned (mapping mode) or source profile with recommendations (exploratory mode).

### Phase 2: Use Case Documentation

**Purpose**: Document the five NIST §3 assumptions before any mapping begins.

**Steps** (interactive — walk through each):
1. **Intended users**: Who will consume this mapping? What skills and knowledge do they have?
2. **Purpose**: Why would someone use this mapping? What question does it answer?
3. **Concept types**: What types of concepts are being mapped from each source?
4. **Direction**: A→B, B→A, or both? Many mappings have an obvious direction.
5. **Exhaustiveness**: Strongest-direct-only (recommended) or exhaustive? "Mapping indirect or tenuous relationships would create so many mappings that they would lose their value." [NIST §3]

**Output**: Use case document with all five assumptions explicitly stated. Carried forward through all subsequent phases.

### Phase 3: Style Selection

**Purpose**: Recommend which relationship style(s) to use based on the documented use case.

**Steps**:
1. Apply NIST §4 Table 2 selection logic (loaded from `references/style-selection-guide.md`)
2. Present recommendation with rationale
3. May recommend multiple styles (NIST §4.6 supports composing styles). When multiple styles are selected, composition follows these rules:
   - **Deduplication**: Same concept pair appearing in multiple styles — keep all, tagged by style
   - **Style conversion**: Set theory relationships can convert to supportive equivalents (except "intersects with") per the conversion table in `references/style-conversion.md`
   - **Richer-wins**: When both a crosswalk and a typed relationship exist for the same pair, the typed relationship is primary; the crosswalk is redundant
4. User confirms or overrides
5. Load the appropriate style file(s) from `styles/` — only the selected style(s)

**Selection logic**:

| Situation | Recommended Style |
|-----------|------------------|
| Pointing to additional information, exploratory draft, diverse concept types | Crosswalk |
| Similar concept types, or different but strongly related types | Supportive |
| Comparing similar concept sets, especially version-to-version | Set Theory |
| Capturing hierarchy within a single source | Structural |

**Output**: Selected style(s) with rationale. Style reference file(s) loaded into context.

### Phase 4: Mapping Execution (Sample)

**Purpose**: Map a representative sample of concept pairs to validate the approach before committing to a full run.

**Steps** (vary by style — detailed instructions in `styles/*.md`):
1. Select a representative sample (10-20 concept pairs spanning different areas of both sources)
2. For each concept pair in the sample:
   - Evaluate the relationship using the selected style's types
   - Assign a relationship type (and rationale for set theory, properties for supportive)
   - Document justification: why this type, what evidence from both sources
   - Tag with confidence level
3. Document "no relationship" findings — pairs considered but found unrelated
4. Capture source observations: ambiguities, granularity issues, duplications, wording problems
5. Record prompts used for the recipe

**Output**: Sample mapping (10-20 pairs) with typed, justified relationships. Proceed to Phase 5 for review.

### Phase 5: Sample Review

**Purpose**: Quality gate — review the sample mapping before committing to the full run. Per NIST §5: "Have other SMEs review the sample and the use case documentation, and provide feedback."

**Steps**:
1. Present the sample with full justification for each pair
2. Check for:
   - Consistency: are similar pairs getting similar treatments?
   - Style drift: has the interpretation of relationship types shifted during the mapping?
   - Exhaustiveness drift: are tenuous relationships creeping in?
   - Directionality errors: is A→B being confused with B→A?
   - Missing "no relationship": were unrelated pairs considered and documented?
   - Use case alignment: does the sample serve the documented purpose and audience?
3. User reviews and provides feedback
4. If issues found: adjust approach and re-run sample (return to Phase 4)
5. If approved: proceed to Phase 4b (full run)

**Output**: Approved sample, confirmed approach. Triggers full mapping run.

### Phase 4b: Mapping Execution (Full Run)

**Purpose**: Complete the full mapping using the validated approach from the sample.

**Steps**:
1. Apply the same approach validated in Phase 4/5 to all remaining concept pairs
2. Same per-pair process: evaluate, assign type, document justification, tag confidence
3. Include the sample pairs already mapped (don't redo them)
4. Continue capturing source observations

**Automation spectrum** (applies to this phase):
- **Interactive**: Present each concept pair, discuss, assign together
- **Semi-automated**: Batch process, pause periodically for review
- **Fully automated**: Process all pairs, present results

**Output**: Complete mapping with typed, justified relationships for all evaluated concept pairs.

### Phase 6: Cross-Model Validation

**Purpose**: Adversarial review of mapping quality by independent AI models.

**Steps**:
1. Check tool availability (codex, gemini CLIs)
2. Run `scripts/validate-mapping.sh` with mapping output + source files
3. Prompt loaded from `references/validation-prompt.md` (not hardcoded)
4. Targets mapping-specific errors:
   - Relationship type misclassification (e.g., "supports" vs "is supported by")
   - Rationale inconsistency (set theory: using syntactic rationale but interpreting meaning)
   - Directionality errors
   - Exhaustiveness drift (mapping tenuous relationships when use case said strongest-only)
   - Missing "no relationship" documentation
   - Property misassignment (supportive: "example of" vs "integral to")
5. Synthesize findings, present to user

**Skip condition**: No external AI tools → skip with note, proceed to export.

**Output**: Validated mapping, validation report.

### Phase 7: Export

**Purpose**: Generate outputs in multiple formats from the rich internal representation.

**Formats** (JSON is canonical lossless; others are projections):
1. **Rich internal JSON**: Full evidence, justifications, citations, reasoning chain, confidence, provenance
2. **OLIR/CPRT-compatible JSON**: NIST submission format — concept pairs with relationship types
3. **Excel**: Spreadsheet with one row per concept pair, columns for relationship type, rationale, justification
4. **Claims-based format**: Knowledge graph claims with directional edges, perspective, evidence
5. **Markdown report**: Human-readable summary with statistics, notable findings, source observations

**Output**: Files in user's chosen format(s), plus the rich internal JSON always.

## Style Files

Each style file in `styles/` is loaded on demand when that style is selected in Phase 3. Contains:

- Complete relationship type definitions with examples
- Step-by-step evaluation guidance for that style
- Common pitfalls specific to the style
- How to document "no relationship" in this style

| File | Style | Key Content |
|------|-------|-------------|
| `crosswalk.md` | B1 | No types — just pairs. Use case documentation is the only context. |
| `supportive.md` | B2 | 6 types (supports, is supported by, identical, equivalent, contrary, no relationship) + 3 properties (example of, integral to, precedes) |
| `set-theory.md` | B3 | 3 rationales (syntactic, semantic, functional) × 5 types (subset, intersects, equal, superset, no relationship). Rationale + type inseparable. |
| `structural.md` | B4 | Parent-child only. Single-source. Fully objective. |

## Reference Materials

| File | Purpose |
|------|---------|
| `relationship-types.md` | All 4 styles in one reference — complete types, properties, definitions |
| `style-selection-guide.md` | NIST §4 Table 2 selection logic with decision tree |
| `style-conversion.md` | Set theory ↔ supportive conversion table, intersects-with caveat |
| `quality-criteria.md` | Good vs bad mapping characteristics from NIST IR 8477 |
| `confidence-framework.md` | Confidence levels for mapping decisions |
| `validation-prompt.md` | Cross-model review prompt (loaded by script at runtime) |
| `output-formats/olir-cprt-format.md` | NIST OLIR/CPRT submission format |
| `output-formats/excel-format.md` | Excel spreadsheet layout |
| `output-formats/claims-format.md` | Knowledge graph claims format |
| `output-formats/internal-format.md` | Rich internal JSON schema |

## Validation Script

`scripts/validate-mapping.sh`:
- Loads prompt from `references/validation-prompt.md` (not hardcoded)
- Accepts: mapping output JSON + optional source files (focal + reference documents). When source files are omitted, the validation report explicitly flags reduced confidence: "Validated without source documents — completeness and relationship accuracy checks have reduced confidence."
- Uses temp files, pipes via stdin (no arg-size limits)
- Runs available models in parallel
- Exits 0 when skipped (no validators installed), 1 only when validators fail

## SKILL.md Behavior

### Workflow Entry Points

1. **Full workflow** — all 7 phases
2. **Specific phase** — e.g., "I have a use case, start at style selection"
3. **Continue previous** — resume from a prior session

### Teaching Mode

On by default. Explains relationship types, why use cases matter, how style selection works. "Skip teaching" / "expert mode" suppresses.

### Automation Spectrum

- **Interactive**: Pause between phases, evaluate pairs together
- **Semi-automated**: Batch process phases 1-4, pause at sample review
- **Fully automated**: Run everything, present final output + validation

### Key Rules

1. **Methodology fidelity** — NIST IR 8477 exactly as published, no invented types
2. **Use case before mapping** — Phase 2 must complete before Phase 4
3. **Rationale for every relationship** — per NIST §5
4. **"No relationship" is a valid, documented result** — not a gap to fill
5. **Sample before full run** — Phase 5 catches systematic errors early
6. **Source observations are first-class** — ambiguities found during mapping are captured
7. **Prompts in files** — all prompts in references/, loaded at runtime, never hardcoded

### Degraded Mode

- **SecID MCP not available**: Skip SecID enrichment, work with user-provided files only
- **Input not structured**: This plugin requires structured input. Suggest running the security-knowledge-ingestion plugin first to convert raw documents.
- **Validation tools not available** (codex, gemini CLIs): Skip Phase 6 with note, proceed to export

## Relationship to Other Plugins

```
security-knowledge-ingestion          nist-ir-8477-mapping
(Plugin 1)                            (this plugin)

Structured source A ──────────────►   Phase 1: Intake
Structured source B ──────────────►   (two structured inputs)
                                      Phase 2-6: Map + validate
                                      Phase 7: Export
                                        ├─► OLIR/CPRT JSON
                                        ├─► Excel
                                        ├─► Claims-based
                                        └─► Markdown report
```

Independent — users can use either alone. This plugin just needs structured input; it doesn't care how it was produced.

## Open Questions

1. **How large can a mapping get before batch processing is impractical?** Two 200-control frameworks = 40,000 directional pairs. Need to determine practical limits and chunking strategy.
2. **Should the plugin support resumable mappings?** Large mappings may span multiple sessions. The rich internal format could support checkpointing.
3. **OLIR submission format details**: The OLIR/CPRT export is best-effort based on published examples in IR 8477 and the OLIR repository. Exact schema to be confirmed against NIST's current submission requirements. The rich internal JSON is always produced regardless.
