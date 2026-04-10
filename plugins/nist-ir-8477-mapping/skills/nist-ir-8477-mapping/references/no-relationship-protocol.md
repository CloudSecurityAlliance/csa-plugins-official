# No-Relationship Protocol

Three-level negative evidence architecture. Required reading before Phase 4b.

The core principle: to claim "nothing maps to concept X," you must show that X was compared against the candidate set and found insufficient. Silent omission is not a finding.

## Level 1: Individual Records (`no_relationships[]`)

Every pair considered and found unrelated gets a full record in `no_relationships[]`. Produce these using the negative pair protocol in `references/evaluation-protocol.md`.

**Record ID convention:** `"no_rel_{focal_id}_{reference_id}"` — e.g., `"no_rel_AICM-PS-01_ISO-A.6.1.3"`. Each record requires an `id` field using this format.

**Required fields per record:**
- `id` — unique identifier using the convention above
- `focal_concept` — `{"id": "...", "title": "..."}`
- `focal_concept_text` — full verbatim text of the focal concept
- `reference_concept` — `{"id": "...", "title": "..."}`
- `reference_concept_text` — full text, or `"[licensed — not reproduced]"` for licensed content
- `evaluation_steps[]` — negative pair protocol steps (closest considered, rejected because, counterfactual)
- `closest_relationship_considered` — `{type, considered_because, rejected_because}`
- `reason` — brief summary of why no relationship exists
- `confidence` — High / Medium / Low

## Level 2: Domain Summaries (`no_relationship_domains[]`)

After completing no_relationship records for a domain, synthesize one domain summary entry:

```json
{
  "domain": "Physical Security",
  "focal_concepts_with_no_relationship": ["AICM-PS-01", "AICM-PS-02", "AICM-PS-03"],
  "individual_record_ids": [
    "no_rel_AICM-PS-01_ISO-A.2.1",
    "no_rel_AICM-PS-01_ISO-A.6.1.3",
    "no_rel_AICM-PS-02_ISO-A.2.1",
    "no_rel_AICM-PS-03_ISO-A.2.1"
  ],
  "structural_reason": "AICM Physical Security controls address datacenter physical access requirements. ISO 42001 Annex A does not include physical security controls — this is a scope difference by design, not a coverage gap.",
  "gap_type": "out-of-scope",
  "note": "These AICM controls would map to ISO 27001 Annex A.11, not ISO 42001."
}
```

`gap_type` values:
- `gap_type: out-of-scope` — the reference document explicitly does not cover this area
- `gap_type: scope-mismatch` — both documents address the same topic but at different scopes (one operational, one strategic)
- `gap_type: abstraction-mismatch` — same concern, different level of abstraction
- `gap_type: genuine-gap` — the reference document should cover this but does not

`individual_record_ids` must be the complete list of all no_relationship record IDs in this domain — not a count, not a sample.

## Level 3: Gap Analysis (`gap_analysis{}`)

Structural interpretation of all negative findings. Synthesize after all no_relationship records and domain summaries are complete.

```json
{
  "summary": "ISO 42001 Annex A coverage assessment against AICM v1.0.3",
  "reference_concepts_with_no_support": [
    {
      "id": "A.6.1.3",
      "title": "AI system impact assessment",
      "reason": "No AICM control addresses AI-specific impact assessment at the organizational level"
    }
  ],
  "focal_concepts_with_no_mapping": [
    {
      "id": "AICM-PS-01",
      "title": "Physical Access Controls",
      "domain": "Physical Security",
      "reason": "ISO 42001 does not cover physical security — out of scope by design"
    }
  ],
  "coverage_percentage": {
    "reference_concepts_covered": "32 of 38 (84.2%)",
    "focal_concepts_mapped": "129 of 243 (53.1%)"
  },
  "structural_findings": [
    "ISO 42001 Annex A focuses on AI governance and lifecycle management; AICM includes broader operational security controls (physical, network, incident response) outside this scope. The unmapped AICM controls are not gaps in ISO 42001 — they are out-of-scope by design.",
    "6 ISO 42001 controls have no AICM support, clustering around AI-specific requirements: impact assessment, transparency documentation, and AI supplier oversight. These represent genuine coverage gaps where AICM does not address AI-specific governance."
  ]
}
```

**Write `structural_findings` first, before computing statistics.** The coverage percentages are computable from the data. The structural findings — interpreting what the numbers mean — are the product. Each finding should be 2-5 sentences explaining a pattern in the negative evidence.

The `individual_record_ids` arrays from all domain summaries collectively back the `focal_concepts_with_no_mapping` list in the gap analysis — every focal concept listed there must appear in at least one domain summary's `individual_record_ids`.

## Scale Guidance

**Small mappings (focal × reference ≤ 500 total possible pairs):** Document every candidate pair considered and found unrelated as an individual record.

**Large mappings (focal × reference > 500 total possible pairs):** Use representative sampling:
- For each unmapped focal concept: one `no_relationship` record against its single most plausible reference concept (the closest candidate that still didn't qualify)
- For each unsupported reference concept: one `no_relationship` record from the focal concept that came closest
- Domain summaries explain why the pattern extends to all other pairs in the domain

For AICM (243) × ISO 42001 (38): 9,234 total possible pairs — use representative sampling.
