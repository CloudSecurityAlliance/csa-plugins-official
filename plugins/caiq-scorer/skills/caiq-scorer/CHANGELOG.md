# CSA Valid-AI-ted Scorer: changelog

## 1.1.1 (October 2026)
- Framework version detection: CAIQ and CCM/AICM versions are now treated separately. A1 JSON `specification_version` is used when present; otherwise the questionnaire's release line maps to a reference file (CAIQ 4.0.x to CCM 4.0.13, CAIQ 4.1.x to CCM 4.1.0, AI-CAIQ 1.0.x to AICM 1.0.2, AI-CAIQ 1.1.x to AICM 1.1.0). The file is used only if every control ID and title matches, and the user still confirms. Previously a CAIQ v4.0.2 was refused although its controls match CCM 4.0.13 exactly.
- Only rows with a Question ID like `A&A-01.1` count as questions, so the "End of Standard" and copyright rows are no longer counted.
- Outputs are saved next to the input as `<name>_scored.xlsx` and `<name>_scoring_report.pdf`; working files go in a temporary directory that is deleted afterwards.
- Lists compatible Python libraries for each job (reading .xlsx, writing .xlsx, writing the PDF), uses whichever is installed, and asks before installing anything.
- No changes to the scoring prompts (prompt set 1.0.0) or the CCM/AICM reference data.

## 1.1.0 (October 2026)
- Prepared for customer distribution: removed internal engineering notes and references to skills customers don't have.
- Added a package version marker (`VERSION`, SKILL.md metadata). The version now appears in the report footer, the disclaimer and an `About` sheet in the scored workbook.
- Questionnaires that declare a framework version this package has no reference data for are now flagged instead of being scored against another version.
- Disclaimer reworded for a CSA-published package; it also says the report is not a STAR Registry listing.
- Packaging: the skill now sits in a `caiq-scorer/` folder inside the ZIP, as Claude's skill upload expects.
- No changes to the scoring prompts (prompt set 1.0.0) or the CCM/AICM reference data.

## 1.0.0 (October 2026)
- First release.
