# Phase 2: Acquisition

## Purpose

Get the data into a workable state. Determine what format it's in and route accordingly.

## Steps

### Step 1: Determine What the User Provided

| Input Type | How to Detect | Next Action |
|-----------|---------------|-------------|
| Local file (PDF, DOCX, HTML) | User provided a file path | Read and examine the file |
| Local file (markdown) | User provided .md file | Examine — may skip to Phase 4 |
| Local file (JSON, CSV) | User provided structured data | Examine — likely skip to Phase 4 for verification |
| URL | User provided a web link | Fetch the content |
| SecID reference | User chose SecID data in Phase 1 | Retrieve from SecID v2 |
| Pasted text | User pasted content directly | Save to working file |

### Step 2: If URL — Fetch the Content

Use web fetch to retrieve the content. If the page requires JavaScript rendering (common for some government sites), fall back to Playwright.

Note the URL — this goes into the recipe (Phase 5) as the source URL.

### Step 3: If SecID v2 — Retrieve Structured Data

If the user chose to use SecID's data in Phase 1, retrieve:
- The structured data (concepts, hierarchy, metadata)
- The recipe that produced it (tools, prompts, steps)

With SecID data in hand, you can skip to Phase 4 for verification (confirm the data looks correct) or directly to Phase 5 to capture/review the recipe.

### Step 4: Determine Format and Route

| Format | State | Route To |
|--------|-------|----------|
| PDF | Raw, needs conversion | Phase 3 |
| DOCX | Raw, needs conversion | Phase 3 |
| HTML | Raw, needs conversion | Phase 3 |
| Markdown (raw) | Has content but not structured | Phase 3 (for cleaning) or Phase 4 (if already clean) |
| Markdown (processed) | Clean, content-only | Phase 4 |
| CSV with concepts | Structured, one row per concept | Phase 4 (verification) |
| JSON with concepts | Structured, concepts identified | Phase 4 (verification) |
| JSON/CSV (flat, no concepts) | Structured but not decomposed | Phase 4 |

**How to tell "clean" from "raw" markdown:** Clean markdown has content only — no page headers/footers, no navigation elements, no repeated boilerplate. Raw markdown (e.g., from a PDF conversion) typically has artifacts from the conversion process.

**How to tell "structured" from "flat":** Structured data has individually identified concepts with IDs, titles, descriptions, and hierarchy. Flat data might be a table dump or a list without concept-level decomposition.

### Step 5: Inform the User

Tell the user what you found and what happens next:

> "You provided a [format] file. [It needs conversion / It's already clean markdown / It's already structured]. Next step: [Phase 3: Conversion / Phase 4: Profiling & Decomposition / Phase 4: Verification]."

## Output

- The document content in its current form
- Format classification
- Routing decision (which phase is next)
- Source URL (if fetched from web — for the recipe)
