---
title: "Security Knowledge Ingestion Plugin"
document-status: DRAFT
date: 2026-04-02
author: "Kurt Seifried + AI assistance"
status: "Decided"
type: "Design spec"
tags:
  - plugin
  - ingestion
  - security-knowledge
  - secid
  - standards
  - frameworks
---

# Security Knowledge Ingestion Plugin — Design Spec

## Summary

A Claude Code plugin for the CSA marketplace that ingests security knowledge documents (standards, regulations, frameworks, controls, capabilities, best practices) into structured, machine-readable data. Produces reproducible conversion recipes alongside the data. Integrates with SecID for discovery and contribution.

**Plugin name**: `security-knowledge-ingestion`

**Marketplace**: `CloudSecurityAlliance/csa-plugins-official`

**Install**: `/plugin install security-knowledge-ingestion@csa-plugins-official`

## Motivation

Security knowledge lives in PDFs, Word docs, HTML pages, and spreadsheets. Converting these into structured data that AI agents and mapping tools can consume is manual, undocumented, and unreproducible. The DataSets repo has conversion tools but no orchestration layer. SecID can identify and locate security knowledge but needs structured data contributions to serve.

This plugin bridges the gap: take a document, produce structured data + the recipe that created it, and guide users toward contributing both back to the community.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| License check timing | At contribution time (Phase 7), not at processing time | User provided the data — processing is never blocked. License only matters for redistribution. |
| SecID data as default | No — user's data is default, SecID is suggested | User provided a file, respect that. Inform them SecID has a match, let them choose. |
| Recipe as output | First-class, alongside the data | Reproducible builds for security knowledge. Enables version updates, community contribution, and error correction. |
| Blocklist scope | Major known items + always ask | Hard stop for ISO, IEEE, HITRUST, PCI-DSS full text. For everything else, find and confirm the license before advising on contribution. |
| Phase count | 7 phases, progressive disclosure | Each phase is focused and skippable. Mirrors pipeline stages 1-3. |
| Cross-model validation | Same pattern as incident-analysis | Codex/Gemini adversarial review catches decomposition errors. |

## Plugin Structure

```
plugins/security-knowledge-ingestion/
  plugin.json
  FEEDBACK.md
  LICENSE
  scripts/
    validate-decomposition.sh          # Cross-model validation script
  skills/
    security-knowledge-ingestion/
      SKILL.md                          # Entry point, progressive disclosure
      phases/
        phase-1-source-identification.md
        phase-2-acquisition.md
        phase-3-conversion.md
        phase-4-profiling-decomposition.md
        phase-5-recipe-capture.md
        phase-6-validation.md
        phase-7-export-contribution.md
      references/
        secid-integration.md
        concept-types.md
        datasets-convention.md
        output-formats.md
        confidence-framework.md
        validation-prompt.md
        license-handling.md
```

## Phase Architecture

### Phase 1: Source Identification

**Purpose**: Understand what the user has and check if SecID already knows about it.

**Steps**:
1. Identify the document: title, publisher, version, document type
2. Construct a candidate SecID (e.g., `secid:control/nist.gov/800-53@r5`)
3. Check SecID v2: does it have structured data for this?
4. If SecID has it: "FYI, SecID has a pre-structured version of this (same version, same source). Would you prefer to use that instead, or continue with your file?" User chooses. Their file is the default.
5. If SecID has the recipe but not data: inform user they can reproduce/verify
6. If SecID doesn't know about it: note this for Phase 7 contribution nudge

**SecID tools used**: `resolve`, `describe`

**Output**: Document identification record (title, publisher, version, type, SecID status)

### Phase 2: Acquisition

**Purpose**: Get the data into a workable state.

**Steps**:
1. Determine what the user provided: local file, URL, SecID reference, already-structured data
2. If URL: fetch the content
3. If SecID v2 reference (user chose SecID in Phase 1): retrieve structured data + recipe
4. Determine format: PDF, DOCX, HTML, markdown, CSV, JSON
5. Route based on format:
   - Already structured (JSON/CSV with concepts identified) → skip to Phase 4 for verification
   - Pre-processed markdown → skip to Phase 4
   - Raw document → continue to Phase 3

**Output**: Raw document in workable format, format classification

### Phase 3: Conversion

**Purpose**: Mechanical format conversion. Tool-driven, not AI-driven.

