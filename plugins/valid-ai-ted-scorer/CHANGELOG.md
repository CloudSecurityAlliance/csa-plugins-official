# valid-ai-ted-scorer: changelog

This is the plugin's changelog. `skills/caiq-scorer/CHANGELOG.md` is CSA's changelog for the published package, kept
unchanged.

## 1.0.1 (2026-10-23; first public release, in `csa-plugins-official`)

A fix release from release 1.0.0's test runs. CSA's method, prompts and data are unchanged; every change is in the
plugin's own marked blocks or its other files, and the count of marked blocks stays 15. The README's "Changes in
1.0.1" lists each change.

## 1.0.0 (2026-10-23; CSA's internal plugin marketplace only)

- First version: CSA's published Valid-AI-ted Scorer package 1.1.0 (`caiq-scorer-v1.1.0.zip`) as a Claude Code plugin.
  The skill is `caiq-scorer`, as published. The prompts, the four reference files, `VERSION` and the package's
  `CHANGELOG.md` are unchanged, and so is the published `SKILL.md` text outside the plugin's marked blocks.
- Seven documented fixes, as marked blocks in `SKILL.md`: A-01, A-02, A-03, A-05, A-15, A-25 and ruling 20. See
  `DEVIATIONS.md`.
- Reference data for every CAIQ and AI-CAIQ release CSA publishes (CSA's decision of 2026-10-22: support every
  current version of the CAIQ, and record which CCM or AICM version each maps to). Added `reference/CCM-4.1.1-merged.csv`,
  `AICM-1.0.3-merged.csv`, `AICM-1.1.0-published-merged.csv` (CSA's published AICM 1.1.0) and `AICM-1.1.1-merged.csv`,
  each generated from CSA's workbook. The A-02 block's table says which file each questionnaire uses. See
  `reference/VERSION.txt`.
- Added CSA's notice for each shipped CCM and AICM version, word for word: `reference/NOTICE-CCM.txt` and
  `reference/NOTICE-AICM.txt`.
- Added guidance (the files are for your own use; the accessibility level is your choice; nothing is installed without
  asking; a fallback CSV and Markdown report; one working folder), built-in help, and two `About` rows naming the
  plugin and its fixes.
- No scripts: the AI applies the rules and writes the files, as the published package does.
