# Phase 4: Chain Analysis

## Purpose

Build the weakness chain — mapping root cause through enabling weakness to exploited weakness and impact. This is optional — the analyst can stop at a single CWE assignment from Phase 3.

## Prerequisites

Read `references/chain-patterns.md` for common chain templates.

## Process

### Step 1: Identify Chain Components

Map the vulnerability to these roles:
- **Root cause** — the fundamental flaw (e.g., missing input validation)
- **Enabling weakness** — what makes the flaw exploitable (e.g., dynamic query construction)
- **Exploited weakness** — the specific vulnerability type (e.g., SQL injection)
- **Impact** — what the attacker achieves (not a CWE — this is the consequence)

Not every vulnerability has all four. Simple vulnerabilities may have root cause → impact with no intermediate steps.

### Step 2: Assign CWEs to Each Link

Each link in the chain gets its own CWE. Use `cwe-tool.py lookup` to verify each one and `cwe-tool.py children` to ensure you're at the right abstraction level.

### Step 3: Check MITRE Relationships

Use `cwe-tool.py chain <CWE-ID1> <CWE-ID2> ...` to retrieve any existing MITRE relationships between your chain CWEs.

**Important:** These relationships are taxonomic — they inform the analysis but do not determine the chain. CWE's ChildOf and PeerOf relationships describe hierarchical classification. CanPrecede/CanFollow relationships describe potential temporal ordering but are sparse in the data.

A valid exploit chain may connect CWEs that have no MITRE relationship. The analyst and you reason about causal/exploit flow based on the vulnerability's specifics.

### Step 4: Tag Each Link Independently

Each chain link gets its own confidence level. The root cause may be **Confirmed** from code analysis while an enabling weakness is **Inferred**. Don't force uniform confidence across the chain.

### Step 5: Check Against Common Patterns

Compare the chain against patterns in `references/chain-patterns.md`. Does it match a known pattern? If so, verify the match is genuine, not just superficial similarity.

### Step 6: AI Relevance Overlay (if applicable)

**After the chain is established**, annotate each link with AI relevance if the vulnerability involves an AI system:
- Use `cwe-tool.py ai-relevant` to check scores for each chain CWE
- Use `cwe-tool.py lookup` to see View1/View2 reasoning
- Reference `references/ai-relevance-guide.md` for interpretation

This is **annotation**, not chain construction. The chain should be correct regardless of AI relevance scores.

## Teaching Moment

> **Why chains matter for CVE records:** A single CWE on a CVE record tells you what the weakness IS, but a chain tells you HOW it's exploitable. For a CNA, the primary CWE (the most specific exploitable weakness) goes on the CVE record. The chain goes in the analysis justification — it shows you understand the vulnerability deeply enough to trace causality.
>
> **Taxonomic vs. directional relationships:** CWE-89 (SQL Injection) has a ChildOf relationship to CWE-943 (Data Query Logic) in view 1000 — that's taxonomy, describing where SQL injection sits in the classification hierarchy. But CWE-20 (Input Validation) CanPrecede CWE-74 (Injection) — that's a directional relationship describing potential causal flow. The tool shows both kinds and labels them differently. Don't confuse parent-child hierarchy with causal exploit flow.

## Output

Present the chain using the standardized flat format:

```
Root Cause: CWE-XXX (Name) [Confidence]
→ enables: CWE-YYY (Name) [Confidence]
→ leads to: CWE-ZZZ (Name) [Confidence]
→ Impact: [description of what the attacker achieves]
```

For compound weaknesses (see Step 5b), use the convergent format:

```
Contributing: CWE-XXX (Name) [Confidence]
Contributing: CWE-YYY (Name) [Confidence]
→ combined effect: [description or CWE] [Confidence]
→ Impact: [description]
```

For each link: CWE ID, Name, confidence level, and relationship to adjacent links.

If AI relevance was applied, show annotations separately:
- CWE-XXX: View1=N, View2=N, Category=...

Then pause: "Here's the full chain with confidence levels per link. Does the causal flow make sense?"