**Steps**:
1. Convert to markdown: PDF→MD (marker), DOCX→MD (pandoc/custom), HTML→MD (custom)
2. Clean: strip headers, footers, navigation, page numbers, boilerplate, non-content
3. Record exactly which tools and commands were used (version numbers)
4. Produce clean markdown

**Tools**: References existing DataSets repo tools (`tools-resources/utils/`) where applicable. Not bundled — user installs or provides.

**Output**: Clean markdown, tool log for recipe

**Skip condition**: Already markdown or structured → skip this phase entirely

### Phase 4: Profiling & Decomposition

**Purpose**: AI-driven comprehension. This is where the document is understood.

**Steps**:
1. **Profile**: Classify the document type (standard, regulation, framework, guidance, benchmark, best practice)
2. **Identify hierarchy**: Flat list, tree, articles/sections/chapters, domains/controls/enhancements
3. **Identify concept types**: Controls, requirements, outcomes, capabilities, recommendations, etc.
4. **Decompose**: Break into individually addressable concepts, each with:
   - Identifier (as used in the source)
   - Title/name
   - Full text/description
   - Concept type
   - Position in hierarchy (parent, level)
   - Metadata (applicability, notes, cross-references within the source)
5. **Tag with confidence**: Every AI-produced classification and decomposition decision carries a confidence level
6. Record the prompts used (version, exact text)

**Pause**: "Here's the decomposition — [N] concepts across [M] hierarchy levels. Does this look right? Anything missing or miscategorized?"

**Output**: Structured JSON/YAML with all concepts, hierarchy, and metadata

### Phase 5: Recipe Capture

**Purpose**: Document the full conversion recipe so this can be reproduced.

**Steps**:
1. Compile the recipe from all prior phases:
   - Source URL (where the content lives)
   - Source document metadata (title, publisher, version, date)
   - Tools and versions used (Phase 3)
   - Prompts used with exact text and version (Phase 4)
   - Conversion steps in order
   - Decisions made and why (e.g., "merged sections 3.1 and 3.2 because they define one concept")
   - Source-specific quirks (e.g., "table on page 12 is malformed, manually corrected")
   - Validation checks to run on output
   - What to watch for on next version update
2. Format as a standalone reproducible document

**Output**: Recipe document (markdown with structured sections)

### Phase 6: Validation

**Purpose**: Cross-model adversarial review of decomposition quality.

**Steps**:
1. Check tool availability (codex CLI, gemini CLI)
2. If available: run `validate-decomposition.sh` with structured output + source excerpts
3. Review prompt targets these error patterns:
   - **Completeness**: Missing concepts from the source
   - **Phantom concepts**: Concepts created that don't exist in the source
   - **Merging errors**: Two distinct concepts merged into one
   - **Splitting errors**: One concept split into multiple
   - **Hierarchy accuracy**: Parent-child structure matches source
   - **Metadata accuracy**: Types, IDs, descriptions faithful to source
   - **Boundary accuracy**: Concept boundaries drawn where the source draws them
4. Synthesize: agreements between models are high-confidence findings
5. Present findings to user, apply corrections

**Pause**: "Here are the validation findings. Do you want to review any corrections before finalizing?"

**Skip condition**: No external AI tools available → skip with note, recommend installing

**Output**: Validated structured data, validation report

### Phase 7: Export & Contribution

**Purpose**: Deliver outputs and guide toward good practices.

**Steps**:
1. **Export structured data** in user's preferred format:
   - Structured JSON (primary — concepts, hierarchy, metadata)
   - YAML-frontmatter markdown (Obsidian-compatible)
   - CSV (one row per concept)
   - DataSets repo format (if user wants that convention)
2. **Export recipe** alongside the data
3. **Storage guidance**: "Where are you storing this? We recommend a version-controlled repo. Here's how CSA does it." Point to DataSets convention reference.
4. **Contribution (for content not already in SecID)**:
   a. **License check** — happens here, not earlier:
      - Blocklist check: ISO, IEEE, HITRUST, PCI-DSS full text → "This is licensed content. The structured data can't be contributed to SecID for public serving. You can still file the recipe (prompts, tools, steps) — just not the structured content."
      - Ask user: "Can you provide the license, or should I look for it at the source URL?"
      - Find and present the license. User confirms.
      - Open/permissive → proceed with contribution guidance
      - Licensed/unknown → "You can use this locally, but we can't recommend contributing it for public redistribution. You can still file the recipe (prompts, tools, steps) — just not the structured content."
   b. **Contribution nudge**: "Want to help the community? File an issue at SecID with the source URL, recipe, and tools used. The SecID team will evaluate for inclusion."
   c. **Offer to draft the issue** — never auto-file
