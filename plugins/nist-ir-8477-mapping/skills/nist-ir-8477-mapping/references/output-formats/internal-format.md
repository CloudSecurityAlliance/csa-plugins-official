# Rich Internal JSON Format

The canonical lossless format. Always produced. All other formats are projections of this.

## Schema

```json
{
  "metadata": {
    "methodology": "NIST IR 8477",
    "style": "supportive",
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
      "focal_concept": {"id": "PE-1", "title": "Physical and Environmental Protection Policy"},
      "reference_concept": {"id": "IAM-12", "title": "Identity and Access Management"},
      "reason": "Different security domains — physical security vs identity management",
      "confidence": "High"
    }
  ],
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

- `rationale` is null for non-set-theory styles. For set theory, it's "syntactic", "semantic", or "functional".
- `relationship_property` is null when no property applies (or for styles that don't have properties).
- `no_relationships` is a separate array — "no relationship" findings are first-class, not buried in the mappings array.
- `source_observations` appear at both the per-mapping and document level.
- `statistics` are computed from the mappings, not manually entered.
