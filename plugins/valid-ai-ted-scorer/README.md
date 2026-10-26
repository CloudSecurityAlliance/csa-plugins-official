# Valid-AI-ted Scorer

The Valid-AI-ted Scorer reads a completed CSA security questionnaire, a CAIQ (for the Cloud Controls Matrix, CCM) or an
AI-CAIQ (for the AI Controls Matrix, AICM), and scores every answer from 0 to 4 using the Cloud Security Alliance's
Valid-AI-ted scoring method. It then writes a scored Excel workbook and a summary PDF with a score for each domain.

The result is **an informational, AI-assisted assessment of the written responses**, produced by your AI assistant.
It does not check that any control is in place, and it is **not a CSA certification or audit** (see
[What it is not](#what-it-is-not)).

The plugin is the published method (CSA's Valid-AI-ted Scorer package 1.1.0) with seven documented fixes, and reference
data added so that every CAIQ and AI-CAIQ release CSA publishes is scored against the CCM or AICM version it pairs
with.

**On this page**

- [Install](#install): the Claude app, ChatGPT, the command line
- [Use it](#use-it)
- [What it does, in detail](#what-it-does-in-detail)
- [What it is not](#what-it-is-not)
- [Fixes in this plugin](#fixes-in-this-plugin)
- [Known issues](#known-issues)
- [Your questionnaire and the AI model](#your-questionnaire-and-the-ai-model)
- [What has been tested](#what-has-been-tested)
- [Versions](#versions)
- [Feedback and support](#feedback-and-support)
- [Licence](#licence)

## Install

### In the Claude app (web or desktop)

On a paid Claude plan (Pro, Max, Team or Enterprise), with **Code execution and file creation** turned on:

1. Go to [Customize → Plugins](https://claude.ai/customize/plugins), select **Add**, then **Add marketplace**, choose
   **Add from a repository**, and enter `CloudSecurityAlliance/csa-plugins-official`. You only do this once.
2. On the **Plugins** tab, open **Discover**, select **valid-ai-ted-scorer**, then select **Add**.

The [main README](../../README.md#install-in-the-claude-app-web-or-desktop) has the full steps, what you need first,
and troubleshooting, checked against Anthropic's documentation on 2026-10-23. **Not yet tested:** this plugin has been
tested only in Claude Code, not in the Claude app (see [What has been tested](#what-has-been-tested)).

### In ChatGPT

ChatGPT adds the scorer as a skill, on Business, Enterprise, Healthcare and Edu plans. Download this repository as a
ZIP, unzip it, zip the folder `plugins/valid-ai-ted-scorer/skills/caiq-scorer` itself, and upload that zip in ChatGPT
under **Plugins** → **Skills** → **Create** → **Upload from your computer**. The
[main README](../../README.md#install-in-chatgpt-web-or-desktop) has every step, the permissions you need, and
OpenAI's links.

**Not tested in ChatGPT.** The skill folder is about 24 MB (about 5 MB zipped), because it carries CSA's reference
data, and we have not checked whether ChatGPT accepts a skill that large, or how the scorer behaves there.

### On the command line

**Claude Code:**

```text
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
/plugin install valid-ai-ted-scorer@csa-plugins-official
```

If Claude Code says `Run /reload-plugins to apply`, run `/reload-plugins`, or start a new session.

**Codex:**

```text
codex plugin marketplace add CloudSecurityAlliance/csa-plugins-official
codex plugin add valid-ai-ted-scorer@csa-plugins-official
```

**Gemini CLI:**

```text
gemini skills install https://github.com/CloudSecurityAlliance/csa-plugins-official.git --path plugins/valid-ai-ted-scorer/skills/caiq-scorer
```

**Antigravity CLI** (which replaced Gemini CLI for personal Google accounts): copy the
`plugins/valid-ai-ted-scorer/skills/caiq-scorer` folder into `~/.gemini/antigravity-cli/skills/`.

The [main README](../../README.md#codex-antigravity-and-gemini-cli) says what works differently in Codex, Antigravity
and Gemini, and when its steps were tested. **This plugin's scoring has not been tested in Codex, Antigravity or
Gemini.**

## Use it

Attach or point to a completed CAIQ or AI-CAIQ workbook (for example one downloaded from the STAR Registry), and ask
for it to be scored. For example:

> Score this completed questionnaire with the Valid-AI-ted Scorer, and produce the scored workbook and summary PDF.

The skill proposes the reference data from your questionnaire's version, and **asks you to confirm it** before it
scores. It then writes `<your file>_scored.xlsx` and `<your file>_scoring_report.pdf`, and never overwrites a file
that was there before it started.

**What it needs:** nothing beyond the plugin. Your AI assistant applies the rules and writes the files with whatever
spreadsheet and PDF tools are already on your machine, Python's standard library included. It never installs anything
without asking. If one of the files still cannot be made and you decline an install, it writes that file's fallback
instead, a CSV for the workbook or a Markdown report for the PDF, and says why.

The skill has built-in help: ask it why a row scored 0, which version you are using, or how to report a problem.

## What it does, in detail

This section explains the method for someone who has never seen it. The rules come from CSA's published
[`SKILL.md`](skills/caiq-scorer/SKILL.md) and the plugin's fixes to it ([`DEVIATIONS.md`](DEVIATIONS.md)).

### What goes in

A completed CAIQ or AI-CAIQ workbook in CSA's template. The scorer works out which questionnaire it is from its
columns (CAIQ files have columns such as `CSP CAIQ Answer` and `CCM Control ID`; AI-CAIQ files have
`Service Provider AI-CAIQ Answer` and `AICM Control ID`), and asks you if that is unclear.

**The version, which you confirm.** The scorer reads the version stamp in cell A1 of the `Introduction` sheet. In
newer files the stamp names both the questionnaire version and the CCM or AICM version; a CAIQ v4.0.x says only, for
example, `v4.0.2`. If there is no stamp, it uses the questionnaire sheet's name, then the file name. If these disagree,
or nothing names a version, it asks you, and it never guesses. From the version it proposes the reference data CSA
pairs with that questionnaire:

| Your questionnaire | Its stamp | Reference data |
|---|---|---|
| CAIQ v4.0.1, v4.0.2 or v4.0.3 | `v4.0.x` | CCM 4.0.13, `CCM-4.0.13-merged.csv` (CSA's last CCM v4.0; 4.0.12 has the same text) |
| CAIQ v4.1.0, or CAIQ-Lite v4.1.0 | CCM 4.1.0 | CCM 4.1.0, `CCM-4.1.0-merged.csv` |
| CAIQ v4.1.0 (CSA's bundle of 2026-10-02) | CCM 4.1.1 | CCM 4.1.1, `CCM-4.1.1-merged.csv` (added) |
| AI-CAIQ 1.0.2 | AICM 1.0.2 | AICM 1.0.2, `AICM-1.0.2-merged.csv` |
| AI-CAIQ 1.0.2 (CSA's bundle of 2025-11-10) | AICM 1.0.3 | AICM 1.0.3, `AICM-1.0.3-merged.csv` (added) |
| AI-CAIQ 1.1.0 (CSA's bundle of 2026-06-18) | AICM 1.1.0 | AICM 1.1.0 as CSA published it, `AICM-1.1.0-published-merged.csv` (added) |
| AI-CAIQ 1.1.0 (CSA's current bundle) | AICM 1.1.1 | AICM 1.1.1, `AICM-1.1.1-merged.csv` (added) |

You then confirm the version, and the scorer does not score without that confirmation. It matters because control IDs
are not stable between versions: of the 242 control IDs that AICM 1.0.x and 1.1.x share, 65 have a different title
(`AIS-08` is "Input Validation" in 1.0.2 but "API Security" in 1.1.0), and CCM 4.0.x and 4.1.x also retitled and
renumbered controls. The wrong version attaches the wrong guidance to your answers, with no visible error.

**What it cannot score.** It says so, rather than guessing, for:

- CAIQ v3.x (for CCM 3.0.1), which has no ownership or description columns;
- AI-CAIQ 1.0.1, which does not have the answer columns CSA added in 1.0.2;
- SSCF-CAIQ v1.0, the questionnaire of CSA's SaaS Security Capability Framework, which has no ownership column and
  pairs with neither CCM nor AICM.

**Organization and Cloud Service,** for the report's first page, come only from you: the assistant asks, or leaves
them blank.

### How it scores, step by step

1. **It finds the questions.** It scores only the questionnaire sheet (named like `CAIQv4.1.0` or `AI-CAIQv1.1.0`,
   with its header in row 2), never the `Introduction` sheet or the other information sheets. It finds each column by
   its header name. CSA's templates merge the Control ID and Domain Title cells over several rows, so a blank cell takes
   the value at the top of its merged range. Only rows with a Question ID like `AIS-08.1` are questions; the "End of
   Standard" row and the copyright line are not scored or counted.
2. **It reads each answer** as `Yes`, `No` or `NA`, ignoring case and spaces. `NA` is kept as an answer, never
   confused with a blank.
3. **It matches each question to its control.** It looks up the question's Control ID (the Question ID before the dot)
   in the reference file of the confirmed version, and attaches that control's implementation and auditing guidelines:
   for a CAIQ, the provider (CSP), customer (CSC) and auditing guidelines; for an AI-CAIQ, the shared guidelines, the
   guidelines for each AI role (model provider, orchestrated service provider, application provider, AI customer and
   cloud service provider) and the five role-specific auditing guidelines. It matches on the Control ID only, and if a
   Control ID is not in the reference file, it says so for that row rather than guessing.
4. **It applies the mechanical checks.** These are rules, applied before any judgment. A row that fails one scores 0
   and is not judged by the model, and that 0 is final:
   - **Ownership.** The `SSRM Control Ownership` column (who is responsible for the control) is required, and must hold
     one of CSA's values:
     - CAIQ: `CSP-owned`, `CSC-owned`, `Shared CSP and CSC`, `Shared CSP and 3rd-party`, `3rd-party outsourced`,
       `Not Determined`;
     - AI-CAIQ: `Owned by CSP`, `Owned by MP`, `Owned by OSP`, `Owned by AP`, `Owned by AIC`,
       `Shared Across the Supply Chain`, `Shared CSP-MP`, `Shared by MP-OSP` (or `Shared MP-OSP`, the spelling in CSA's
       drop-down), `Shared OSP-AP`, `Shared AP-AIC`, `Not Determined`.

     A blank ownership is accepted only when the answer is `NA`.
   - **Which descriptions are required.** The ownership decides whether the provider's implementation description and
     the customer's responsibilities description are required:
     - CAIQ: the provider description for `CSP-owned`, `Shared CSP and CSC`, `Shared CSP and 3rd-party` and
       `3rd-party outsourced`; the customer description for `CSC-owned`, `Shared CSP and CSC`,
       `Shared CSP and 3rd-party` and `3rd-party outsourced`;
     - AI-CAIQ: the provider description for every value except `Not Determined`; the customer description only for
       `Owned by AIC`, `Shared AP-AIC` and `Shared Across the Supply Chain`;
     - `Not Determined` requires neither, and a missing or invalid ownership requires both.
   - **Too short to count.** The row scores 0 if a required description is blank, only 1 or 2 characters, or just
     "yes" or "no". This is why a blank description can zero a row even where CSA's template marks it optional. A description
     that isn't required may be blank without this check: the model then judges the row, and scores empty content 0.

   A row that fails gets the justification "Final score based on Implementation Description Score (0)".
5. **The model judges every other row,** following CSA's scoring prompts, against the control's guidelines. It gives
   the provider's description a score with a justification and feedback, gives the customer's responsibilities
   feedback (text only, no score), and gives the row an overall score: a holistic blend of the parts, with no fixed
   weighting. Every score is on this scale:

   | Score | Meaning |
   |---|---|
   | 0 | Fails: non-compliant, a major contradiction, or empty |
   | 1 | Weak or minimal |
   | 2 | Basic or partial (also the most a "No" answer can get) |
   | 3 | Strong: meets expectations |
   | 4 | Excellent: exceeds expectations |

   Four rules always apply:
   - **A "No" answer caps every score for that row at 2,** however well it is explained.
   - **A major contradiction** between the answer and its explanation, such as "Yes" with "we do not implement this",
     scores 0 for that part, or for the whole row if it undoes the answer.
   - **An `NA` answer can still score 4** if its justification is thorough.
   - **An uncertain score becomes 2,** and a score outside 0–4 is brought back into range.

   The model also writes **readability feedback** on clarity, grammar and organization, which does not affect the
   score.

### Domain scores, the overall score, and what PASS means

For each domain (the CCM or AICM domain title), the scorer counts the questions, the passing scores (2 or more) and the
failing ones (below 2). It takes the plain average of the row scores, `NA` rows included, and turns it into a
percentage: average ÷ 4 × 100. A domain **passes at 50% or more**, compared before rounding. The **overall score** is
the plain average of all row scores, worked out the same way, not an average of the domain scores.

**What PASS means, and what it doesn't.** PASS means the responses average at least 2 of 4. It measures the quality
and coherence of what was written, not whether controls are in place, not independent evidence, and not compliance. A
well-written "No" scores 2 of 4, which is 50%, so a domain answered entirely with well-written "No" responses shows as
PASS.

### What comes out

**The scored workbook, `<your file>_scored.xlsx`,** beside your questionnaire. One row per question, with:

- your question, answer, ownership and two descriptions;
- for the provider's description: its score, the justification, the feedback, and the feedback's justification;
- for the customer's responsibilities: the feedback and its justification;
- the control's ID, specification, title and domain, and the guideline text from the reference data;
- the row's `Score`, `Score Justification` and `Readability Feedback`.

The column names are CSA's, in CSA's order ([`SKILL.md`](skills/caiq-scorer/SKILL.md), step 8). A second sheet,
`About`, records the scorer (`CSA Valid-AI-ted Scorer`), the package version (1.1.0), the prompt set (1.0.0), the
questionnaire type, the confirmed CCM or AICM version, the date, CSA's disclaimer, and two plugin lines: the plugin and
its version (`valid-ai-ted-scorer 1.0.1`), and the fixes applied.

**The summary report, `<your file>_scoring_report.pdf`:**

- **Page 1:** the title (`CAIQ / CCM Scoring Report` or `AI-CAIQ / AICM Scoring Report`); the organization and cloud
  service if you gave them; the overall score, PASS or FAIL, the date, and the CCM or AICM and questionnaire versions;
  then three or four paragraphs on the overall result, the highest- and lowest-scoring domains, and recommendations
  drawn from the numbers.
- **Page 2:** a bar chart of each domain's percentage, green for a pass and red for a fail, with a dashed line at 50%.
- **Page 3 onward:** one block per domain, with its question count, passing and failing scores, average, percentage
  and status, a few sentences on its strengths, and one or two suggestions drawn from that domain's feedback.
- **Last page:** CSA's disclaimer, word for word, then the same two plugin lines as the `About` sheet.

Every page's footer says `CSA Valid-AI-ted Scorer v1.1.0`.

The assistant keeps its working files in one new folder beside your questionnaire, `<your file>_work/`, and removes
it at the end or tells you where it is.

### Cost

Measured on 2026-10-23 with `claude-opus-5-5` at effort `xhigh` (macOS) and at the default effort (Windows), at
list-price equivalent:

| Questionnaire | Cost per run |
|---|---|
| A seeded file of about 25 questions | $1.52 to $3.19 |
| A full CAIQ (261 or 283 questions) | $1.80 to $9.63 |
| The full AI-CAIQ (320 questions) | $2.38 to $17.48 |

A full file's cost can vary several-fold between runs, settings and models. These measurements did not record how
long a run takes.

### Scores vary between runs

The mechanical checks are rules: in every test run that scored, the automatic zeros were exactly the expected rows. The
rows the model judges are different: they can score differently from one run to the next, and on a full questionnaire
the feedback can turn generic. Don't compare scores from different runs as if they were exact.

## What it is not

It does not verify that any control is implemented. It is not a CSA certification, audit, attestation, STAR Registry
listing or Valid-AI-ted badge, and it does not replace CSA's own service. The files it writes are for your own use, not
for distribution. Every report carries CSA's disclaimer.

## Fixes in this plugin

The published method is followed as written, except for seven documented fixes. Each is a marked block in
`skills/caiq-scorer/SKILL.md`, beside the sentence it amends. [`DEVIATIONS.md`](DEVIATIONS.md) gives each one's reason,
effect on scores and upstream report.

| Fix | What changes |
|---|---|
| A-01 | `Shared MP-OSP`, the spelling in CSA's AI-CAIQ drop-down, is accepted as well as the published `Shared by MP-OSP`. Rows using it are no longer zeroed. |
| A-02 | The version is read from the questionnaire's stamp (cell A1 of its `Introduction` sheet), and the reference data is proposed from a table covering every CAIQ and AI-CAIQ release (see [What goes in](#what-goes-in)). You still confirm it. |
| A-03 | Only the questionnaire sheet is scored (row 2 holds its header); columns are found by name; merged Control ID and Domain Title cells take the value at the top of their range; the footer rows are not questions. |
| A-05 | Reference rows are matched on the Control ID only, so a title typo in the bundled data never refuses a row. |
| A-15 | `Service Provider AI-CAIQ Answer`, the header in CSA's AI-CAIQ templates, is read as the answer column. |
| A-25 | A byte-order mark at the start of a reference file is ignored. |
| Ruling 20 | Which descriptions each AI-CAIQ ownership value requires, as ruled by the method's owner. |

**Four reference files are the plugin's additions** (marked "added" in the [version table](#what-goes-in)), generated
from CSA's own workbooks in the package's format, and checked against CSA's questionnaires and CSA's data service.
[`reference/VERSION.txt`](skills/caiq-scorer/reference/VERSION.txt) gives each one's source and checks.

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
- **Untested outside Claude Code:** the Claude app, ChatGPT, Codex and Gemini (see
  [What has been tested](#what-has-been-tested)).

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

**Not tested:** 1.0.1 on Windows; Claude Desktop and claude.ai; ChatGPT, Codex and Gemini; an interactive Claude Code
session (every run was headless); Linux; models other than `claude-opus-5-5`; and the fallback CSV, which no run has
needed.

## Versions

Plugin `valid-ai-ted-scorer` 1.0.1; CSA's Valid-AI-ted Scorer package 1.1.0; scoring prompt set 1.0.0; reference data
for CCM 4.0.13, 4.1.0 and 4.1.1, and AICM 1.0.2, 1.0.3, 1.1.0 and 1.1.1 (CCM 4.1.1, AICM 1.0.3, the published AICM
1.1.0 and AICM 1.1.1 added by the plugin).

The outputs carry `CSA Valid-AI-ted Scorer v1.1.0`, because 1.1.0 is the version of CSA's method and package. The
plugin's own version is 1.0.1, the version of its packaging and fixes.

### Changes in 1.0.1

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
- The measured cost, in the help and in "Known issues", and "What has been tested" above.
- The version is 1.0.1 throughout, so that a marketplace update replaces an installed 1.0.0.

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
