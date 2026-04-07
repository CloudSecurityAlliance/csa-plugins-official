# Phase 7: Export

## Purpose

Generate mapping outputs in multiple formats from the rich internal representation.

Read `references/output-formats/internal-format.md` for the canonical schema. Read the format-specific reference for each format the user requests.

## Formats

**JSON is the canonical lossless format.** All other formats are projections that may lose information.

| Format | Reference | Best For |
|--------|-----------|----------|
| Rich internal JSON | `references/output-formats/internal-format.md` | Complete record — always produced |
| OLIR/CPRT JSON | `references/output-formats/olir-cprt-format.md` | NIST submission |
| Excel | `references/output-formats/excel-format.md` | Human review, stakeholder communication |
| Claims-based | `references/output-formats/claims-format.md` | Knowledge graph, provenance tracking |
| Markdown report | (inline) | Quick summary, documentation |

## Steps

### Step 1: Always Produce Rich Internal JSON

This format contains everything: concept pairs, relationship types, rationale, justification, confidence, source observations, use case document, prompts used. It's the complete record of the mapping.

### Step 2: Ask User for Additional Formats

> "The rich internal JSON is saved. Which additional formats do you want?"

If the user doesn't have a preference, suggest:
- Excel for sharing with stakeholders
- OLIR/CPRT if they plan to submit to NIST
- Markdown report for quick human-readable summary

### Step 3: Generate Requested Formats

Each format is a projection of the internal JSON. Losses are noted:

- **OLIR/CPRT**: Drops justification detail, confidence, source observations. Keeps concept pairs + relationship types.
- **Excel**: One row per concept pair. Multi-value fields (cross-references) are semicolon-delimited. Nested metadata is flattened.
- **Claims-based**: Adds directional edge metadata, perspective/lens information, provenance chain. May expand the internal format rather than reduce it.
- **Markdown report**: Summary statistics, relationship type distribution, notable findings, source observations, use case document. Not a complete record — a human-readable overview.

### Step 4: Generate Markdown Report

Always include a markdown report (even if not explicitly requested) with:

1. **Use case summary** (from Phase 2)
2. **Style used** and rationale (from Phase 3)
3. **Statistics**: Total pairs evaluated, distribution by relationship type, confidence distribution
4. **Notable findings**: Surprising relationships, important "no relationship" findings
5. **Source observations**: Ambiguities, granularity issues, terminology problems found
6. **Validation summary** (from Phase 6, if performed)
7. **Methodology note**: "This mapping was produced using the NIST IR 8477 methodology. Relationship style: [style]. See use case document for assumptions and scope."

### Step 5: Save and Present

Save all output files. Present:

> "Mapping complete:
> - [N] concept pairs evaluated
> - [distribution by relationship type]
> - Outputs saved:
>   - [path to internal JSON]
>   - [path to additional formats]
>   - [path to markdown report]
>
> If you run into any issues or want to share feedback: https://github.com/CloudSecurityAlliance/csa-plugins-official/issues"

## Output

- Rich internal JSON (always)
- User-requested format(s)
- Markdown report (always)
