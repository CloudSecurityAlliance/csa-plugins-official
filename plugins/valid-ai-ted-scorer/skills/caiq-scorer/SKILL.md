---
name: caiq-scorer
description: Scores a completed CAIQ (CCM) or AI-CAIQ (AICM) questionnaire question-by-question on a 0-4 scale using CSA's Valid-AI-ted scoring methodology, and produces a scored workbook plus a domain-rollup summary report (PDF). Use when the user uploads or references a filled-out CAIQ or AI-CAIQ (for example one downloaded from the CSA STAR Registry) and wants it scored, graded, rated, or wants a Valid-AI-ted style scoring or summary report.
metadata:
  publisher: Cloud Security Alliance
  version: "1.1.0"
  prompt-set: "1.0.0"
  frameworks: "CCM 4.0.13, CCM 4.1.0, AICM 1.0.2, AICM 1.1.0"
---

# CSA Valid-AI-ted Scorer (CAIQ / AI-CAIQ)

**Package version 1.1.0** · scoring prompt set 1.0.0 · reference data for CCM 4.0.13, CCM 4.1.0, AICM 1.0.2 and AICM 1.1.0.

This skill applies the Cloud Security Alliance's Valid-AI-ted scoring methodology to a completed CAIQ or AI-CAIQ. The scoring prompts in `prompts/caiq/` and `prompts/ai-caiq/` and the control reference data in `reference/` are CSA's own methodology files. Follow the pipeline below exactly.

<!-- valid-ai-ted-scorer: begin precedence -->
> **How to read this file (plugin `valid-ai-ted-scorer` 1.0.1).** This file is CSA's published Valid-AI-ted Scorer instructions (package 1.1.0), unchanged, plus blocks marked `valid-ai-ted-scorer`, like this one. Each block sits directly after the published sentence it amends, and names that sentence. Line numbers in the blocks ("published line 37") count the lines of CSA's published `SKILL.md`, without the blocks. A block takes precedence over the sentence it names, and over the general words "exactly", "without interpretation", "no aliases" and "do not deviate", **for the point it names only**. Everything else applies as written: every other mechanical rule, the "No" cap, the contradiction rule, the output columns, the version marks and the disclaimer. The sections marked `valid-ai-ted-scorer` at the end of this file (guidance, help, and where this copy comes from) apply too. The plugin's `DEVIATIONS.md`, two folders up from this file, gives each block's reason and its effect on scores.
<!-- valid-ai-ted-scorer: end precedence -->

The result is an **informational, AI-assisted assessment** of the quality and internal consistency of the written responses. It does not verify that controls are implemented, and it is not a CSA certification, audit, attestation, STAR Registry listing or Valid-AI-ted badge. Every report must carry the disclaimer in step 9.

## Pipeline

