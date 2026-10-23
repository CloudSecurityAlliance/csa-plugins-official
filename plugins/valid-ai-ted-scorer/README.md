# Valid-AI-ted Scorer

Scores a completed CAIQ (CCM) or AI-CAIQ (AICM) questionnaire question by question, on a 0–4 scale, using the
Cloud Security Alliance's Valid-AI-ted scoring method. It writes a scored Excel workbook and a summary PDF with domain
roll-ups.

The plugin is the published method (CSA's Valid-AI-ted Scorer package 1.1.0) with seven documented fixes, and reference
data added so that every CAIQ and AI-CAIQ release CSA publishes is scored against the CCM or AICM version it pairs
with. Its result is **an informational, AI-assisted assessment of the written responses**, produced by your AI
assistant.

## Install

In Claude Code:

```
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
/plugin install valid-ai-ted-scorer@csa-plugins-official
```

## What it is not

It does not verify that any control is implemented. It is not a CSA certification, audit, attestation, STAR Registry
listing or Valid-AI-ted badge, and it does not replace CSA's own service. The files it writes are for your own use, not
for distribution. Every report carries CSA's disclaimer.

## Use

Attach or point to a completed CAIQ or AI-CAIQ workbook (for example one downloaded from the STAR Registry), and ask
for it to be scored. For example:

> Score this completed questionnaire with the Valid-AI-ted Scorer, and produce the scored workbook and summary PDF.

The skill proposes the reference data from your questionnaire's version, and **asks you to confirm it** before it
scores. It then writes `<your file>_scored.xlsx` and `<your file>_scoring_report.pdf`, and never overwrites a file that was there before it started.

**PASS** means the responses average at least 2 of 4. It measures the quality and coherence of what was written, not
whether controls are in place: a domain answered entirely with well-written "No" responses shows as PASS. A blank
description scores 0, even where CSA's template marks it optional.

**What it needs:** nothing beyond the plugin. Your AI assistant applies the rules and writes the files with whatever
spreadsheet and PDF tools are already on your machine, Python's standard library included. It never installs anything
without asking. If one of the files still cannot be made and you decline an install, it writes that file's fallback
instead, a CSV for the workbook or a Markdown report for the PDF, and says why.

The skill has built-in help: ask it why a row scored 0, which version you are using, or how to report a problem.

## Fixes in this plugin

The published method is followed as written, except for seven documented fixes. Each is a marked block in
`skills/caiq-scorer/SKILL.md`, beside the sentence it amends. [`DEVIATIONS.md`](DEVIATIONS.md) gives each one's reason,
effect on scores and upstream report.

| Fix | What changes |
|---|---|
| A-01 | `Shared MP-OSP`, the spelling in CSA's AI-CAIQ drop-down, is accepted as well as the published `Shared by MP-OSP`. Rows using it are no longer zeroed. |
| A-02 | The version is read from the questionnaire's stamp (cell A1 of its `Introduction` sheet), and the reference data is proposed from a table covering every CAIQ and AI-CAIQ release (see below). You still confirm it. |
| A-03 | Only the questionnaire sheet is scored (row 2 holds its header); columns are found by name; merged Control ID and Domain Title cells take the value at the top of their range; the footer rows are not questions. |
| A-05 | Reference rows are matched on the Control ID only, so a title typo in the bundled data never refuses a row. |
| A-15 | `Service Provider AI-CAIQ Answer`, the header in CSA's AI-CAIQ templates, is read as the answer column. |
| A-25 | A byte-order mark at the start of a reference file is ignored. |
| Ruling 20 | Which descriptions each AI-CAIQ ownership value requires, as ruled by the method's owner. |

**Which questionnaires it scores, against which data.** The plugin reads the version from the questionnaire's stamp
and proposes the reference data CSA pairs with it:

| Your questionnaire | Its stamp | Reference data |
|---|---|---|
| CAIQ v4.0.1, v4.0.2 or v4.0.3 | `v4.0.x` | CCM 4.0.13, `CCM-4.0.13-merged.csv` (CSA's last CCM v4.0; 4.0.12 has the same text) |
| CAIQ v4.1.0, or CAIQ-Lite v4.1.0 | CCM 4.1.0 | CCM 4.1.0, `CCM-4.1.0-merged.csv` |
| CAIQ v4.1.0 (CSA's bundle of 2026-10-02) | CCM 4.1.1 | CCM 4.1.1, `CCM-4.1.1-merged.csv` (added) |
| AI-CAIQ 1.0.2 | AICM 1.0.2 | AICM 1.0.2, `AICM-1.0.2-merged.csv` |
| AI-CAIQ 1.0.2 (CSA's bundle of 2025-11-10) | AICM 1.0.3 | AICM 1.0.3, `AICM-1.0.3-merged.csv` (added) |
| AI-CAIQ 1.1.0 (CSA's bundle of 2026-06-18) | AICM 1.1.0 | AICM 1.1.0 as CSA published it, `AICM-1.1.0-published-merged.csv` (added) |
| AI-CAIQ 1.1.0 (CSA's current bundle) | AICM 1.1.1 | AICM 1.1.1, `AICM-1.1.1-merged.csv` (added) |

Two questionnaires cannot be scored by this method, and the plugin says so rather than guessing: CAIQ v3.x (for CCM
3.0.1), which has no ownership or description columns; and SSCF-CAIQ v1.0, the questionnaire of CSA's SaaS Security
Capability Framework, which has no ownership column and pairs with neither CCM nor AICM. The four
added files are the plugin's additions, generated from CSA's own workbooks in the package's format, and checked
against CSA's questionnaires and CSA's data service. [`reference/VERSION.txt`](skills/caiq-scorer/reference/VERSION.txt)
gives each one's source and checks.

**The package's own `AICM-1.1.0-merged.csv` ships unchanged, but is not used.** It is a pre-publication text of AICM
1.1.0 (A-05). An AI-CAIQ stamped AICM 1.1.0 is scored against CSA's published AICM 1.1.0
(`AICM-1.1.0-published-merged.csv`) instead, as CSA decided on 2026-10-22.

The workbook's `About` sheet and the PDF's last page name the plugin and these fixes.

## Accessibility

The files are for your own use, so you choose the level of accessibility you need. By default the assistant uses
whatever tools are installed. If you need an accessible PDF, for example for a screen-reader user, the assistant can
tell you what CSA's internal Document Pipeline bake-off found:
- the bake-off found Typst and WeasyPrint passed PDF/UA-1 on its template, with 0 veraPDF failures;
- Typst is a single ~17 MB binary with byte-identical output; WeasyPrint needs Python with the pango and cairo
  libraries;
- veraPDF covers about 89 of 136 Matterhorn checkpoints, so it is machine validation only.

The bake-off tested its own template, not a file your assistant writes. A PDF from this plugin is not accessible, or
PDF/UA, unless it has been validated.

## Known issues

- **Two published rules are kept as written** (the method's owner ruled to keep them). For `3rd-party outsourced` and
  `Shared CSP and 3rd-party`, a blank customer description scores the row 0, although CSA's template marks it optional.
  And an `NA` answer with a blank ownership requires both descriptions.
- **An uncertain score becomes 2**, which counts as a pass.
- **The package's own AICM 1.1.0 file is a pre-publication text, so it ships unchanged but is not used.** 63 cells in
  20 controls differ from CSA's published AICM 1.1.0 (`DEVIATIONS.md`, A-05). An AI-CAIQ stamped AICM 1.1.0 is scored
  against CSA's published text instead.
- **Four reference files are the plugin's additions**, generated from CSA's workbooks. They are not part of CSA's
  published package.
- **A CAIQ v4.0.x names no CCM version.** It is scored against CCM 4.0.13, CSA's last CCM v4.0, whose control text
  is what those questionnaires carry.
- **The version confirmation has been observed to be skipped** in a session that cannot ask questions, such as a
  non-interactive run. The rule is still to confirm before scoring.
- **Scores vary between runs.** Rows the model judges can score differently from one run to the next, and on a full
  questionnaire the feedback can turn generic. Don't compare scores from different runs as if they were exact.
- **Organization and Cloud Service** come only from you; the assistant asks, or leaves them blank.
- **Cost:** measured on 2026-10-23 with `claude-opus-5-5` at effort `xhigh` (macOS) and at the default effort
  (Windows), at list-price equivalent. A seeded file of about 25 questions cost $1.52 to $3.19; a full CAIQ (261 or 283
  questions), $1.80 to $9.63; the full AI-CAIQ (320 questions), $2.38 to $17.48. A full file's cost can vary several-fold
  between runs, settings and models.

## Versions

Plugin `valid-ai-ted-scorer` 1.0.1; CSA's Valid-AI-ted Scorer package 1.1.0; scoring prompt set 1.0.0; reference data
for CCM 4.0.13, 4.1.0 and 4.1.1, and AICM 1.0.2, 1.0.3, 1.1.0 and 1.1.1 (CCM 4.1.1, AICM 1.0.3, the published AICM
1.1.0 and AICM 1.1.1 added by the plugin).

The outputs carry `CSA Valid-AI-ted Scorer v1.1.0`, because 1.1.0 is the version of CSA's method and package. The
plugin's own version is 1.0.1, the version of its packaging and fixes.

## Changes in 1.0.1

Every change is in the plugin's own guidance, help and outputs blocks, and its other files; CSA's method, prompts and
data are unchanged. Each comes from release 1.0.0's test runs.

- Working files go in one folder beside the questionnaire, `<input name>_work/`, never in a system temporary folder,
  the home folder or a parent folder.
- A mechanical 0 is final: the assistant never offers to re-score it.
- Drafts are built and checked in the working folder; no superseded or wrong draft is left beside the questionnaire.
- The counts in the reply and the PDF are taken from the finished workbook.
- Python is run by name (`python3`, `python`, or `py` on Windows) before the assistant asks for help.
- The fallback applies per file, and only after Python's standard library has been tried.
- The `About` sheet's disclaimer is written without the Markdown `**` marks.
- Page 1's questionnaire version field is the number only, `CAIQ: 4.1.0` for a CAIQ-Lite too.
- The SSCF-CAIQ refusal does not suggest that CSA has another method for it.
- The measured cost, in the help and in "Known issues", and "What has been tested" below.
- The version is 1.0.1 throughout, so that a marketplace update replaces an installed 1.0.0.

## Your questionnaire and the AI model

Raw evidence never goes to CSA. When the plugin reads your evidence, it is processed by the AI model you run it with, under your agreement with that provider.

The assistant keeps its working files in one new folder beside your questionnaire, `<your file>_work/`. At the end it
removes the folder, or tells you where it is, since it holds your answers.

Your AI assistant also keeps its own records of the session, outside the plugin's control. Claude Code, for example,
stores session transcripts and large tool outputs under `~/.claude/projects/`, and these hold questionnaire content.
Delete them there if you need to.

## What has been tested

Every run was a headless Claude Code session (Claude Code 2.1.309, model `claude-opus-5-5`) on 2026-10-23. The test
questionnaires, checks and results are kept in CSA's internal test records.

- **1.0.1, macOS, 9 runs**, three at a time, at effort `xhigh`: six on a near-final build of 1.0.1 and three re-runs on
  its final guidance text. The inputs were seeded CAIQ, CAIQ-Lite and AI-CAIQ questionnaires with invented answers, an
  SSCF-CAIQ (refused, as it should be), a run with no spreadsheet or PDF library, and a real 283-question CAIQ from the
  STAR Registry. In every run that scored, the automatic zeros were exactly the expected rows and the working folder was
  beside the questionnaire; no run wrote a working file outside the questionnaire's folder.
- **1.0.0, macOS, 12 runs**, one at a time, at effort `xhigh`, and **1.0.0, Windows 11, 20 runs**: ten questionnaires,
  twice each, installed from CSA's internal plugin marketplace. In every run that scored, the automatic zeros were
  exactly the expected rows. What fell short was the handling of files and replies, which 1.0.1 fixes (see "Changes in
  1.0.1").

**Not tested:** 1.0.1 on Windows; Claude Desktop and claude.ai; an interactive Claude Code session (every run was
headless); Linux; models other than `claude-opus-5-5`; and the fallback CSV, which no run has needed.

## How to describe it

| Say | Don't say |
|---|---|
| "an informational, AI-assisted assessment of the written responses" | "official", "certified", "verified", "audit", "CSA report", "STAR listing", "badge" |
| "the published method (package 1.1.0) with seven documented fixes, and reference data added for every current CAIQ and AI-CAIQ" | "CSA's scorer" without "method"; "identical to the published scorer" |
| "produced by your AI assistant" | "produced by CSA" |
| "scores vary between runs" | "the same result every time", "repeatable", "deterministic" |
| "PASS means the responses average at least 2 of 4; it is not about whether controls are in place" | "you passed", "compliant" |

## Where it comes from

- **The method:** CSA's Valid-AI-ted Scorer package 1.1.0, from <https://labs.cloudsecurityalliance.org/valid-ai-ted-scorer/>
  (`caiq-scorer-v1.1.0.zip`, SHA-256 `ae37c946e734030d90c30ae911955ed6e3136135715f1b6223fefcacf7770334`). Its
  `SKILL.md`, prompts, `VERSION`, `CHANGELOG.md` and four reference files flow down unchanged; the plugin adds marked
  blocks to `SKILL.md`.
- **The engine:** the package's prompts and reference files are byte-identical to `engine/prompts/` and `engine/data/`
  in CSA's scoring engine (a private CSA repository), at commit `1cc171b`.
- **The added reference files:** generated from CSA's own workbooks (`reference/VERSION.txt`).
- **Where corrections go:**
  - a problem with the scoring method, the prompts or CSA's reference data goes to CSA, as the owner of the package
    and the engine. The fixes here are written up for CSA (`DEVIATIONS.md`), though none is filed yet, and a later
    package that carries them lets the plugin drop its blocks;
  - a problem with this plugin, its fixes or its added data goes to this repository ([`FEEDBACK.md`](FEEDBACK.md)).

## Feedback and support

There is no formal support; help is built into the skill. Report problems as an issue in
`CloudSecurityAlliance/csa-plugins-official` with `[valid-ai-ted-scorer]` at the start of the title. Never include
questionnaire content (see [`FEEDBACK.md`](FEEDBACK.md)). Report security problems privately, through the repository's
private vulnerability reporting (the **Security** tab), under CSA's security policy; never in a public issue.

## Development

This plugin is built and tested in CSA's private repositories, which are the source of truth for its own files. CSA's
published Valid-AI-ted Scorer package is the source of truth for the method, the prompts and the four published
reference files. This marketplace receives released versions only, so a change made here directly would be lost at
the next release: report it instead (see "Feedback and support"). What does not come here: the test questionnaires
and results, the internal tester's guide, and CSA's source workbooks for the added reference files, each pinned by
SHA-256 in `skills/caiq-scorer/reference/VERSION.txt` with the CSA page it comes from.

## Licence

The plugin's own files, including the sections it adds to `SKILL.md`, are licensed under the Apache License 2.0
([`LICENSE`](LICENSE)). **The licence does not cover the CSA works the plugin includes:** CSA's published `SKILL.md`
text, the scoring prompts, and the CCM and AICM reference data. These remain © Cloud Security Alliance, all rights
reserved. The data is under CSA's notices, reproduced word for word in `skills/caiq-scorer/reference/NOTICE-CCM.txt`
and `NOTICE-AICM.txt`. [`NOTICE`](NOTICE) has the details.
