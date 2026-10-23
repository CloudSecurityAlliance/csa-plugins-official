# Where this plugin departs from CSA's published scorer

`valid-ai-ted-scorer` 1.0.1 is CSA's published Valid-AI-ted Scorer package 1.1.0
(`caiq-scorer-v1.1.0.zip`, SHA-256 `ae37c946e734030d90c30ae911955ed6e3136135715f1b6223fefcacf7770334`): the published
method with seven documented fixes, and reference data added so that every CAIQ and AI-CAIQ release CSA publishes
is scored against the CCM or AICM version it pairs with.

**What is unchanged.** The scoring prompts, `VERSION`, `CHANGELOG.md` and the four published reference files are the
package's own, byte for byte. CSA's published `SKILL.md` text is also unchanged: the plugin adds blocks marked
`<!-- valid-ai-ted-scorer: begin … -->` and `<!-- valid-ai-ted-scorer: end … -->`, and removing them gives the
published file byte for byte. No data file is edited; each fix is a rule for reading the files. Line numbers below are
those of the published `SKILL.md`.

**How a block works.** Each block sits directly after the published sentence it amends, and names that sentence. The
first block, after line 15, tells the model that a block takes precedence over the sentence it names, and over the
general words "exactly", "without interpretation", "no aliases" and "do not deviate", for that point only. Everything
else applies as written.

