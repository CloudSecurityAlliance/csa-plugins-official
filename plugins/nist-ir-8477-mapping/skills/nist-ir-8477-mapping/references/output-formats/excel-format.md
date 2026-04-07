# Excel Format

Spreadsheet with one row per concept pair. Designed for human review and stakeholder communication.

## Columns

| Column | Description | Always Present |
|--------|-------------|---------------|
| Focal ID | Concept ID from focal document | Yes |
| Focal Title | Concept title from focal document | Yes |
| Reference ID | Concept ID from reference document | Yes |
| Reference Title | Concept title from reference document | Yes |
| Relationship Type | The style-specific relationship type | Yes |
| Rationale | Syntactic/Semantic/Functional (set theory only) | Set theory only |
| Property | Example of/Integral to/Precedes (supportive only) | Supportive only |
| Justification | Why this relationship type was chosen | Yes |
| Confidence | High/Medium/Low | Yes |
| Source Observations | Notes about ambiguities or issues | If present |

## Notes

- **Lossy projection**: Multi-value fields (source observations, cross-references) are semicolon-delimited. Nested metadata is flattened.
- One worksheet for mappings, one for "no relationship" findings, one for source observations.
- Consider including a summary worksheet with statistics and the use case document.
- JSON is the source of truth — use Excel for review and communication, not as the canonical record.
