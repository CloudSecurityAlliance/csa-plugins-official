# Incident Analysis Report Template

This template is **goal-oriented, not schema-rigid**. It describes what we want to capture and why. Reports are freeform markdown consumed by humans and AI — both can handle flexible structure.

## Required Elements

Every report should include these, but format and ordering are flexible:

- **Incident name** — What people call this incident (common name, not formal)
- **Affected vendor/service** — Who was impacted
- **When it happened** — Approximate date range
- **Analysis date** — "This analysis reflects information available as of YYYY-MM-DD"
- **Executive summary** — 2-3 paragraphs: what happened, how bad, key takeaways
- **Timeline** — Chronological reconstruction of events, with confidence tags
- **Technical analysis** — Attack chain, vectors, impact. Use MITRE ATT&CK terminology where applicable but keep it readable
- **Source analysis** — What sources agree/disagree on, confidence assessments, bias notes
- **Gap analysis** — What's not being said, inferences (all labeled "Analyst/AI assessment:")
- **Key findings** — Numbered list of most important takeaways, each with confidence level
- **Resources** — Links to vendor disclosures, news, discussions, CVEs, advisories. Include access dates
- **Implications for CSA controls** — Which AICM/CCM control domain families are relevant and briefly why. Do NOT do detailed control-by-control mapping — that is the job of the controls mapping plugin

## Intentionally Flexible

- Section ordering adapts to the incident
- Sections can be combined or split based on complexity
- Additional sections can be added (regulatory impact, supply chain, etc.)
- Prose style varies — narrative for some incidents, bullet points for others
- Use judgment about detail level per section

## Output Location

Reports write to the `dataset-private-incident-analysis` repo:

1. Use analyst-specified directory if provided
2. Otherwise check `~/GitHub/CloudSecurityAlliance-DataSets/dataset-private-incident-analysis/`
3. If not found, ask: "I can't find the incident analysis dataset repo. Where should I save reports?"

Filename: `YYYY-MM-DD-<incident-slug>.md` (e.g., `2026-02-15-acme-corp-api-breach.md`)

## Versioning

Reports are immutable. Re-analysis produces a new file with today's date. The new report notes in its Executive Summary that it supersedes a prior analysis and highlights what changed.
