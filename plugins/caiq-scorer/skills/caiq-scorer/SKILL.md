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

The result is an **informational, AI-assisted assessment** of the quality and internal consistency of the written responses. It does not verify that controls are implemented, and it is not a CSA certification, audit, attestation, STAR Registry listing or Valid-AI-ted badge. Every report must carry the disclaimer in step 9.

## Pipeline

1. **Detect mode.** Read the uploaded file. If it has CAIQ/CCM-style columns (`CSP CAIQ Answer`, `SSRM Control Ownership`, `CSP Implementation Description...`, `CCM Control ID`, `CCM Domain Title`), the mode is **`caiq`**. If it has AI-CAIQ/AICM-style columns (`Service Provider CAIQ Answer` or AICM-specific guideline columns, `AICM Control ID`/`AICM Domain Title`), the mode is **`ai-caiq`**. If cell A1 contains JSON metadata naming the specification (`"specification_name"`), use it to confirm. If the mode is still ambiguous, ask the user.

2. **Detect the framework version** (CCM 4.0.13 or 4.1.0; AICM 1.0.2 or 1.1.0) from the cell A1 metadata or the filename, then **ask the user to confirm which version applies before enriching. Never silently default to a version.** If the questionnaire declares a version not listed above, tell the user this package does not include reference data for it and that a newer version of the scorer may be available from CSA; do not substitute a different version's guideline text.

   **AICM only:** control IDs are *not* stable between AICM 1.0.x and 1.1.x. Of the 242 control IDs shared by the two reference files, 65 have a different `Control Title` (for example, `AIS-08` is "Input Validation" in 1.0.2 but "API Security" in 1.1.0). Using the wrong file attaches wrong guideline text with no visible error. Enrich only from the reference file that matches the confirmed version; never mix them.

3. **Normalize.** Treat answers as `Yes`/`No`/`NA` (case- and whitespace-insensitive). Preserve a literal "NA"; never confuse it with a blank or missing answer.

4. **Enrich each row.** Look up the row's Control ID in the matching `reference/*.csv` by exact match on the `Control ID` column, and attach:
   - **`caiq` mode:** `CSP` as *Cloud Service Provider Implementation Guidelines (CSP)*, `CSC` as *Cloud Service Consumer Implementation Guidelines (CSC)*, and `Auditing Guidelines`.
   - **`ai-caiq` mode:** `Shared Implementation Guidelines`, `Implementation Guidelines for Model Provider (MP)`, `...Orchestrated Service Provider (OSP)`, `...Application Provider (AP)`, `...AI Customer (AIC)`, `Cloud Service Provider (CSP)`, and the five role-specific `Auditing Guidelines for ...` columns.

   If a Control ID is not in the reference file, say so for that row rather than guessing guideline text.

5. **Mechanical pre-scoring.** Apply these rules before any judgment-based scoring, exactly and without interpretation:
   - An implementation-description or responsibilities answer is **auto-scored 0** if it is blank, 1–2 ASCII characters, or just "yes"/"no" (with optional punctuation).
   - **SSRM Control Ownership** is mandatory. It is auto-scored 0 if blank (unless the CAIQ answer for that row is `NA`, in which case a blank ownership is acceptable and not scored) or if it is not one of these valid values (case-insensitive exact match, no aliases, no fuzzy matching):
     - `caiq` mode: `CSP-owned`, `CSC-owned`, `Shared CSP and CSC`, `Shared CSP and 3rd-party`, `3rd-party outsourced`, `Not Determined`.
     - `ai-caiq` mode: `Owned by CSP`, `Owned by MP`, `Owned by OSP`, `Owned by AP`, `Owned by AIC`, `Shared Across the Supply Chain`, `Shared CSP-MP`, `Shared by MP-OSP`, `Shared OSP-AP`, `Shared AP-AIC`, `Not Determined`.
   - Whether the CSP/Service Provider description and the CSC/Service Customer description are *required* for a row depends on ownership. The provider-side answer is required when ownership is CSP-owned, Shared CSP and CSC, Shared CSP and 3rd-party, or 3rd-party outsourced. The customer-side answer is required when ownership is CSC-owned, Shared CSP and CSC, Shared CSP and 3rd-party, or 3rd-party outsourced. If ownership is missing or unparseable, require both.
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

   **Explain what PASS means.** A well-written "No" scores 2/4 = 50%, so a domain answered entirely with well-written "No" responses shows as PASS. PASS/FAIL here measures response quality and coherence, not implementation, independent evidence or compliance. Say this plainly when presenting results.

8. **Write the scored workbook (.xlsx)** with exactly these columns, in this order:

   **`caiq` mode:**
   `Question ID, Question, CSP CAIQ Answer, SSRM Control Ownership, CSP Implementation Description (Optional/Recommended), CSP Implementation Description Score, CSP Implementation Description Score Justification, CSP Implementation Description Feedback, CSP Implementation Description Feedback Justification, CSC Responsibilities (Optional/Recommended), CSC Responsibilities Feedback, CSC Responsibilities Feedback Justification, CCM Control ID, CCM Control Specification, CCM Control Title, CCM Domain Title, Cloud Service Provider Implementation Guidelines (CSP), Cloud Service Consumer Implementation Guidelines (CSC), Auditing Guidelines, Score, Score Justification, Readability Feedback`

   **`ai-caiq` mode:**
   `Question ID, Question, Service Provider CAIQ Answer, SSRM Control Ownership, Service Provider Implementation Description (Optional/Recommended), Service Provider Implementation Description Score, Service Provider Implementation Description Score Justification, Service Provider Implementation Description Feedback, Service Provider Implementation Description Feedback Justification, Service Customer Responsibilities (Optional/Recommended), Service Customer Responsibilities Feedback, Service Customer Responsibilities Feedback Justification, AICM Control ID, AICM Control Specification, AICM Control Title, AICM Domain Title, Shared Implementation Guidelines, Implementation Guidelines for Model Provider (MP), Implementation Guidelines for Orchestrated Service Provider (OSP), Implementation Guidelines for Application Provider (AP), Implementation Guidelines for AI Customer (AIC), Cloud Service Provider (CSP), Auditing Guidelines for Application Provider (AP), Auditing Guidelines for Orchestrated Services Provider (OSP), Auditing Guidelines for Model Provider (MP), Auditing Guidelines for AI Customer (AIC), Auditing Guidelines for Cloud Service Provider (CSP), Score, Score Justification, Readability Feedback`

   Do not write any "Normalized" column, the `SSRM Control Ownership Score` or its justification, or a numeric CSC/Service Customer score or its justification.

   Add a second sheet named `About` with: `Scorer: CSA Valid-AI-ted Scorer`, `Package version: 1.1.0`, `Prompt set: 1.0.0`, the mode, the confirmed framework version, the date, and the disclaimer text from step 9.

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