**Kept as published** (the method's owner ruled on these on 2026-10-22):
- **Ruling 01.** All three mechanical checks zero the row and skip AI scoring (lines 35–41), including the third-party
  customer rule.
- **Ruling 02.** A row's Score is the model's overall score, with the "No" cap, the contradiction 0 and the clamp
  (lines 47–56).
- **Ruling 08.** The overall score is the plain mean of all rows, and PASS is 50% or more (line 59).

## The fixes

### A-01: CSA's ownership value "Shared MP-OSP"

- **`SKILL.md` says:** line 37: ownership must match a listed value, "case-insensitive exact match, no aliases, no fuzzy
  matching", or the row scores 0. Line 39 lists `Shared by MP-OSP` for `ai-caiq` mode.
- **The plugin:** also accepts `Shared MP-OSP`, and treats the two spellings as one value. Line 37's "no aliases" does
  not apply to this one pair. It never advises a member to change one spelling into the other.
- **Why:** CSA's AI-CAIQ templates (v1.0.2 and v1.1.0) offer `Shared MP-OSP` in their drop-down, and "Shared by
  MP-OSP" appears nowhere in CSA's AICM or AI-CAIQ material. Under the published text, every row where a member picks
  CSA's own value scores 0, and CSA's testing found the report then advising the member to change the correct value.
- **Effect on scores:** rows using `Shared MP-OSP` are judged by the model instead of scoring 0. No other row changes.
- **Upstream:** drafted for CSA's scoring engine and for the members' package; not yet filed.

### A-02: where to read the version, and which reference file each questionnaire uses

- **`SKILL.md` says:** line 23: detect the framework version "from the cell A1 metadata or the filename", ask the
  member to confirm, and stop if the version is not one of CCM 4.0.13, CCM 4.1.0, AICM 1.0.2 or AICM 1.1.0.
- **The plugin:**
  - **where to read:** the stamp is in A1 of the `Introduction` sheet, and the questionnaire sheet's A1 carries the
    same stamp. It is JSON (`specification_name`, `specification_version`, `caiq_version`) or, in CAIQ v4.0.x, plain
    text such as `v4.0.2`. `caiq_version` is read first, then `specification_version`, then the questionnaire sheet's
    name, then the filename. If they disagree, or nothing names a version, the plugin asks the member and never
    guesses;
  - **which file:** a table covering every CAIQ and AI-CAIQ release CSA publishes, and those members still hold:

| The questionnaire | Its stamp | Reference file |
|---|---|---|
| CAIQ v4.0.1, v4.0.2 or v4.0.3 | plain text `v4.0.x`, which names no CCM version | `CCM-4.0.13-merged.csv` (CCM 4.0.12 has identical text) |
| CAIQ v4.1.0, or CAIQ-Lite v4.1.0 | `specification_version` 4.1.0 | `CCM-4.1.0-merged.csv` |
| CAIQ v4.1.0 | `specification_version` 4.1.1 (CSA's bundle of 2026-10-02) | `CCM-4.1.1-merged.csv` (added) |
| AI-CAIQ 1.0.2 | `specification_version` 1.0.2 | `AICM-1.0.2-merged.csv` |
| AI-CAIQ 1.0.2 | `specification_version` 1.0.3 (CSA's bundle of 2025-11-10) | `AICM-1.0.3-merged.csv` (added) |
| AI-CAIQ 1.1.0 | `specification_version` 1.1.0 (CSA's bundle of 2026-06-18) | `AICM-1.1.0-published-merged.csv` (added) |
| AI-CAIQ 1.1.0 | `specification_version` 1.1.1 (CSA's current bundle) | `AICM-1.1.1-merged.csv` (added) |
| a stamp with no `caiq_version` | `specification_version` only | that specification's file |
| SSCF-CAIQ v1.0 (CSA's SaaS Security Capability Framework) | no stamp; sheet `SSCF-CAIQv1.0` | none: a different framework, with no ownership column; the plugin says so, not that a newer scorer may exist |
| CAIQ v3.x, AI-CAIQ 1.0.1, or anything else | — | none: as line 23 says |

  The member still confirms the version before scoring.
- **Why:** questionnaires name questionnaire versions, not framework versions, and CSA ships the same questionnaire
  version stamped with different framework versions. Examples:
  - CAIQ v4.0.x files say `v4.0.2` or `v4.0.3`, and never "4.0.13";
  - CAIQ v4.1.0 comes stamped CCM 4.1.0 or 4.1.1;
  - AI-CAIQ 1.0.2 is stamped AICM 1.0.3;
  - AI-CAIQ 1.1.0 is stamped AICM 1.1.0 or 1.1.1.

  Read literally, line 23 stops or misroutes these real files. CSA decided on 2026-10-22 to support every current
  version of the CAIQ, and to record which CCM or AICM version each maps to. The table was built from:
  - CSA's own templates and change logs;
  - 13 STAR Registry files;
  - CSA's MCP data service.

  A questionnaire's own control titles and specifications equal those of the file the table gives it.
- **Effect on scores:** each questionnaire is enriched with the guideline text of the framework version it was
  issued with, as line 25 requires. Against the published package:
  - a CAIQ stamped CCM 4.1.1 gets CCM 4.1.1's text instead of a stop or CCM 4.1.0's;
  - an AI-CAIQ stamped AICM 1.0.3 gets 1.0.3's UEM-01 CSP guideline instead of 1.0.2's;
  - an AI-CAIQ stamped AICM 1.1.0 gets CSA's published 1.1.0 instead of the pre-publication text (63 cells, A-05);
  - an AI-CAIQ stamped AICM 1.1.1 gets 1.1.1's three corrected MP guidelines.
- **Upstream:** reported in CSA's review of the package (finding A-02); no separate draft.

### A-03: which sheet and rows are the questionnaire (two blocks)

- **`SKILL.md` says:** line 21: "Read the uploaded file". Line 29: look up "the row's Control ID". Line 59: "group by
  `CCM Domain Title` / `AICM Domain Title`".
- **The plugin:** in a block directly after line 21 (`A-03-sheet`), scores only the questionnaire sheet, named like `CAIQv4.1.0` or `AI-CAIQv1.1.0`, or else the
  sheet whose header row holds "Question ID" (row 2 in CSA's templates); never the `Introduction` sheet or an `About`
  sheet. In a file that is not CSA's template as published (a CSV export, renamed sheets, extra or deleted columns),
  it finds each column by its header name, and asks the member if the mode or version is still unclear. In the block
  after line 29 (`A-03`), a blank Control ID or Domain Title inside a merged range takes the value at the top of the range. A
  row's Control ID is its Question ID before the dot. Only rows whose Question ID looks like `AIS-08.1` are questions;
  "End of Standard" and the copyright line are not.
- **Why:** CSA's templates merge those cells over several rows. In CSA's templates and 13 registry files, the Control
  ID is blank on 22–27% of question rows and the Domain Title on 94%, so a literal read leaves those rows without
  guideline text or a domain. The two footer rows are not questions, but one test run first counted them (285 on a
  283-question file).
- **Effect on scores:** every question gets its guideline text and its own domain, and footer rows are never scored or
  counted.
- **Upstream:** reported in CSA's review of the package (finding A-03); no separate draft.

### A-05: matching reference rows on the Control ID only

- **`SKILL.md` says:** line 29: "exact match on the `Control ID` column".
- **The plugin:** matches on the Control ID only, never on the title. It reports a differing title to the member, but
  never refuses or re-matches a row because of it. The output's Control Title and Control Specification are the
  questionnaire's own text.
- **Why:** the package's `AICM-1.1.0-merged.csv` is a pre-publication text of AICM 1.1.0. 63 cells in 20 controls
  differ from CSA's published workbook, including two title typos ("Source Code Managemement" for AIS-12,
  "Prompt Differentation" for AIS-15) and three specifications (AIS-09, LOG-03, LOG-16). A title check would refuse
  valid rows.
- **Effect on scores:** none. Guideline text still comes from the file of the confirmed version. Since the A-02 table
  sends an AI-CAIQ stamped AICM 1.1.0 to CSA's published 1.1.0, the package's pre-publication file, which ships
  unchanged, is not used (CSA's decision, 2026-10-22).
- **Upstream:** drafted as a data note for CSA's scoring engine; not yet filed.

### A-15: the AI-CAIQ answer column

- **`SKILL.md` says:** line 21 names the AI-CAIQ answer column `Service Provider CAIQ Answer`.
- **The plugin:** `Service Provider AI-CAIQ Answer`, the header in CSA's AI-CAIQ templates, is the answer column and
  marks `ai-caiq` mode. Headers are matched ignoring case and runs of spaces (CSA's CAIQ template has two spaces in
  `CSC Responsibilities  (Optional/Recommended)`). The output's column names stay exactly as lines 66–69 give them.
- **Why:** CSA's AI-CAIQ templates (v1.0.2 and v1.1.0) head the answer column `Service Provider AI-CAIQ Answer`, a
  name `SKILL.md` does not give.
- **Effect on scores:** none intended. It makes sure the member's answers are read from CSA's own column.
- **Upstream:** drafted for CSA's scoring engine; not yet filed.

### A-25: the byte-order mark in `CCM-4.0.13-merged.csv`

- **`SKILL.md` says:** line 29: look the row up in "the matching `reference/*.csv`".
- **The plugin:** reads the reference files as UTF-8 and ignores a byte-order mark at the start of a file, so the
  first column reads `Control Domain`.
- **Why:** `CCM-4.0.13-merged.csv` begins with a UTF-8 byte-order mark. The file is not edited (no data file is).
- **Effect on scores:** none. It prevents a misread first column.
- **Upstream:** reported in CSA's review of the package (finding A-25); no separate draft.

### Ruling 20: which descriptions each AI-CAIQ ownership value requires

- **`SKILL.md` says:** line 40 lists which descriptions are required, for CAIQ ownership values only. "If ownership is
  missing or unparseable, require both."
- **The plugin:** line 40's lists are the `caiq` table. In `ai-caiq` mode:
  - the provider description is required for every valid value except `Not Determined`;
  - the customer description is required only for `Owned by AIC`, `Shared AP-AIC` and
    `Shared Across the Supply Chain`;
  - `Not Determined` requires neither.

  Line 40's last sentence applies in both modes. A required description that fails step 5's first rule zeroes the row.
- **Why:** `SKILL.md` gives no table for AI-CAIQ values, so the outcome was left to the model; in CSA's testing it told
  the member a row was fine and then scored it 0. The method's owner ruled this table on 2026-10-22.
- **Effect on scores:** in AI-CAIQ files, a row with a required description that is blank, 1–2 characters, or just
  "yes"/"no" scores 0 by rule instead of by the model's judgment. A description the table does not require may be
  blank or short without a mechanical 0 (the block says so): the row goes to AI scoring, where empty content scores 0.
- **Upstream:** drafted for CSA's scoring engine, with the ruling; not yet filed.

## Other marked blocks

- **Reference data added** (after line 23; amends the lists of reference data in lines 13 and 23). The plugin adds
  four files, each built from CSA's own workbook for its version, in the package's format, and gated. The method is
  the one that reproduces the package's `CCM-4.1.0-merged.csv` byte for byte, its `CCM-4.0.13-merged.csv` cell for
  cell, and its `AICM-1.1.0-merged.csv` except A-05's 63 cells:
  - `CCM-4.1.1-merged.csv`;
  - `AICM-1.0.3-merged.csv`;
  - `AICM-1.1.0-published-merged.csv`, CSA's published AICM 1.1.0. **The package's pre-publication
    `AICM-1.1.0-merged.csv` ships unchanged, byte for byte, but is not used**: no row of the A-02 table names it.
    CSA decided this on 2026-10-22;
  - `AICM-1.1.1-merged.csv`.

  The checks behind each: its control IDs, the questionnaire it pairs with, zero differences from the workbook, and CSA's
  MCP data service where it holds that version. `reference/VERSION.txt` gives each file's source, checks and SHA-256,
  and `reference/NOTICE-CCM.txt` and `NOTICE-AICM.txt` give CSA's notice for each version.
- **Precedence** (after line 15). It says how a block relates to the published text.
- **Ruling 08 note** (after line 59). Compare the unrounded percentage with 50%, and round only for display. It
  clarifies line 59 and changes nothing.
- **Outputs** (after line 73; amends line 73's `About` fields, page 1 of line 76 and the final page of lines 79–82). It adds two rows to
  the workbook's `About` sheet, and the same two lines after the disclaimer on the PDF's last page:
  `Plugin: valid-ai-ted-scorer 1.0.1` and `Plugin fixes applied: A-01, A-02, A-03, A-05, A-15, A-25, ruling 20;
  reference data added for CCM 4.1.1, AICM 1.0.3, AICM 1.1.0 (published text) and AICM 1.1.1 (see DEVIATIONS.md)`. The disclaimer, the footer and the published version marks are unchanged.
  From 1.0.1 it also says that the disclaimer's `**` marks are Markdown bold, to be left out of plain-text outputs
  with the words unchanged, and that page 1's questionnaire version field is the prefix and the number only
  (`CAIQ: 4.1.0` for a CAIQ-Lite too).
- **Guidance, help, and where this copy comes from** (appended after line 92). This is guidance for the AI and the
  member, not a change to the method:
  - a mechanical 0 is final: never offer to re-score it (from 1.0.1);
  - the files are for the member's own use;
  - the member chooses the accessibility level;
  - nothing is installed without asking;
  - a fallback CSV or Markdown report, per file, for a file that nothing here can make, Python's standard library
    included (per file from 1.0.1);
  - working files go in one folder beside the questionnaire, `<input name>_work/`, never in a temporary, home or
    parent folder (from 1.0.1);
  - drafts are built and checked in the working folder, and no superseded draft is left beside the questionnaire
    (from 1.0.1);
  - counts are taken from the workbook (from 1.0.1);
  - Python is run by name before asking the member (from 1.0.1);
  - built-in help;
  - the copy's provenance.

## The published version marks

The outputs still say `CSA Valid-AI-ted Scorer v1.1.0` (the footer, the disclaimer and the `About` sheet), because
1.1.0 is the version of CSA's method and package. 1.0.1 is the version of this plugin's packaging. The two `About`
rows and the PDF's last lines say which plugin, and which fixes, produced the files.
