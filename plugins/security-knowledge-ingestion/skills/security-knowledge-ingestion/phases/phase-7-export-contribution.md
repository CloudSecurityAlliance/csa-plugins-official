# Phase 7: Export & Contribution

## Purpose

Deliver the structured data and recipe in the user's preferred format. Guide them toward good data management practices. If the content is new to SecID and the license allows, offer a contribution path.

Read `references/output-formats.md`, `references/license-handling.md`, and `references/datasets-convention.md` before starting this phase.

## Steps

### Step 1: Export Structured Data

Ask the user which format(s) they want:

| Format | Description | Best For |
|--------|-------------|----------|
| **JSON** | Structured with concepts, hierarchy, metadata | Machine consumption, API use, mapping tools |
| **YAML-frontmatter Markdown** | Obsidian-compatible, one file per concept or single file | Human reading, note-taking, knowledge management |
| **CSV** | One row per concept, flat | Spreadsheets, quick analysis, import to databases |
| **DataSets repo format** | Full folder structure with README.json, document.md, etc. | Contributing to CSA DataSets repo or following that convention |

See `references/output-formats.md` for the schema and layout of each format.

If the user doesn't have a preference, default to JSON (most versatile).

### Step 2: Export Recipe

Save the recipe from Phase 5 alongside the structured data. Same directory, consistent naming:

- `{document-name}.json` + `{document-name}-recipe.md`
- Or DataSets convention: `document.json` + `PROCESSING-NOTES.md`

The recipe travels with the data. They're a pair.

### Step 3: Storage Guidance

Ask the user where they're storing this:

> "Where will you keep the structured data and recipe? A few options:"

**GitHub repo** (recommended): Version-controlled, shareable, easy to update when the source document changes. CSA uses a DataSets repo pattern — see `references/datasets-convention.md` for the convention with examples. If you're going to contribute to the community or collaborate with others, this is the best option.

**Google Drive**: Easy sharing, accessible anywhere, no version control but good for teams that don't use git.

**OneDrive/SharePoint**: Good for enterprise/Microsoft shops, team sharing, integrates with existing workflows.

**Local files**: Works, but the data dies with your laptop unless you have backups. No versioning, no collaboration. If you have backup software (Time Machine, Backblaze, etc.) your data is safe, but you lose version history and the ability to share or contribute.

Don't lecture — present the options and let the user choose. If they say "local files," that's fine.

### Step 4: Contribution (if applicable)

**Only offer this if the source was NOT already in SecID** (check the SecID status from Phase 1).

If SecID status was `known_no_data` or `unknown`, proceed with the contribution flow:

#### Step 4a: License Check

This is where the license matters — not for the user's local processing (that's already done), but for public redistribution via SecID.

**First, check the blocklist** (see `references/license-handling.md`):

| Blocked Source | Reason |
|---------------|--------|
| ISO standards (full text) | Copyrighted, not freely redistributable |
| IEEE standards (full text) | Copyrighted, not freely redistributable |
| HITRUST CSF | Licensed, requires agreement |
| PCI-DSS (full text) | Requires acceptance of terms |

If the source is on the blocklist:

> "This is licensed content — the structured data can't be contributed to SecID for public serving. You can still file the recipe (prompts, tools, steps) — just not the structured content. The recipe helps others who have their own licensed copy process it the same way."

If not on the blocklist, determine the license:

> "Before we can suggest contributing this to SecID, we need to know the license. Can you provide the license for this content, or would you like me to look for it at the source URL?"

If the user says to look:
- Check the source URL for license/terms pages
- Check the document itself for license statements
- Check common locations (footer, about page, legal page)

Present what you find and let the user confirm.

**Three outcomes:**

| License Status | Contribution Advice |
|---------------|-------------------|
| Open/permissive (CC0, CC-BY, public domain, government work) | "This can be contributed — both structured data and recipe." |
| Licensed/restricted | "The structured data can't be contributed for public redistribution. You can still contribute the recipe." |
| Unknown/unclear | "We couldn't determine the license. You can use this locally, but we can't recommend contributing it for public redistribution until the license is confirmed. You can still contribute the recipe." |

#### Step 4b: Contribution Nudge

For content that can be contributed (or recipe-only for licensed content):

> "Want to help the community? You can file an issue at the SecID repository with:
> - The source URL (where the original content lives)
> - The recipe (tools, prompts, and steps used to process it)
> - The structured data output (if the license allows)
>
> The SecID team will review it for inclusion. Would you like me to draft the issue?"

If the user says yes, draft a GitHub issue body they can copy:

```markdown
## New source: {Document Title} {Version}

**SecID**: {secid string}
**Source URL**: {url}
**Publisher**: {publisher}
**License**: {license status}

### Recipe

{paste or link to recipe}

### Structured Data

{paste, link, or "licensed content — recipe only"}

### Notes

{any relevant notes about the conversion}
```

**Never auto-file the issue.** Draft it, show it to the user, let them file it themselves.

#### Step 4c: SecID Registry Entry

If the source was `unknown` to SecID (not even in the registry), additionally suggest:

> "This source isn't in SecID's registry at all yet. The SecID team can also add a registry entry so future users can discover it. Include this in the issue if you'd like."

### Step 5: Wrap Up

Summarize what was produced:

> "Done! Here's what you have:
> - Structured data: {path/format}
> - Recipe: {path}
> - {N} concepts across {M} hierarchy levels
> - Validation: {status — validated/skipped}
> - Contribution: {status — drafted issue/not applicable/recipe only}
>
> If you run into any issues or want to share feedback: https://github.com/CloudSecurityAlliance/csa-plugins-official/issues"

## Output

- Structured data in user's chosen format(s)
- Recipe document
- Optional: drafted contribution issue
- Storage guidance delivered