1. **Detect mode.** Read the uploaded file. If it has CAIQ/CCM-style columns (`CSP CAIQ Answer`, `SSRM Control Ownership`, `CSP Implementation Description...`, `CCM Control ID`, `CCM Domain Title`), the mode is **`caiq`**. If it has AI-CAIQ/AICM-style columns (`Service Provider CAIQ Answer` or AICM-specific guideline columns, `AICM Control ID`/`AICM Domain Title`), the mode is **`ai-caiq`**. If cell A1 contains JSON metadata naming the specification (`"specification_name"`), use it to confirm. If the mode is still ambiguous, ask the user.

   <!-- valid-ai-ted-scorer: begin A-03-sheet -->
   > **Plugin fix A-03, which sheet** (amends step 1's "Read the uploaded file", published line 21; see `DEVIATIONS.md`): score only the questionnaire sheet. It is the sheet named like `CAIQv4.0.3`, `CAIQv4.1.0`, `CAIQLitev4.1.0`, `AI-CAIQv1.0.2` or `AI-CAIQv1.1.0`, or else the sheet whose header row holds "Question ID"; in CSA's templates the header row is row 2. Never score the `Introduction` sheet, the other information sheets, or an `About` sheet. If the file is not CSA's template as published (a CSV export, renamed sheets, extra or deleted columns), find each column by its header name, as A-15 says; if the mode or the version is still unclear, ask the member, and never guess.
   <!-- valid-ai-ted-scorer: end A-03-sheet -->

   <!-- valid-ai-ted-scorer: begin A-15 -->
   > **Plugin fix A-15** (amends step 1's "`Service Provider CAIQ Answer`", published line 21; see `DEVIATIONS.md`): CSA's AI-CAIQ templates head the answer column `Service Provider AI-CAIQ Answer`. That is the AI-CAIQ answer column, and it marks `ai-caiq` mode just as `Service Provider CAIQ Answer` does. Match column headers ignoring case and runs of spaces: CSA's CAIQ template, for example, has two spaces in `CSC Responsibilities  (Optional/Recommended)`. The output's column names stay exactly as step 8 gives them.
   <!-- valid-ai-ted-scorer: end A-15 -->

2. **Detect the framework version** (CCM 4.0.13 or 4.1.0; AICM 1.0.2 or 1.1.0) from the cell A1 metadata or the filename, then **ask the user to confirm which version applies before enriching. Never silently default to a version.** If the questionnaire declares a version not listed above, tell the user this package does not include reference data for it and that a newer version of the scorer may be available from CSA; do not substitute a different version's guideline text.

   <!-- valid-ai-ted-scorer: begin added-data -->
   > **Plugin data: reference files added** (amends the lists of reference data in published line 13 and in step 2, published line 23; see `DEVIATIONS.md`): besides the package's four files, this plugin carries four files it generated from CSA's own workbooks, in the package's format: `CCM-4.1.1-merged.csv`, `AICM-1.0.3-merged.csv`, `AICM-1.1.0-published-merged.csv` (CSA's published AICM 1.1.0; the package's `AICM-1.1.0-merged.csv` is a pre-publication text) and `AICM-1.1.1-merged.csv`. They are the plugin's additions, not part of CSA's published package; `reference/VERSION.txt` gives each file's source. The A-02 table below says which file each questionnaire uses. Never mix files: CCM 4.0.x and 4.1.x retitled and renumbered controls just as AICM 1.0.x and 1.1.x did, so the "AICM only" rule below applies to CCM too.
   <!-- valid-ai-ted-scorer: end added-data -->

   <!-- valid-ai-ted-scorer: begin A-02 -->
   > **Plugin fix A-02** (amends step 2's "from the cell A1 metadata or the filename", published line 23, its list of versions, and, for the questionnaires in the table below that it cannot score, its suggestion that a newer scorer may be available; see `DEVIATIONS.md`): a questionnaire names its own questionnaire version, which is not always the framework version.
   >
   > **Where to read the version.** In CSA's templates the first sheet is `Introduction`, and its cell A1 holds the stamp; the questionnaire sheet's A1 carries the same stamp. The stamp is either JSON (`specification_name`, `specification_version` and `caiq_version`) or, in CAIQ v4.0.x, plain text such as `v4.0.2`. Read `caiq_version` first, for the questionnaire's version, then `specification_version`, for the framework's: the table's rows are chosen by the pair, not by either alone (an AI-CAIQ 1.1.0 may be stamped AICM 1.1.0 or 1.1.1). With no JSON, use the version the plain text names, then the questionnaire sheet's name (for example `CAIQv4.0.2`), then the filename. If the stamps disagree, or nothing names a version, ask the member; never guess.
   >
   > **Which reference file.** Propose it from this table:
   >
   > | The questionnaire (its sheet; its A1 stamp) | Use |
   > |---|---|
   > | CAIQ v4.0.1, v4.0.2 or v4.0.3 (sheet `CAIQv4.0.x`; A1 plain text such as `v4.0.2`, which names no CCM version) | `CCM-4.0.13-merged.csv` |
   > | CAIQ v4.1.0, or CAIQ-Lite v4.1.0, stamped CCM 4.1.0 (sheet `CAIQv4.1.0` or `CAIQLitev4.1.0`; `specification_version` 4.1.0, with `specification_name` "Cloud Controls Matrix", or "Cloud Controls Matrix Lite" for CAIQ-Lite) | `CCM-4.1.0-merged.csv` |
   > | CAIQ v4.1.0 stamped CCM 4.1.1 (sheet `CAIQv4.1.0`; `specification_version` 4.1.1: CSA's bundle of 2026-10-02) | `CCM-4.1.1-merged.csv` |
   > | AI-CAIQ 1.0.2 stamped AICM 1.0.2 (sheet `AI-CAIQv1.0.2`; `specification_version` 1.0.2) | `AICM-1.0.2-merged.csv` |
   > | AI-CAIQ 1.0.2 stamped AICM 1.0.3 (sheet `AI-CAIQv1.0.2`; `specification_version` 1.0.3: CSA's bundle of 2025-11-10) | `AICM-1.0.3-merged.csv` |
   > | AI-CAIQ 1.1.0 stamped AICM 1.1.0 (sheet `AI-CAIQv1.1.0`; `specification_version` 1.1.0: CSA's bundle of 2026-06-18) | `AICM-1.1.0-published-merged.csv`, CSA's published AICM 1.1.0 (not the package's pre-publication `AICM-1.1.0-merged.csv`) |
   > | AI-CAIQ 1.1.0 stamped AICM 1.1.1 (sheet `AI-CAIQv1.1.0`; `specification_version` 1.1.1: CSA's current bundle) | `AICM-1.1.1-merged.csv` |
   > | no `caiq_version` in A1, and a `specification_version` named above | the file of that specification version; tell the member it was chosen from the specification stamp, because the stamp names no questionnaire version |
   > | SSCF-CAIQ v1.0, for CSA's SaaS Security Capability Framework (sheet `SSCF-CAIQv1.0`; no A1 stamp; Question IDs such as `CCC-SaaS-1.1`) | none: tell the member it is a questionnaire for a different CSA framework, which this method cannot score (it has no ownership column, and there is no CCM or AICM data for it); do not suggest that a newer scorer covers it. Do not suggest that CSA has another method for it. |
   > | CAIQ v3.x (for CCM 3.0.1), AI-CAIQ 1.0.1, or anything else | none: do as step 2 says (CAIQ v3.x has no ownership or description columns, and CSA added the AI-CAIQ's answer columns in 1.0.2, so the method cannot score these) |
   >
   > Then still ask the member to confirm the version, as step 2 says, and never score without that confirmation.
   <!-- valid-ai-ted-scorer: end A-02 -->

   **AICM only:** control IDs are *not* stable between AICM 1.0.x and 1.1.x. Of the 242 control IDs shared by the two reference files, 65 have a different `Control Title` (for example, `AIS-08` is "Input Validation" in 1.0.2 but "API Security" in 1.1.0). Using the wrong file attaches wrong guideline text with no visible error. Enrich only from the reference file that matches the confirmed version; never mix them.

3. **Normalize.** Treat answers as `Yes`/`No`/`NA` (case- and whitespace-insensitive). Preserve a literal "NA"; never confuse it with a blank or missing answer.

4. **Enrich each row.** Look up the row's Control ID in the matching `reference/*.csv` by exact match on the `Control ID` column, and attach:

   <!-- valid-ai-ted-scorer: begin A-03 -->
   > **Plugin fix A-03, which rows** (amends step 4's "the row's Control ID", published line 29, and step 7's "group by … Domain Title", published line 59; see `DEVIATIONS.md`): CSA's templates merge the Control ID and Domain Title cells over several rows, so most rows read blank there. A blank Control ID or Domain Title inside a merged range takes the value at the top of the range. A row's Control ID is its Question ID before the dot (`AIS-08.1` → `AIS-08`). Only rows whose Question ID looks like `AIS-08.1` (letters or `&`, a hyphen, two digits, a dot, digits) are questions; the "End of Standard" row and the copyright line at the foot of the sheet are not, and are neither scored nor counted.
   <!-- valid-ai-ted-scorer: end A-03 -->

   <!-- valid-ai-ted-scorer: begin A-05 -->
   > **Plugin fix A-05** (amends step 4's "exact match on the `Control ID` column", published line 29; see `DEVIATIONS.md`): match reference rows on the Control ID only, never on the title. If the questionnaire's title differs from the reference file's (the package's AICM 1.1.0 file has two typos, in AIS-12 and AIS-15), tell the member, but never refuse or re-match the row because of it. The output's Control Title and Control Specification are the questionnaire's own text; the guideline columns come from the reference file.
   <!-- valid-ai-ted-scorer: end A-05 -->

   <!-- valid-ai-ted-scorer: begin A-25 -->
   > **Plugin fix A-25** (amends step 4's "the matching `reference/*.csv`", published line 29; see `DEVIATIONS.md`): read the reference files as UTF-8 and ignore a byte-order mark at the start of a file (`CCM-4.0.13-merged.csv` has one), so that its first column reads `Control Domain`.
   <!-- valid-ai-ted-scorer: end A-25 -->
   - **`caiq` mode:** `CSP` as *Cloud Service Provider Implementation Guidelines (CSP)*, `CSC` as *Cloud Service Consumer Implementation Guidelines (CSC)*, and `Auditing Guidelines`.
   - **`ai-caiq` mode:** `Shared Implementation Guidelines`, `Implementation Guidelines for Model Provider (MP)`, `...Orchestrated Service Provider (OSP)`, `...Application Provider (AP)`, `...AI Customer (AIC)`, `Cloud Service Provider (CSP)`, and the five role-specific `Auditing Guidelines for ...` columns.

   If a Control ID is not in the reference file, say so for that row rather than guessing guideline text.

5. **Mechanical pre-scoring.** Apply these rules before any judgment-based scoring, exactly and without interpretation:
   - An implementation-description or responsibilities answer is **auto-scored 0** if it is blank, 1–2 ASCII characters, or just "yes"/"no" (with optional punctuation).
   - **SSRM Control Ownership** is mandatory. It is auto-scored 0 if blank (unless the CAIQ answer for that row is `NA`, in which case a blank ownership is acceptable and not scored) or if it is not one of these valid values (case-insensitive exact match, no aliases, no fuzzy matching):
     - `caiq` mode: `CSP-owned`, `CSC-owned`, `Shared CSP and CSC`, `Shared CSP and 3rd-party`, `3rd-party outsourced`, `Not Determined`.
     - `ai-caiq` mode: `Owned by CSP`, `Owned by MP`, `Owned by OSP`, `Owned by AP`, `Owned by AIC`, `Shared Across the Supply Chain`, `Shared CSP-MP`, `Shared by MP-OSP`, `Shared OSP-AP`, `Shared AP-AIC`, `Not Determined`.

       <!-- valid-ai-ted-scorer: begin A-01 -->
       > **Plugin fix A-01** (amends step 5's "no aliases", published line 37, and the `ai-caiq` list, published line 39; see `DEVIATIONS.md`): also accept `Shared MP-OSP`, the spelling in CSA's AI-CAIQ drop-down, and keep accepting `Shared by MP-OSP`. They are one value. Line 37's "no aliases" does not apply to this one pair; every other value is matched exactly as line 37 says. Never advise a member to change one spelling into the other.
       <!-- valid-ai-ted-scorer: end A-01 -->
   - Whether the CSP/Service Provider description and the CSC/Service Customer description are *required* for a row depends on ownership. The provider-side answer is required when ownership is CSP-owned, Shared CSP and CSC, Shared CSP and 3rd-party, or 3rd-party outsourced. The customer-side answer is required when ownership is CSC-owned, Shared CSP and CSC, Shared CSP and 3rd-party, or 3rd-party outsourced. If ownership is missing or unparseable, require both.

     <!-- valid-ai-ted-scorer: begin ruling-20 -->
     > **Plugin fix, ruling 20** (amends step 5's required-description rule, published line 40; see `DEVIATIONS.md`): line 40's lists are the `caiq`-mode table. In `ai-caiq` mode, the Service Provider description is required for every valid ownership value except `Not Determined`; the Service Customer description is required only for `Owned by AIC`, `Shared AP-AIC` and `Shared Across the Supply Chain`; and `Not Determined` requires neither. Line 40's last sentence ("If ownership is missing or unparseable, require both") applies in both modes. A required description that fails step 5's first rule (blank, 1–2 characters, or just "yes"/"no") zeroes the row, as step 5 says. A description that the mode's table does not require may be blank or short without a mechanical 0: the row goes to AI scoring, where empty content scores 0 under step 6.
     <!-- valid-ai-ted-scorer: end ruling-20 -->
   - For a row that fails mechanically, skip AI scoring. Its overall `Score` is its `CSP/Service Provider Implementation Description Score` (0), capped at 2 if the answer is "No". `Score Justification` = "Final score based on Implementation Description Score (0)". `Readability Feedback` = "None".

6. **AI scoring.** For every row that passed mechanical pre-scoring, reason exactly as the prompt set instructs. Apply, concatenated in this order: `prompts/{mode}/instruction_prompt.md`, then `prompts/{mode}/output_prompt.md`, then "Expected Output Format:", then `prompts/{mode}/output_format.md`, then `prompts/{mode}/data_prompt.md`, then the row's data (answer, ownership, descriptions, enriched guideline text, control and domain context).

   Core rules (do not deviate):
   - The scale is **0–4** for every component and for the overall score.
   - **A "No" answer caps every score for that row at 2**, however well written the explanation is.
   - **A major contradiction between the stated answer and the explanation** (for example "Yes" with "we do not implement this") scores **0** for the affected component, or for the whole row if it invalidates the response. This is separate from, and more severe than, the "No" cap.
   - 0 = fails, non-compliant, major contradiction or empty; 1 = weak or minimal; 2 = basic or partial (also the ceiling for "No"); 3 = strong, meets expectations; 4 = excellent, exceeds expectations.
   - "NA" answers can still reach 4 if the justification is thorough.
   - If a score would fall outside 0–4, clamp it into range. If a score would be non-numeric or uncertain, use 2 rather than leaving it blank.
   - Produce, per row (use the AI-CAIQ field names in `ai-caiq` mode; accept "Service Customer Responsibilities" with either one or two spaces before "Responsibilities", since the prompt files use both):
     - `SSRM Control Ownership Score` and justification (internal only; not written to the workbook, see step 8).
     - `CSP Implementation Description Score` / `Service Provider Implementation Description Score`, with score justification, feedback and feedback justification.
     - `CSC Responsibilities Feedback` / `Service Customer Responsibilities Feedback`, with feedback justification. Only the feedback text goes to the workbook, not a separate numeric score.
     - Overall `Score` and `Score Justification`: a holistic blend of the components, adjusted for contradictions. There is no fixed weighting formula.
     - `Readability Feedback`: clarity, grammar and organization. It does not affect the numeric scores.

7. **Aggregate per domain** (group by `CCM Domain Title` / `AICM Domain Title`): `total_questions`, `pass_count` (Score ≥ 2), `fail_count` (Score < 2), `average_score` (plain unweighted mean of `Score`, NA rows included), `percentage_score` = average / 4 × 100, `pass_status` = percentage_score ≥ 50%. The overall score is the unweighted mean of all row scores, expressed the same way.

   <!-- valid-ai-ted-scorer: begin ruling-08 -->
   > **Plugin note, ruling 08** (clarifies step 7's "`pass_status` = percentage_score ≥ 50%", published line 59; it changes nothing; see `DEVIATIONS.md`): compare the unrounded percentage with 50%, and round only for display. The overall score is the plain mean of all row scores, as line 59 says, not a mean of the domain scores.
   <!-- valid-ai-ted-scorer: end ruling-08 -->

   **Explain what PASS means.** A well-written "No" scores 2/4 = 50%, so a domain answered entirely with well-written "No" responses shows as PASS. PASS/FAIL here measures response quality and coherence, not implementation, independent evidence or compliance. Say this plainly when presenting results.

8. **Write the scored workbook (.xlsx)** with exactly these columns, in this order:

   **`caiq` mode:**
   `Question ID, Question, CSP CAIQ Answer, SSRM Control Ownership, CSP Implementation Description (Optional/Recommended), CSP Implementation Description Score, CSP Implementation Description Score Justification, CSP Implementation Description Feedback, CSP Implementation Description Feedback Justification, CSC Responsibilities (Optional/Recommended), CSC Responsibilities Feedback, CSC Responsibilities Feedback Justification, CCM Control ID, CCM Control Specification, CCM Control Title, CCM Domain Title, Cloud Service Provider Implementation Guidelines (CSP), Cloud Service Consumer Implementation Guidelines (CSC), Auditing Guidelines, Score, Score Justification, Readability Feedback`

   **`ai-caiq` mode:**
   `Question ID, Question, Service Provider CAIQ Answer, SSRM Control Ownership, Service Provider Implementation Description (Optional/Recommended), Service Provider Implementation Description Score, Service Provider Implementation Description Score Justification, Service Provider Implementation Description Feedback, Service Provider Implementation Description Feedback Justification, Service Customer Responsibilities (Optional/Recommended), Service Customer Responsibilities Feedback, Service Customer Responsibilities Feedback Justification, AICM Control ID, AICM Control Specification, AICM Control Title, AICM Domain Title, Shared Implementation Guidelines, Implementation Guidelines for Model Provider (MP), Implementation Guidelines for Orchestrated Service Provider (OSP), Implementation Guidelines for Application Provider (AP), Implementation Guidelines for AI Customer (AIC), Cloud Service Provider (CSP), Auditing Guidelines for Application Provider (AP), Auditing Guidelines for Orchestrated Services Provider (OSP), Auditing Guidelines for Model Provider (MP), Auditing Guidelines for AI Customer (AIC), Auditing Guidelines for Cloud Service Provider (CSP), Score, Score Justification, Readability Feedback`

   Do not write any "Normalized" column, the `SSRM Control Ownership Score` or its justification, or a numeric CSC/Service Customer score or its justification.

   Add a second sheet named `About` with: `Scorer: CSA Valid-AI-ted Scorer`, `Package version: 1.1.0`, `Prompt set: 1.0.0`, the mode, the confirmed framework version, the date, and the disclaimer text from step 9.

   <!-- valid-ai-ted-scorer: begin outputs -->
   > **Plugin addition: outputs** (amends step 8's `About` fields, published line 73, and step 9's page 1 and final page, published lines 76 and 79–82; see `DEVIATIONS.md`): add two rows to the `About` sheet, after the published ones:
   > - `Plugin: valid-ai-ted-scorer 1.0.1`
   > - `Plugin fixes applied: A-01, A-02, A-03, A-05, A-15, A-25, ruling 20; reference data added for CCM 4.1.1, AICM 1.0.3, AICM 1.1.0 (published text) and AICM 1.1.1 (see DEVIATIONS.md)`
   >
   > On the PDF's final page, put the same two lines after the disclaimer. The disclaimer itself stays word for word, and the footer stays `CSA Valid-AI-ted Scorer v1.1.0`.
   >
   > The `**` marks in step 9's disclaimer are Markdown bold, not text. In the `About` sheet, in a CSV and in any other plain-text output, write the disclaimer without them; in the PDF the phrase may be bold, and in the Markdown fallback report the marks may stay. The words stay exactly as published.
   >
   > On page 1, the questionnaire version field is the prefix and the number only: `CAIQ: 4.1.0` or `AI-CAIQ: 1.1.0`, for every variant. For a CAIQ-Lite, write `CAIQ: 4.1.0`, and say "CAIQ-Lite" in the first overview paragraph.
   <!-- valid-ai-ted-scorer: end outputs -->

9. **Write the summary report (PDF)** in this layout and order:
   - **Page 1: title and overview.** Title: `CAIQ / CCM Scoring Report` (`caiq` mode) or `AI-CAIQ / AICM Scoring Report` (`ai-caiq` mode). Two-column metadata: left = Organization (if known), Score (overall %), Status (PASS/FAIL), Date; right = Cloud Service (if known), spec version (`CCM:`/`AICM:` + version), questionnaire version (`CAIQ:`/`AI-CAIQ:` + version). Then 3–4 paragraphs: the overall average and percentage, the highest- and lowest-scoring domains (named, with their %), and constructive, strategic recommendations written from the actual numbers.
   - **Page 2: domain score visualization.** A horizontal bar chart with one bar per domain showing its percentage score (0–100%). Bars are **green (#4CAF50) if the domain passes (≥ 50%), red (#F44336) if not**, with a dashed threshold line labelled 50%, a caption explaining the chart and a small pass/fail legend.
   - **Page 3 onward: control domain breakdown.** One block per domain, not split across a page break: the domain name as a sub-heading; a row of stats (Total Questions, Passing Scores ≥ 2, Failing Scores < 2); a second row (Avg. Score /4, Score %, Status PASS/FAIL in green/red); then 1–3 sentences on strengths and 1–2 concrete improvement suggestions, grounded in that domain's actual `Readability Feedback` and `Score Justification` text.
   - **Final page: disclaimer.** Use exactly this wording:

     > **Disclaimer:**
     > This is an informational scoring report generated with the CSA Valid-AI-ted Scorer (package version 1.1.0), an AI-assisted application of the Cloud Security Alliance's Valid-AI-ted scoring methodology run in the user's own AI assistant. It evaluates a self-submitted CAIQ/AI-CAIQ and is **not an official CSA report, certification, audit, or formal attestation** of compliance with any regulatory, legal, or industry standard requirements (e.g., ISO/IEC 27001, SOC 2, HIPAA, GDPR, etc.). It does not confer, imply, or represent an "AI Verified" badge, a STAR Registry listing or any other CSA-issued status, and does not imply endorsement, approval, or validation by the Cloud Security Alliance of any organization's security posture. Organizations remain solely responsible for ensuring their security, privacy, and compliance obligations are met. This report carries no warranty and no liability is assumed for decisions made based on it.

   Put `CSA Valid-AI-ted Scorer v1.1.0` in the footer of every page. Build the workbook and PDF with whatever spreadsheet and document tools are available; the content and layout above are what matter, not a particular library.

## Rules

- Never skip mechanical pre-scoring, and never let judgment override a mechanical 0.
- Never let a "No" answer's component or overall score exceed 2, and never let an answer-versus-explanation contradiction escape a 0.
- Never present the output as an official CSA report, audit, certification, STAR listing or badge. Always include the disclaimer above, verbatim, as the final page.
- If the uploaded file is missing columns the pipeline needs (for example no Control ID to enrich against), say exactly what is missing rather than inventing guideline text or scores.
- If the user asks which version of the scorer they are using, answer with the package version, prompt set and frameworks listed at the top of this file, and mention that the latest version and installation guide are available from the Cloud Security Alliance.

<!-- valid-ai-ted-scorer: begin guidance -->
## Plugin guidance: the files you make

*Added by the plugin `valid-ai-ted-scorer`. This is guidance, not a requirement of the method.*

- **A mechanical 0 is final.** It is the method's rule (step 5), not a judgment. Never offer to re-score it, never call the rule unclear, and never give the score a row or the questionnaire would have had without it. If the member disagrees, explain the rule that zeroed the row (see Help) and say that a changed answer or description would be scored afresh.
- **The files are for the member's own use**, not for distribution. CSA's official report comes from CSA's own service; these files are an informational, AI-assisted assessment of the written responses, produced by the member's AI assistant. Say so when you hand them over.
- **The member chooses the accessibility level.** By default, make the files with whatever tools are already here, as step 9 says. If the member wants an accessible PDF, for example for a screen-reader user, offer the findings of CSA's Document Pipeline bake-off. Its report is internal to CSA, so its findings are given here in full:
  - Typst and WeasyPrint both passed PDF/UA-1 with 0 veraPDF failures on the bake-off's template. Typst is a single ~17 MB binary whose output is byte-identical from run to run; WeasyPrint's output is not, and it needs Python with the pango and cairo libraries.
  - Chrome/Puppeteer failed PDF/UA-1 (6 rules), and Quarto/LaTeX needs "a GB-scale TeX toolchain".
  - veraPDF "covers ~89 of 136 Matterhorn checkpoints", so it is machine validation only. The bake-off tested its own template, not a file you write: never call a PDF you make "accessible" or "PDF/UA" unless it was validated.
- **Never install anything without asking.** Say what you would install and why, and accept a "no".
- **Fallback, per file.** Python's standard library can write both a `.xlsx` (a zip of XML files) and a simple PDF, so try it before falling back. A refused or missing tool is not a reason to fall back while the standard library remains. Only for a file that nothing here can make, and only after the member declines an install, write that file's fallback, and say plainly why. A member may get a workbook and a fallback report, or the reverse:
  - for the workbook, `<input name>_scored.csv`, with the workbook's columns in step 8's order;
  - for the report, `<input name>_scoring_report.md`, with the report's sections in step 9's order, the `About` fields at the top and the disclaimer word for word at the end;
  - each file's first line says that it is a fallback, and why the `.xlsx` or the PDF could not be made here;
  - in the CSV, a cell that starts with `=`, `+`, `-` or `@` gets a leading apostrophe (`'`), so that a spreadsheet cannot run it as a formula;
  - never call these files the workbook or the report: they are a fallback CSV and Markdown report.
- **Working files.** Put every intermediate file (scripts, JSON, scratch tables) in one new folder **beside the questionnaire**, named after it: `<input name>_work/`. If that name is taken, add a number. Never use a system temporary folder (`/tmp`, `$TMPDIR`, `%TEMP%`), the home folder, or any folder above the questionnaire's, and never a fixed path. If the questionnaire's folder cannot be written to, ask the member for a folder. If you cannot ask, use the session's own working folder, provided it is none of the folders above, and say so. Nothing that holds questionnaire content goes anywhere else. At the end, remove the folder if you can. If you cannot, say so, give its full path, and name every file in it that holds the member's answers.
- **File names:** `<input name>_scored.xlsx` and `<input name>_scoring_report.pdf`, beside the questionnaire. "Never overwrite" protects files that were there before you started: if one of these names is taken by such a file, choose a new name. Build and check drafts in the working folder, and write each final file beside the questionnaire once, after it is checked. A file you wrote in this session may be replaced, but never leave a superseded or wrong draft beside the questionnaire.
- **Counts.** Take every count you report, in your reply and in the PDF, from the workbook you wrote, once it is finished, never from an earlier step. The automatic zeros are the rows whose `Score Justification` is "Final score based on Implementation Description Score (0)"; the zeros overall are the rows whose `Score` is 0. A row that passes the mechanical checks can still be scored 0, so the two numbers can differ. Count again after any change.
- **Running code.** Run Python by name: `python3`, `python`, or `py` on Windows. If running Python is refused because of how it was named (by path, or a virtual environment's interpreter), try one of these names before asking the member. A refusal of anything else is the member's decision: do not do the same thing another way. Writing the working folder's first file with your file-writing tool, which creates the folder, is how the working-files bullet above asks you to make it; it is not a way around a refused `mkdir`.
<!-- valid-ai-ted-scorer: end guidance -->

<!-- valid-ai-ted-scorer: begin help -->
## Help

*Added by the plugin `valid-ai-ted-scorer`. Use it to answer the member's questions.*

**How to use it.** Attach or point to a completed CAIQ or AI-CAIQ workbook, and ask for it to be scored. Confirm the questionnaire version when asked. The result is a scored workbook and a summary PDF (or the fallback files above, if those cannot be made here). PASS means the responses average at least 2 of 4: it is about the quality and coherence of the written responses, not about whether controls are in place (step 7). A blank description scores 0, even where CSA's template marks it optional.

**"Why did this row score 0?"**
- For a row that failed mechanically, the workbook cannot say why: step 5 gives every such row the same justification, "Final score based on Implementation Description Score (0)". Re-derive the reason from the row's own values (its answer, its ownership and its two descriptions) under step 5 and the ruling 20 block, and name the rule that zeroed it. This is rule-based; it is not a re-judgment. A mechanical 0 is final: never offer to re-score it (see the guidance block).
- For a row the model judged, explain it from its recorded justification only. Never re-score it.

**Known issues.**
- Two published rules are kept as written (ruling 01). For `3rd-party outsourced` and `Shared CSP and 3rd-party`, the customer description is required, so a blank one zeroes the row although CSA's template marks it optional. And an `NA` answer with a blank ownership requires both descriptions.
- A score the model is unsure of becomes 2, which counts as a pass (step 6).
- The package's own AICM 1.1.0 file is a pre-publication text: 63 cells in 20 controls differ from CSA's published AICM 1.1.0 (`DEVIATIONS.md`, A-05). This plugin scores an AI-CAIQ stamped AICM 1.1.0 against CSA's published text (`AICM-1.1.0-published-merged.csv`) instead, and keeps the package's file unchanged.
- Four reference files are this plugin's additions, generated from CSA's workbooks (`reference/VERSION.txt`); they are not part of CSA's published package.
- A CAIQ v4.0.x names no CCM version. It is scored against CCM 4.0.13, CSA's last CCM v4.0, whose control text is what those questionnaires carry.
- A session that cannot ask questions, such as a non-interactive run, has been observed to skip the version confirmation. The rule is still to confirm before scoring.
- The scores of judged rows vary between runs, and on a full questionnaire the feedback can turn generic. Do not compare scores from different runs as if they were exact.
- Organization and Cloud Service come only from the member: ask, or leave them blank.
- Cost: measured on 2026-10-23 with `claude-opus-5-5` at effort `xhigh` (macOS) and at the default effort (Windows), at list-price equivalent. A seeded file of about 25 questions cost $1.52 to $3.19; a full CAIQ (261 or 283 questions), $1.80 to $9.63; the full AI-CAIQ (320 questions), $2.38 to $17.48. A full file's cost can vary several-fold between runs, settings and models.

**Which version.** Plugin `valid-ai-ted-scorer` 1.0.1; CSA's Valid-AI-ted Scorer package 1.1.0; scoring prompt set 1.0.0; reference data CCM 4.0.13, 4.1.0 and 4.1.1, and AICM 1.0.2, 1.0.3, 1.1.0 (the package's pre-publication text, and CSA's published text) and 1.1.1 (CCM 4.1.1, AICM 1.0.3, the published AICM 1.1.0 and AICM 1.1.1 added by the plugin); plugin fixes A-01, A-02, A-03, A-05, A-15, A-25 and ruling 20. Give all of this when the member asks which version they are using (it adds to the last of the published rules).

**Reporting a problem without sharing the questionnaire.**
- Give the file type and questionnaire version, the number of questions, the plugin version, the step where it went wrong, and the Question IDs involved.
- Never include answers, descriptions, justifications or the organization's name.
- Claude Code's `/bug` sends the whole session, questionnaire included, to Anthropic, not to CSA.
- Where: an issue in `CloudSecurityAlliance/csa-plugins-official` with `[valid-ai-ted-scorer]` at the start of its title (see the plugin's `FEEDBACK.md`). Report a security problem privately, through that repository's private vulnerability reporting, never in a public issue.
<!-- valid-ai-ted-scorer: end help -->

<!-- valid-ai-ted-scorer: begin provenance -->
## Where this copy comes from

*Added by the plugin `valid-ai-ted-scorer`.*

- Outside the marked blocks, this file is CSA's published `SKILL.md` from the Valid-AI-ted Scorer package 1.1.0 (`caiq-scorer-v1.1.0.zip`, SHA-256 `ae37c946e734030d90c30ae911955ed6e3136135715f1b6223fefcacf7770334`), unchanged: removing every marked block gives that file byte for byte. `VERSION`, `CHANGELOG.md`, `prompts/` and the four published reference files are that package's, byte for byte.
- `reference/CCM-4.1.1-merged.csv`, `AICM-1.0.3-merged.csv`, `AICM-1.1.0-published-merged.csv` and `AICM-1.1.1-merged.csv` are the plugin's additions. `reference/VERSION.txt` gives the source, row count and SHA-256 of every reference file.
- The scoring method, the prompts and the reference data are CSA's. Corrections to them go to CSA (see the plugin's `README.md`); the plugin's own fixes are listed in its `DEVIATIONS.md`.
- Licence: the plugin's own files, these added sections included, are under the Apache License 2.0. CSA's published `SKILL.md` text and the scoring prompts are © Cloud Security Alliance, all rights reserved. The CCM and AICM data is under CSA's notices, in `reference/NOTICE-CCM.txt` and `reference/NOTICE-AICM.txt`. The plugin's `NOTICE` has the details.
<!-- valid-ai-ted-scorer: end provenance -->
