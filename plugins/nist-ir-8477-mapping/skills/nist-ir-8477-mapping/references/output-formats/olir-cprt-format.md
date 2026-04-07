# OLIR/CPRT-Compatible JSON Format

Best-effort format for NIST OLIR submission and CPRT hosting. Based on published examples in IR 8477 and the OLIR repository. Exact schema pending confirmation against NIST's current submission requirements.

## Format

This is a **lossy projection** of the rich internal JSON. It drops: justification detail, confidence levels, source observations, prompts used. It keeps: concept pairs and relationship types.

```json
{
  "focal_document": "NIST SP 800-53 Revision 5",
  "reference_document": "CSA CCM v4.1",
  "relationship_style": "supportive",
  "mappings": [
    {
      "focal_element_id": "AC-2",
      "focal_element_description": "Account Management",
      "reference_element_id": "IAM-12",
      "reference_element_description": "Identity and Access Management",
      "relationship_type": "is supported by",
      "relationship_property": "integral to",
      "relationship_explanation": "IAM-12 requires identity lifecycle management supporting AC-2 account management."
    }
  ]
}
```

## Notes

- `relationship_explanation` is a condensed version of the full justification
- Set theory mappings include a `rationale` field
- Crosswalk mappings omit `relationship_type` and `relationship_property`
- This format is designed for NIST consumption — confirm against current OLIR submission requirements before submitting
