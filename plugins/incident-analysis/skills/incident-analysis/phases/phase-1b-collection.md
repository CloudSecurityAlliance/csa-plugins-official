# Phase 1b: Source Collection

## Purpose

Given a confirmed incident, gather all available sources comprehensively. The goal is a complete picture, not just the first article you find.

## Input

An incident identified in Phase 1a, or provided directly by the analyst (name, CVE, company, URL).

## Collection Strategy

Search systematically across source types. For each source type, do a targeted web search and attempt to fetch the content.

### Source Types to Search For

Search for each of these categories. Not every incident will have all of them.

1. **Official vendor disclosure** — blog posts, incident reports, security advisories, customer notifications
2. **Security researcher write-ups** — independent analysis, proof-of-concept details, technical deep-dives
3. **CVE/NVD entries** — if a vulnerability is involved, check the CVE database
4. **CISA advisories** — check if CISA issued an advisory or alert
5. **SEC filings** — for public companies, check for 8-K filings about the incident
6. **Tech news coverage** — Ars Technica, Bleeping Computer, The Record, Krebs on Security, Dark Reading, etc.
7. **Mainstream news** — if the incident was big enough for general coverage
8. **Hacker News discussion** — search HN for the incident. Comments often contain technical insights and insider perspectives
9. **Reddit discussion** — search relevant subreddits (r/netsec, r/cybersecurity, r/sysadmin, etc.)
10. **Security forum discussions** — if applicable

### Web Access Strategy

- **Try web fetch first** for each source — it's faster and lighter
- **Fall back to Playwright** when fetch fails, returns incomplete content, or the site needs JavaScript rendering
- **Playwright is especially useful for:** Reddit, dynamically rendered pages, sites with anti-bot measures, news sites with heavy JS frameworks
- **For paywalled content:** attempt to get whatever is freely available (preview, excerpt), then ask the analyst if they can provide full text

## Graceful Degradation

**Never silently skip a source.** For each source you find but can't access:

1. List it in the inventory with the URL and source type
2. Note what kind of content you expected to find there
3. After collecting everything you can, present the failures: "I found but couldn't access these N sources. Can you paste the content for any of them?"

The analyst may have subscriptions, internal access, or cached copies.

## Teaching Moment (if teaching mode is on)

> **Why comprehensiveness matters:** Most analysts stop at the vendor disclosure and maybe one news article. But vendor disclosures are written to minimize damage. News articles are written to maximize engagement. The truth is usually somewhere in between, and you can only find it by comparing multiple perspectives.
>
> **Why I check community sources:** Hacker News and Reddit threads sometimes surface insider knowledge, technical details, or contextual information that doesn't appear in official disclosures. A comment from someone who "used to work at [company]" may be fabricated — or may be the most honest account available. You can't know without cross-referencing.

## Output

A **structured source inventory** presented to the analyst:

For each source found:
- **Source name/title**
- **URL**
- **Source type** (vendor disclosure, news, researcher, community, regulatory, etc.)
- **Date published/posted**
- **Status**: Retrieved / Partially retrieved / Failed to access / Awaiting analyst input
- **Brief summary** of what this source covers (2-3 sentences)

After presenting the inventory, pause and ask:
- "I've collected N sources (M fully retrieved, P need your help). Would you like to add any sources I missed, or paste content for the ones I couldn't access?"

Wait for the analyst's input before proceeding to Phase 2.