5. Never auto-push, auto-register, or auto-contribute anything

**Output**: Structured data files, recipe document, optional draft issue

## Reference Materials

| File | Purpose |
|------|---------|
| `secid-integration.md` | How to use SecID MCP tools (resolve, lookup, describe). How SecID v2 serves data + recipes. When to check, how to interpret responses. |
| `concept-types.md` | Controls, requirements, outcomes, capabilities, recommendations, technologies, functions, processes, techniques, roles, skills. Aligned with NIST IR 8477 definitions. How to identify which types a document contains. |
| `datasets-convention.md` | CSA DataSets repo format explained with examples: README.json, document.md, document-processed.md, document.csv, document.json, PROCESSING-NOTES.md. Template for users to follow or adapt. |
| `output-formats.md` | Structured JSON schema, YAML-frontmatter markdown, CSV layout, DataSets repo format. |
| `confidence-framework.md` | Confidence levels for AI-produced decompositions. How certain is the classification, hierarchy identification, and concept decomposition? |
| `validation-prompt.md` | The structured review prompt sent to Codex/Gemini. Targets: completeness, phantoms, merging, splitting, hierarchy, metadata, boundaries. |
| `license-handling.md` | Blocklist (ISO, IEEE, HITRUST, PCI-DSS, etc.). How to find licenses at source URLs. Three outcomes: open → contribute data + recipe; licensed → recipe only; unknown → local use, flag for contribution. |

## Validation Script

`scripts/validate-decomposition.sh` follows the same pattern as incident-analysis's `validate-report.sh`:

- Takes path to structured output file as argument
- Checks for codex/gemini CLI availability
- Sends structured output + review prompt to available models in parallel
- Saves reviews as `<filename>.codex-review.md` / `<filename>.gemini-review.md`
- Exit 0 if at least one review succeeded

The review prompt is stored in `references/validation-prompt.md` and embedded in the script.

## SKILL.md Behavior

### Workflow Entry Points

1. **Full workflow** — walk through all 7 phases
2. **Specific phase** — jump to a phase (e.g., user has clean markdown, start at Phase 4)
3. **Continue previous** — resume from where a prior session left off

### Teaching Mode

On by default. Explains what each phase does, why concept types matter, how hierarchy identification works. "Skip teaching" or "expert mode" suppresses explanations.

### Automation Spectrum

- **Interactive**: Pause between every phase, teach as you go
- **Semi-automated**: Run phases 1-5 with minimal pauses, stop at validation
- **Fully automated**: Run everything, present final output + validation results

User's choice, communicated at the start.

### Key Rules

1. **User's data is default** — SecID match is suggested, not imposed
2. **Processing is never blocked by license** — only contribution is
3. **Recipe is a first-class output** — every ingestion produces one
4. **Never auto-contribute** — always ask, never push/file/register
5. **Tag AI decompositions with confidence** — label AI work as AI work
6. **Blocklist is a hard stop for contribution** — but not for processing
7. **Storage guidance is a nudge** — recommend good practices, don't enforce

## Relationship to Other Plugins

```
security-knowledge-ingestion          nist-ir-8477-mapping (future)
(this plugin)                         (separate plugin)

Structured data ──────────────────►   Input: two structured sources
Recipe ───────────────────────────►   (references recipe for provenance)
SecID contribution (via issue) ──►   SecID lookup for concept metadata
```

The ingestion plugin produces what the mapping plugin consumes. They're independent — users can use either alone.

## Open Questions

1. **Should the plugin bundle any conversion tools?** Currently references external tools (marker, pandoc). Bundling adds size but removes setup friction. Recommendation: don't bundle for v1, document prerequisites.
2. **Recipe format standardization**: Should recipes follow a specific schema, or is freeform markdown sufficient for v1? Recommendation: freeform markdown for v1, schema when patterns stabilize.
3. **SecID v2 recipe format**: When SecID v2 launches, what format does it serve recipes in? The plugin should consume whatever SecID produces. Coordinate with SecID team.
