# Phase 1a: Incident Discovery

## Purpose

Help the analyst identify which incident to analyze.

## Two Entry Points

### The analyst has a specific incident

They'll provide a name, CVE, company name, or URL. Your job:

1. Confirm you know which incident they mean
2. Do a quick web search to verify the incident and get basic facts
3. Present a brief overview: what happened, when, who was affected, incident type
4. Confirm with the analyst: "Is this the incident you want to analyze?"

### The analyst needs to find an incident

They want to analyze something but don't have a specific one in mind. Your job:

1. Ask what they're interested in: recent incidents? A specific sector? A particular attack type? Cloud vs. AI focus?
2. Search for recent noteworthy cloud/AI security incidents
3. Present 3-5 candidates with:
   - Incident name
   - Affected vendor/service
   - Approximate date
   - Brief description (1-2 sentences)
   - Why it's noteworthy (scale, novelty, relevance)
   - Estimated source availability (well-documented vs. sparse)
4. Let the analyst pick one

## What Makes an Incident "Noteworthy" for Analysis

**Teaching moment** (if teaching mode is on):

> Not all incidents are equally useful for analysis. The best candidates have:
> - **Multiple public sources** — vendor disclosure, news coverage, researcher write-ups, community discussion. Sparse coverage limits analysis depth.
> - **Relevance to cloud/AI** — the incident involves cloud infrastructure, AI systems, or SaaS products that map to CSA's control frameworks.
> - **Complexity** — simple credential stuffing is less analytically interesting than supply chain compromises or novel attack vectors.
> - **Recency** — recent incidents have more available sources and current relevance.
> - **Impact** — significant user/data impact makes the analysis more valuable for controls mapping.

## Output

A confirmed incident selection:
- **Incident name** (the common name people use)
- **Affected entity** (company, service, or product)
- **Date range** (approximate)
- **Incident type** (breach, vulnerability, supply chain, misconfiguration, etc.)
- **Brief description** (2-3 sentences)

Once confirmed, proceed to Phase 1b (source collection).
