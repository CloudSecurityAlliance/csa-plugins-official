# Phase 3: Conversion

## Purpose

Mechanical format conversion to clean markdown. This phase is tool-driven, not AI-driven. The goal is to get the content into a format the AI can work with in Phase 4.

## Skip Condition

Skip this phase entirely if the input is already clean markdown or structured data (JSON/CSV). Go directly to Phase 4.

## Steps

### Step 1: Choose Conversion Tool

| Source Format | Recommended Tool | Install Command |
|--------------|-----------------|-----------------|
| PDF | marker | `pip install marker-pdf` |
| DOCX | pandoc | `brew install pandoc` or system package manager |
| HTML | pandoc or custom | `brew install pandoc` |
| Excel/CSV | Python stdlib | Already available |

**If the tool isn't installed:** Inform the user which tool is needed and how to install it. Offer alternatives:
- "If you can convert the document to markdown yourself, provide the markdown and we'll skip to Phase 4."
- "You could use an online converter — but **do not upload sensitive, licensed, private, or embargoed documents to third-party online services.** Only use online converters for publicly available, non-restricted content."

Don't block — there's always a path forward.

### Step 2: Convert

Run the appropriate tool. Record the exact command with version numbers:

```bash
# PDF example
marker_single /path/to/document.pdf --output_dir /path/to/output/

# DOCX example
pandoc -f docx -t markdown /path/to/document.docx -o /path/to/output.md

# HTML example
pandoc -f html -t markdown /path/to/document.html -o /path/to/output.md
```

If the DataSets repo tools are available (`~/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/tools-resources/utils/`), those can also be used:
- `pdf_to_md.sh` for PDF conversion
- `convert-HTML-to-Markdown.py` for HTML
- `docx_to_md.py` for DOCX

Record whichever tool and command you used — this goes into the recipe.

### Step 3: Clean

Strip non-content artifacts from the conversion output:

- **Page headers and footers** — repeated text at top/bottom of each page
- **Page numbers** — standalone numbers between content sections
- **Navigation elements** — table of contents links, "back to top" links
- **Boilerplate** — copyright notices, standard disclaimers (note their existence but remove from content body)
- **Image placeholders** — `![](image_N.png)` references from PDF conversion (note them, they may contain important tables or diagrams)
- **Broken tables** — PDF-to-markdown table conversion is often imperfect. Flag tables that look malformed rather than silently passing them through.

**Do NOT remove:**
- Front matter (title, authors, date, version)
- Table of contents (as a structural reference, even if links don't work)
- References/bibliography
- Appendices
- Any actual content, even if it looks like boilerplate — when in doubt, keep it

### Step 4: Record What You Did

For the recipe (Phase 5), record:

- Tool name and version (e.g., `marker-pdf 0.3.2`)
- Exact command used
- Input file characteristics (format, size, page count if applicable)
- What was cleaned and why
- Any manual corrections made (e.g., "fixed table on page 12 that marker split across two code blocks")
- Known issues with the conversion (e.g., "footnotes were lost", "two-column layout was linearized")

## Output

- Clean markdown file with content only
- Tool and command log (for recipe)
- List of known conversion issues or artifacts

## Teaching Moment (if teaching mode is on)

> **Why mechanical conversion matters:** The goal here is purely mechanical — get the document from its original format into clean markdown without interpreting or restructuring the content. The AI comprehension work happens in Phase 4. Keeping these separate means the conversion is reproducible (same tool, same command, same output) and the AI work is auditable (here's exactly what the AI was given, here's what it produced).
