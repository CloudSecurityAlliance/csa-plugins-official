# CSA Valid-AI-ted Scorer: changelog

## 1.1.0 (October 2026)
- Prepared for customer distribution: removed internal engineering notes and references to skills customers don't have.
- Added a package version marker (`VERSION`, SKILL.md metadata). The version now appears in the report footer, the disclaimer and an `About` sheet in the scored workbook.
- Questionnaires that declare a framework version this package has no reference data for are now flagged instead of being scored against another version.
- Disclaimer reworded for a CSA-published package; it also says the report is not a STAR Registry listing.
- Packaging: the skill now sits in a `caiq-scorer/` folder inside the ZIP, as Claude's skill upload expects.
- No changes to the scoring prompts (prompt set 1.0.0) or the CCM/AICM reference data.

## 1.0.0 (October 2026)
- First release.
