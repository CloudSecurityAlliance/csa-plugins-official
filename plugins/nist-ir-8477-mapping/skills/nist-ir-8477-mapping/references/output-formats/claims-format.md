# Claims-Based Format

Format for the knowledge graph vision. Every mapping is a **claim** (not a fact) from a perspective, with evidence. See the Security Standards Mapping project's `VISION-CLAIMS-GRAPH-2026-02-21.md` for the full design.

## Format

This format **expands** the internal JSON rather than reducing it. It adds provenance, perspective, and claim metadata.

```json
{
  "claim": {
    "id": "claim-uuid-here",
    "type": "mapping_relationship",
    "source_concept": {
      "secid": "secid:control/cloudsecurityalliance.org/ccm@4.1#IAM-12",
      "title": "Identity and Access Management"
    },
    "target_concept": {
      "secid": "secid:control/nist.gov/800-53@r5#AC-2",
      "title": "Account Management"
    },
    "relationship": {
      "style": "supportive",
      "type": "supports",
      "property": "integral to",
      "direction": "source → target"
    },
    "evidence": {
      "evaluation_steps": [
        "identical: no — wording differs",
        "direction: source supports target — IAM-12 enables AC-2",
        "property: integral to — AC-2 cannot be achieved without IAM-12"
      ],
      "alternatives_considered": [
        {"type": "is supported by", "rejected_because": "IAM-12 is the enabler, not the target"}
      ],
      "text_evidence": [
        {"source": "focal", "excerpt": "Relevant text from AC-2..."},
        {"source": "reference", "excerpt": "Relevant text from IAM-12..."}
      ],
      "justification": "Full justification text...",
      "confidence": "High"
    },
    "perspective": {
      "methodology": "secid:methodology/nist.gov/ir-8477",
      "style": "supportive",
      "evaluator": "AI-assisted (Claude)",
      "use_case": "Security engineers evaluating control overlap"
    },
    "provenance": {
      "created": "2026-04-06",
      "methodology_version": "NIST IR 8477 (February 2024)",
      "plugin_version": "0.1.0",
      "validation": {"models": ["codex", "gemini"], "findings_applied": 3}
    }
  }
}
```

## Design Principles

- **Claims, not facts**: Different engines, methodologies, and evaluators can legitimately produce different relationships for the same concept pair. All claims are preserved.
- **Directional edges**: The relationship has a direction. A→B is not the same as B→A.
- **SecID anchored**: Both concepts are identified by SecID, making them machine-resolvable.
- **Full provenance**: Every claim carries its methodology, evaluator, validation status, and creation date.
