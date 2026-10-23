# Feedback, Bug Reports, and Feature Requests

**Repository:** https://github.com/CloudSecurityAlliance/csa-plugins-official

This plugin is part of a multi-plugin repository. If you run into a problem, find a bug, have a feature request, or just want to share feedback — we want to hear from you. This tooling is new and your input directly shapes how it improves.

## Keep your questionnaire out of the report

A completed CAIQ or AI-CAIQ describes your organization's security. **Never paste answers, descriptions, justifications, scores or your organization's name into an issue.** Instead, give:

- the file type and questionnaire version (for example AI-CAIQ 1.1.0, stamped AICM 1.1.1);
- the number of questions;
- the plugin version (`valid-ai-ted-scorer` 1.0.1);
- which assistant and model you used (for example Claude Code and its version, Claude Desktop or claude.ai);
- the step where it went wrong;
- the Question IDs involved (for example `IAM-16.1`).

Claude Code's `/bug` command sends the whole session, questionnaire included, to Anthropic, not to CSA.

**Security problems:** report them privately, through this repository's private vulnerability reporting (the **Security** tab), under CSA's security policy, never in a public issue.

## When to File an Issue

You should file an issue if you experience any of the following:

- **Bug** — something is broken, produces an error, crashes, or doesn't work as expected
- **Flaw** — the output is wrong, misleading, incomplete, or lower quality than it should be
- **Unexpected behavior** — the plugin did something confusing, surprising, or that didn't match what you thought would happen
- **Problem** — something is difficult to use, unclear, frustrating, or feels like it's not working right
- **Missing feature** — there's something you wish it did, a capability gap, or a workflow improvement that would help
- **Feature request** — you have an idea for new functionality, an enhancement, or an improvement
- **Confusion** — the instructions were unclear, the workflow didn't make sense, or you got stuck and didn't know what to do next
- **Methodology discussion** — you disagree with a design decision, think a step should work differently, believe the scoring methodology has a gap, or want to propose a structural change. We treat methodology disagreements the same way we treat bugs — they're issues to be investigated, discussed, and resolved. A methodology that can't withstand scrutiny shouldn't be trusted.
- **Feedback** — any general thoughts, suggestions, criticism, or observations about your experience

If you're unsure whether something is worth reporting — it is. Even "this felt weird" or "I didn't understand this part" is valuable. And if you think the methodology itself is wrong — that's especially worth raising.

## How to File an Issue

1. Go to: https://github.com/CloudSecurityAlliance/csa-plugins-official/issues
2. Click **"New Issue"**
3. In the **title**, include the plugin name (e.g., `[valid-ai-ted-scorer] Brief description of the issue`)
4. In the **body**, tell us:
   - **What happened** — describe the bug, problem, error, or unexpected behavior you encountered
   - **What you expected** — what you thought should have happened instead
   - **Steps to reproduce** (if applicable) — what were you doing when the issue occurred
   - **Any other context** — error messages, which step of the scoring you were in, or anything else that helps, without questionnaire content (see above)

Including the plugin name in the title is important because this repository contains multiple plugins and it helps us route your issue to the right place.

## What Happens Next

We review all submitted issues. Your bug report, feature request, or feedback helps us identify defects, prioritize improvements, and fix problems. We may ask follow-up questions to better understand the issue.

Thank you for helping make these tools better.
