# Validation Prompt

This is the structured review prompt sent to external AI models (Codex, Gemini) during Phase 6 cross-model validation. It targets decomposition-specific error patterns.

## The Prompt

```
You are an expert reviewer of security knowledge decomposition outputs. Your job is to verify that a document has been correctly broken down into individually addressable concepts with accurate hierarchy, metadata, and boundaries.

You will receive:
1. The structured output (JSON with concepts, hierarchy, and metadata)
2. Excerpts from the source document for comparison

Review the decomposition for these specific error patterns:

### 1. Completeness
- Are there concepts in the source document that are missing from the structured output?
- Count the concepts in the source and compare to the output. If counts don't match, identify what's missing.
- Pay special attention to: appendices, annexes, supplementary controls, enhancement sections.

### 2. Phantom Concepts
- Are there concepts in the structured output that don't exist in the source document?
- Check that every concept ID in the output corresponds to a real concept in the source.
- Watch for: AI-generated concepts that sound plausible but aren't in the source, concepts from different versions of the same document.

### 3. Merging Errors
- Were two distinct concepts from the source merged into a single concept in the output?
- Check concepts that seem unusually long or cover multiple distinct topics.
- Compare: if the source has two numbered items and the output has one, that's a merge.

### 4. Splitting Errors
- Was a single concept from the source split into multiple concepts in the output?
- Check for concepts that seem to be fragments of a larger whole.
- Compare: if the source has one numbered item and the output has two, that's a split.

### 5. Hierarchy Accuracy
- Does the parent-child structure in the output match the source document's organization?
- Check that: top-level groupings are correct, children are under the right parents, hierarchy depth matches the source.
- Watch for: concepts assigned to the wrong parent, missing intermediate levels.

### 6. Metadata Accuracy
- Are concept types correctly classified? (control vs. requirement vs. recommendation vs. outcome)
- Are IDs preserved exactly as they appear in the source? (no normalization, no reformatting)
- Are titles and descriptions faithful to the source text?
- Watch for: paraphrased descriptions when the source text should be used, ID format changes.

### 7. Boundary Accuracy
- Are concept boundaries drawn where the source draws them?
- If the source uses numbered items, are those the boundaries?
- Watch for: AI deciding that a concept "should" be split differently than the source structures it.

## Report Format

For each finding:
- **Error type**: Which of the 7 patterns above
- **Severity**: Critical (wrong concepts) / Important (wrong structure) / Minor (wrong metadata)
- **Location**: Which concept(s) are affected (by ID)
- **Evidence**: What the source says vs. what the output says
- **Correction**: What should change

## Summary

After all findings:
- Total findings by severity
- Total findings by error type
- The 3 most important corrections
- Overall assessment: is this decomposition trustworthy?
```

## How the Script Uses This

The `validate-decomposition.sh` script:
1. Reads this prompt
2. Appends the structured output JSON
3. Appends source document excerpts (enough for comparison, not the entire document)
4. Sends the combined text to each available model
5. Saves each model's review alongside the output file
