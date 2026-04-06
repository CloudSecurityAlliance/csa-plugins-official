# Confidence Framework for Decomposition

Tag every AI-produced classification and decomposition decision with a confidence level. This helps users know where to focus their review effort.

## Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| **High** | Almost certainly correct — clear evidence from the source | Explicitly numbered controls, clear hierarchy markers, unambiguous concept types |
| **Medium** | Likely correct but involves interpretation | Prose-heavy documents where concept boundaries are judgment calls, hierarchy inferred from formatting rather than explicit markers |
| **Low** | Best guess — significant ambiguity in the source | Documents with inconsistent structure, concepts that could be classified multiple ways, hierarchy that isn't clearly defined |

## What Gets Tagged

| Decision | Typical Confidence | Why |
|----------|-------------------|-----|
| Document type classification | High | Usually clear from the document itself (it says "standard" or "regulation") |
| Hierarchy identification | High for well-structured, Medium for inconsistent | Depends on whether the source has explicit hierarchy markers |
| Concept ID extraction | High when explicit, Medium when inferred | "AC-2" is explicit; "the requirement in paragraph 3" is inferred |
| Concept boundary decisions | Medium to High | Where one concept ends and another begins can be interpretive |
| Concept type classification | Medium to High | Some concepts are ambiguous (is this a requirement or a recommendation?) |
| Cross-reference detection | Medium | Explicit references ("see AC-3") are High; implicit relationships are Medium |
| Parent-child assignment | High for explicit, Medium for inferred | Some documents have clear nesting; others require interpretation |

## Usage Rules

1. **Tag every AI-produced decision** — not just the final concept list, but the profiling decisions too
2. **Default to the lower level when uncertain** — Medium not High, Low not Medium
3. **Explain Low confidence items** — if something is Low, say why (e.g., "the document uses inconsistent numbering in this section")
4. **High does not mean infallible** — even High confidence items should be spot-checked by the user
5. **Confidence is about the AI's certainty, not the source's quality** — a well-written document produces High confidence decompositions; a poorly structured document produces Medium/Low confidence even if the content is excellent

## Common Confidence Mistakes

### Over-confidence in structure

**Mistake:** Assigning High confidence to hierarchy identification when the document uses formatting (bold, indentation) rather than explicit markers (numbered sections, "Domain:", "Control:").

**Fix:** If hierarchy is inferred from formatting, it's Medium. Formatting is a hint, not a declaration.

### Under-confidence in explicit IDs

**Mistake:** Assigning Medium confidence to concept extraction when the source has clear, unambiguous identifiers (e.g., "AC-2", "IAM-12", "Art. 6").

**Fix:** If the ID is printed right there in the source, it's High. The AI didn't interpret anything — it read the label.

### Missing confidence on concept boundaries

**Mistake:** Not tagging concept boundary decisions at all, even though deciding where one concept ends and another begins is a significant interpretive step.

**Fix:** Always tag boundary decisions. "I split this into 3 concepts because the source has 3 numbered items" is High. "I split this into 3 concepts because it discusses 3 distinct topics" is Medium.
