# Phase 9: Report Generation

## Purpose

Synthesize all work from Phases 1-8 into a comprehensive incident analysis report and write it to the dataset repo.

## Prerequisites

Read `references/report-template.md` for the template structure and output location.

## Process

### Step 1: Resolve Output Location

Determine where to save the report:
1. If the analyst specified a directory earlier, use that
2. Check if `~/GitHub/CloudSecurityAlliance-DataSets/dataset-private-incident-analysis/` exists
3. If not found, ask: "I can't find the incident analysis dataset repo. Where should I save the report?"

### Step 2: Generate the Report

Using all the work from prior phases — source inventory, unified fact sheet, conflicts table, vendor analysis, timeline, regulatory compliance overlay, impact assessment, gap analysis, and defensive recommendations — synthesize the report.

**Key guidelines:**
- The report should stand alone — a reader who wasn't part of the analysis should be able to understand it fully
- Include the analysis date prominently: "This analysis reflects information available as of YYYY-MM-DD"
- Tag every factual claim with its confidence level
- All AI/analyst inferences are prefixed with "Analyst/AI assessment:"
- The CSA controls section stays high-level — list relevant AICM/CCM domain families and briefly explain why each is relevant to this incident. Do NOT do detailed control-by-control mapping (that is the job of the controls mapping plugin). This section is generated during report synthesis, not by any prior phase — synthesize it from the attack chain, impact assessment, and defensive recommendations
- Include the Vendor & Integration Analysis findings (from Phase 4) as a report section — the access comparison table, available-but-unused controls, and shared responsibility assessment are core deliverables, not just inputs to later phases
- Include all source URLs with access dates in the Resources section
- Write in clear, professional prose. Not academic — more like a well-written briefing

**Report quality bar:**
- Could a CSA analyst who wasn't part of this analysis use this report to brief leadership? If not, it needs more context.
- Could the controls mapping plugin take this report and map it to specific controls? If the attack chain and key findings aren't structured enough, improve them.
- Are the defensive recommendations specific enough that a security team could start implementing them without further research? If they're vague, sharpen them.
- Does the impact assessment clearly identify all affected populations and severity levels? If a reader can't tell who was harmed and how badly, the impact section needs work.

### Step 3: Check for Prior Analysis

Before writing, check if the output directory already contains a report for this incident (matching the incident slug). If so:
- Note the prior report in the Executive Summary: "This analysis supersedes the prior analysis from YYYY-MM-DD"
- Briefly note what's new or changed

### Step 4: Write the Report

Write the report as `YYYY-MM-DD-<incident-slug>.md` to the resolved output directory.

The `<incident-slug>` is a kebab-case short name derived from the incident name (e.g., "SolarWinds Supply Chain Compromise" → `solarwinds-supply-chain`).

### Step 5: Confirm with Analyst

After writing, tell the analyst:
- Where the report was saved (full path)
- A brief summary of what's in it
- "Would you like me to revise anything before we're done?"

## Teaching Moment (if teaching mode is on)

> **Why reports are structured this way:** The executive summary comes first because most readers — especially leadership — won't read the whole report. They need the "so what" immediately. The timeline and technical analysis come next for readers who need to understand what happened. Impact assessment and defensive recommendations follow for readers who need to decide what to do. Source analysis and gap analysis are for readers who want to assess the reliability of the findings. Resources go last as a reference section.
>
> **Why we track sources explicitly:** In incident analysis, provenance is everything. A claim without a source is just an opinion. Tracking access dates matters because sources change — vendors update disclosures, articles get corrections, community posts get edited. The report captures a point-in-time snapshot.
