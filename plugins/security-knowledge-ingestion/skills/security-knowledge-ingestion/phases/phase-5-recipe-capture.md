# Phase 5: Recipe Capture

## Purpose

Document the full conversion recipe so this ingestion can be reproduced. The recipe is a first-class output — as important as the structured data itself.

## Why Recipes Matter

Without a recipe, every ingestion is a one-off. When the standard updates (CCM 4.1 → 4.2, NIST CSF 2.0 → 2.1), someone has to figure out the process from scratch. With a recipe, they run the same steps, diff the output, and handle what changed.

Recipes also enable:
- **Community contribution**: Others can verify your work by reproducing it
- **Error correction**: If someone finds a mistake, they can trace it to the specific step that produced it
- **Version tracking**: The recipe documents exactly which tools and prompts produced which output

## Steps

### Step 1: Compile the Recipe

Gather information from all prior phases into a single document:

```markdown
# Ingestion Recipe: {Document Title} {Version}

## Source
- **Title**: {full title}
- **Publisher**: {organization}
- **Version**: {version/revision/edition}
- **Source URL**: {where to get the original document}
- **Date retrieved**: {when you got it}
- **SecID**: {secid string, if known}

## Input
- **Format provided**: {PDF, DOCX, HTML, markdown, JSON, etc.}
- **File characteristics**: {page count, file size, notable features}

## Conversion (Phase 3)
- **Tool**: {tool name and version, e.g., "marker-pdf 0.3.2"}
- **Command**: {exact command used}
- **Cleaning**: {what was removed and why}
- **Manual corrections**: {any hand-fixes applied}
- **Known issues**: {conversion artifacts, lost content, etc.}

## Profiling & Decomposition (Phase 4)
- **Document type**: {classification and confidence}
- **Hierarchy**: {levels identified, e.g., "3 levels: Functions → Categories → Subcategories"}
- **Concept types**: {what was found}
- **Concepts extracted**: {total count, breakdown by level}
- **Prompts used**: {exact prompt text, or reference to a versioned prompt}
- **Decisions made**:
  - {decision 1 and rationale}
  - {decision 2 and rationale}
  - ...

## Source-Specific Quirks
- {anything unusual about this document that future processors should know}
- {e.g., "Table on page 12 is malformed in the PDF — columns are merged"}
- {e.g., "Controls IAM-14 through IAM-16 are new in v4.1, not present in v4.0"}
- {e.g., "Article numbering restarts in each Title — Art. 1 appears multiple times"}

## Validation Checks
- {checks to run on the output to verify correctness}
- {e.g., "Should have exactly 207 controls"}
- {e.g., "Every control should have a parent domain"}
- {e.g., "No duplicate IDs"}

## Version Update Notes
- {what to watch for when the next version is released}
- {e.g., "Check for renamed domains — v4.0 had IVS, v4.1 renamed to I&S"}
- {e.g., "New articles may be added between existing ones — check numbering"}
```

### Step 2: Review with User

Present the recipe summary:

> "Here's the conversion recipe — it documents every step so this can be reproduced. Does anything look incomplete or incorrect?"

The recipe should be understandable by someone who wasn't present during the ingestion.

### Step 3: Save

Save the recipe alongside the structured data output. Use a consistent naming convention:

- `{document-name}-recipe.md` (e.g., `nist-800-53-r5-recipe.md`)
- Or follow the DataSets repo convention if the user is using that: `PROCESSING-NOTES.md`

## Output

A standalone recipe document (markdown) that contains everything needed to reproduce this ingestion.
