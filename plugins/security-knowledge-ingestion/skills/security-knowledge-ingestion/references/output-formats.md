# Output Formats

The plugin produces structured data in several formats. All formats contain the same information — they're projections of the same internal representation.

## JSON (Primary)

The default and most versatile format. Structure:

```json
{
  "metadata": {
    "title": "NIST SP 800-53 Revision 5",
    "publisher": "NIST",
    "version": "r5",
    "secid": "secid:control/nist.gov/800-53@r5",
    "document_type": "standard",
    "hierarchy_levels": ["family", "control", "enhancement"],
    "concept_count": 1189,
    "ingestion_date": "2026-04-02",
    "confidence": "High"
  },
  "concepts": [
    {
      "id": "AC-2",
      "title": "Account Management",
      "description": "The full text of the control...",
      "concept_type": "control",
      "hierarchy_level": "control",
      "parent_id": "AC",
      "metadata": {
        "baseline_impact": ["low", "moderate", "high"]
      },
      "cross_references": ["AC-3", "AC-6", "IA-2"],
      "confidence": "High"
    }
  ]
}
```

## YAML-Frontmatter Markdown (Obsidian-Compatible)

One file per concept, or a single file with all concepts. Useful for knowledge management tools.

**Single-file format:**

```markdown
---
title: NIST SP 800-53 Revision 5
publisher: NIST
version: r5
secid: secid:control/nist.gov/800-53@r5
document_type: standard
concept_count: 1189
---

## AC-2: Account Management

**Type:** control | **Parent:** AC | **Confidence:** High

The full text of the control...

**Cross-references:** AC-3, AC-6, IA-2

---

## AC-3: Access Enforcement

...
```

**Per-concept files** (for Obsidian vaults):

```
output/
  nist-800-53-r5/
    _metadata.md          # Document-level metadata
    AC/
      AC-2.md             # One file per control
      AC-3.md
      ...
```

## CSV

One row per concept. Flat — hierarchy is expressed through the `parent_id` column.

```csv
id,title,concept_type,hierarchy_level,parent_id,description,cross_references,confidence
AC-2,Account Management,control,control,AC,"The full text...","AC-3;AC-6;IA-2",High
AC-3,Access Enforcement,control,control,AC,"The full text...","AC-2;AC-4",High
```

## DataSets Repo Format

Follows the CSA DataSets repository convention. See `datasets-convention.md` for the full pattern. Produces a folder:

```
{document-name}/
  README.json             # Metadata (title, publisher, license, classification)
  document.md             # Original content in markdown
  document-processed.md   # Cleaned/processed markdown
  document.csv            # Structured CSV
  document.json           # Structured JSON
  PROCESSING-NOTES.md     # The recipe from Phase 5
```
