# Rich Internal JSON Format

The canonical lossless format. Always produced. All other formats are projections of this.

## Schema

```json
{
  "metadata": {
    "methodology": "NIST IR 8477",
    "styles": ["supportive"],
    "focal_document": {
      "title": "NIST SP 800-53 Revision 5",
      "secid": "secid:control/nist.gov/800-53@r5",
      "concept_count": 1189,
      "concept_types": ["control"]
    },
    "reference_document": {
      "title": "CSA CCM v4.1",
      "secid": "secid:control/cloudsecurityalliance.org/ccm@4.1",
      "concept_count": 207,
      "concept_types": ["control"]
    },
    "use_case": {
      "intended_users": "Security engineers evaluating control overlap",
      "purpose": "Determine how CCM controls support NIST 800-53 controls",
      "concept_types_mapped": "controls to controls",
      "direction": "reference → focal (CCM → NIST)",
      "exhaustiveness": "strongest-direct-only"
    },
    "style_selection_rationale": "B2 Supportive chosen because the use case asks how CCM supports NIST rather than set-theoretic overlap",
    "candidate_generation_strategy": "Paired by security domain — IAM with AC family, DSP with SC family, etc. Pre-filtered to strongest-direct candidates.",
    "total_pairs_considered": 857,
    "provenance": {
      "model_evaluator": "claude-sonnet-4-6",
      "plugin_version": "nist-ir-8477-mapping@1.x",
      "session_type": "interactive"
    },
    "created": "2026-04-06",
    "prompts_used": ["mapping-v1.0"],
    "validation": {
      "performed": true,
      "models": ["codex", "gemini"],
      "findings_applied": 3
    }
  },
  "mappings": [
    {
      "focal_concept": {
        "id": "AC-2",
        "title": "Account Management"
      },
      "reference_concept": {
        "id": "IAM-12",
        "title": "Identity and Access Management"
      },
      "focal_concept_text": "The organization shall establish, document, and manage user accounts...",
      "reference_concept_text": "[licensed — not reproduced]",
      "evaluation_steps": [
        "identical: no — wording differs significantly",
        "equivalent: no — IAM-12 is broader than AC-2 in scope",
        "contrary: no — no contradicting elements found",
        "direction: reference supports focal — IAM-12's requirements are a component of achieving AC-2",
        "property: integral to — AC-2 cannot be achieved without IAM-12's lifecycle controls"
      ],
      "alternatives_considered": [
        {"type": "supports", "rejected_because": "AC-2 is the focal goal; IAM-12 is the enabler — direction is reference→focal"},
        {"type": "equivalent", "rejected_because": "IAM-12 is broader than AC-2, covering more than just account management"}
      ],
      "text_evidence": [
        {"source": "focal", "excerpt": "...comprehensive account management including provisioning, de-provisioning, and periodic review..."},
        {"source": "reference", "excerpt": "[licensed — minimum excerpt] ...identity lifecycle management..."}
      ],
      "style": "supportive",
      "relationship_type": "is supported by",
      "relationship_property": "integral to",
      "rationale": null,
      "justification": "IAM-12 requires comprehensive identity lifecycle management including provisioning, de-provisioning, and periodic review, which directly supports AC-2's account management requirements for...",
      "confidence": "High",
      "source_observations": ["IAM-12 uses broader terminology than AC-2 for the same operational scope"]
    }
  ],
  "no_relationships": [
    {
      "id": "no_rel_PE-1_IAM-12",
      "focal_concept": {"id": "PE-1", "title": "Physical and Environmental Protection Policy"},
      "focal_concept_text": "The organization develops, documents, and disseminates a physical and environmental protection policy...",
      "reference_concept": {"id": "IAM-12", "title": "Identity and Access Management"},
      "reference_concept_text": "[licensed — not reproduced]",
      "evaluation_steps": [
        "closest considered: supports (IAM-12 → PE-1)",
        "rejected because: PE-1 addresses physical security policy (facility access, environmental hazards); IAM-12 addresses digital identity — different security domains with no substantive content overlap",
        "counterfactual: a relationship would exist if either concept addressed the other's domain, which neither does"
      ],
      "closest_relationship_considered": {
        "type": "supports",
        "considered_because": "both involve access — one digital, one physical",
        "rejected_because": "physical access and digital identity management are operationally distinct; 'access' is the only shared term and it refers to different things"
      },
      "reason": "Different security domains — physical security vs. identity management — with no content overlap",
      "confidence": "High"
    }
  ],
  "no_relationship_domains": [
    {
      "domain": "Physical and Environmental Protection",
      "focal_concepts_with_no_relationship": ["PE-1", "PE-2"],
      "individual_record_ids": ["no_rel_PE-1_IAM-12", "no_rel_PE-2_IAM-12"],
      "structural_reason": "Physical protection controls address facility and environmental security, which is outside the scope of CCM IAM controls.",
      "gap_type": "scope-mismatch",
      "note": "PE family controls would map to CCM's physical security domain controls, not IAM."
    }
  ],
  "gap_analysis": {
    "summary": "NIST SP 800-53r5 coverage assessment against CSA CCM v4.1",
    "reference_concepts_with_no_support": [
      {"id": "IAM-12", "title": "Identity and Access Management", "reason": "No NIST control evaluated in this pass addresses IAM-12's full scope"}
    ],
    "focal_concepts_with_no_mapping": [
      {"id": "PE-1", "title": "Physical and Environmental Protection Policy", "domain": "Physical and Environmental Protection", "reason": "CCM does not include physical security controls"}
    ],
    "coverage_percentage": {
      "reference_concepts_covered": "195 of 207 (94.2%)",
      "focal_concepts_mapped": "1050 of 1189 (88.3%)"
    },
    "structural_findings": [
      "CCM provides strong coverage of NIST 800-53 technical and operational controls but has limited equivalent controls for physical and environmental protection (PE family) and personnel security (PS family).",
      "The 12 unmapped NIST controls cluster in the PE and PS families, reflecting CCM's cloud-service focus rather than a coverage gap — physical security in cloud environments is typically a provider responsibility addressed separately."
    ]
  },
  "source_observations": [
    "CCM uses domain-level groupings (IAM, DSP, etc.) that don't map cleanly to NIST control families",
    "NIST AC-2 is more prescriptive about specific account types than CCM IAM-12"
  ],
  "statistics": {
    "total_pairs_evaluated": 245,
    "by_type": {
      "supports": 45,
      "is_supported_by": 78,
      "equivalent": 12,
      "identical": 0,
      "contrary": 3,
      "no_relationship": 107
    },
    "by_confidence": {"High": 156, "Medium": 72, "Low": 17}
  }
}
```

