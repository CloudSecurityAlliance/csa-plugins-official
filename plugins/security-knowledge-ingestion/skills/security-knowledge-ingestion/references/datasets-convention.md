# DataSets Repository Convention

CSA maintains structured security knowledge in the DataSets repositories:
- **Public:** `CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards`
- **Private:** `CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards`

This convention is how CSA organizes the data. You can follow it for your own repos, or adapt it to your needs. It's a recommendation, not a requirement.

## Directory Structure

Each document gets its own folder:

```
standards-voluntary/US/NIST/NIST.SP.800-53r5/
  README.json             # Required metadata
  document.md             # Main content in markdown
  document-processed.md   # Cleaned version (headers/footers stripped)
  document.csv            # Structured rows (one per concept)
  document.json           # Machine-readable structured data
  document_meta.json      # Processing metadata (from conversion tools)
  PROCESSING-NOTES.md     # How this was converted (the recipe)
```

Not all files are required — produce what you have. At minimum: `README.json` and one content file.

## Top-Level Organization

```
regulations-mandatory/{country}/      # Legally binding (EU AI Act, GDPR)
standards-voluntary/{scope}/{org}/    # Voluntary (NIST, ISO, PCI-DSS)
frameworks-guidance/{type}/{org}/     # Frameworks (CCM, CSF, ATT&CK)
best-practices/companies/{company}/   # Company guidelines
```

## README.json Schema

```json
{
  "title": "NIST SP 800-53 Revision 5",
  "short_title": "NIST 800-53r5",
  "publisher": "National Institute of Standards and Technology",
  "version": "Revision 5",
  "date": "2020-09-23",
  "url": "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
  "license": "Public domain (US Government work)",
  "license_required": false,
  "classification": "standards-voluntary",
  "country": "US",
  "description": "Security and Privacy Controls for Information Systems and Organizations"
}
```

For licensed standards (ISO, IEEE): set `"license_required": true` and include a `"purchase_url"` field. Do not include the full text of licensed content.

## Naming Conventions

- Folders include version: `NIST.SP.800-53r5/`, `CCM-4.1/`
- Use official naming: `NIST.AI.600-1/`, not `nist-ai-600-1/`
- No version subdirectories: `CCM-4.1/` not `CCM/4.1/`

## Conversion Pipeline

The DataSets repo follows this progression:

```
Original (PDF/HTML/DOCX)
  → document.md (markdown conversion)
    → document-processed.md (cleaned)
      → document.csv (structured rows)
        → document.json (machine-readable)
```

Each step is documented in `PROCESSING-NOTES.md` — which is the recipe from Phase 5 of this plugin.

## Tools

The DataSets repo has conversion tools in `tools-resources/utils/`:
- `pdf_to_md.sh` — PDF to markdown (uses marker)
- `convert-HTML-to-Markdown.py` — HTML to markdown
- `docx_to_md.py` — DOCX to markdown
- `convert-CSV-to-JSON-list.py` — CSV to JSON
- `excel_to_csv.py` — Excel to CSV

These are the same tools Phase 3 of this plugin uses. If you're producing DataSets-format output, you're already compatible.