## Notes

- **Multiple entries per concept pair are expected.** The same focal/reference pair can appear multiple times when:
  - Multiple styles are composed (e.g., one supportive entry + one set-theory entry for the same pair)
  - A pair has both a supportive relationship AND a contrary relationship on different elements (per NIST §4.2)
  - The same pair is evaluated under different set-theory rationales (syntactic vs semantic)
- Each mapping entry carries its own `style` field so entries from different styles are distinguishable.
- `metadata.styles` is an array — lists all styles used in this mapping engagement.
- `rationale` is null for non-set-theory styles. For set theory, it's "syntactic", "semantic", or "functional".
- `relationship_property` is null when no property applies (or for styles that don't have properties).
- `no_relationships` is a separate array — "no relationship" findings are first-class, not buried in the mappings array.
- `evaluation_steps` records the step-by-step reasoning used to select or reject each relationship type, making AI reasoning auditable.
- `alternatives_considered` lists relationship types explicitly considered and rejected, with rationale — required for defensible mappings.
- `text_evidence` captures the excerpts that ground each mapping decision; use `[licensed — not reproduced]` for controlled text.
- `closest_relationship_considered` in `no_relationships` entries records what the evaluator nearly assigned and why it was rejected.
- `no_relationship_domains` aggregates no-relationship findings by security domain for structural analysis.
- `gap_analysis` is a top-level summary of coverage gaps — focal concepts with no mapping and reference concepts with no support.
- `structural_findings` in `gap_analysis` explains systemic patterns (e.g., PE family absent from CCM by design).
- `source_observations` appear at both the per-mapping and document level.
- `statistics` are computed from the mappings, not manually entered.
- `style_selection_rationale`, `candidate_generation_strategy`, `total_pairs_considered` — metadata fields documenting how the mapping was approached. `provenance` captures the model, plugin version, and session type used.
- `focal_concept_text` and `reference_concept_text` — full verbatim text of each concept. For licensed content, `reference_concept_text` is `"[licensed — not reproduced]"` and excerpts go in `text_evidence[].excerpt`.
- `evaluation_steps[]` — string array documenting every check performed during evaluation, following `"check: result — reason"` format. Required for all `mappings[]` entries. evaluation_steps[] for B1/B2/B3 styles typically contains 5-7 entries — one per check (identical, equivalent, contrary, direction, and optionally property). Steps 1 (read concepts), 2 (capture text), and 8 (record alternatives) produce other fields (focal_concept_text, reference_concept_text, alternatives_considered[]) rather than evaluation_steps entries.
- `alternatives_considered[]` — array of `{type, rejected_because}` objects listing relationship types that were considered and rejected. At least one entry required per positive mapping.
- `text_evidence[]` — array of `{source: "focal"|"reference", excerpt}` objects. Replaces the older flat `source_text_excerpts` field. Source attribution is mandatory.
- `no_relationships[].id` — unique identifier for each no-relationship record, following the convention `"no_rel_{focal_id}_{reference_id}"`. Required field.
- `closest_relationship_considered` — object with `{type, considered_because, rejected_because}` on each `no_relationships[]` entry, documenting the closest relationship that was still rejected.
- `no_relationship_domains[]` — domain-level summaries aggregating no_relationship records. `individual_record_ids` must be the COMPLETE list of record IDs, not a count.
- `gap_analysis{}` — top-level structural interpretation of all negative evidence. Write `structural_findings[]` before computing `coverage_percentage` statistics.
