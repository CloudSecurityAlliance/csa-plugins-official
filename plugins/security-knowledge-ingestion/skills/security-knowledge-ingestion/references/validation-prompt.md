# Validation Prompt

This is the canonical review prompt loaded by `scripts/validate-decomposition.sh` at runtime. Edit this file to change validation behavior — the script reads it directly, nothing is hardcoded.

The prompt text must be between the ``` fences below. The script extracts everything between the first and second ``` lines.

## The Prompt

```
You are an expert reviewer of security knowledge decomposition outputs. Your job is to verify that a document has been correctly broken down into individually addressable concepts with accurate hierarchy, metadata, and boundaries.

You will receive:
1. The structured output (JSON with concepts, hierarchy, and metadata)
2. The source document for comparison (if provided — may be markdown, text, or other readable format)

If no source document is provided, do your best with internal consistency checks and your knowledge of the referenced source. Flag reduced confidence when you cannot verify against the source.

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
1. Loads this prompt by extracting text between the ``` fences above
2. Appends the structured output JSON
3. Appends the source document (if a second argument was provided)
4. Writes the combined text to a temp file (avoids CLI argument-size limits)
5. Pipes the temp file to each available model via stdin
6. Saves each model's review alongside the output file

**To change validation behavior:** Edit the prompt text between the fences above. The script will pick up changes on the next run. No script modifications needed.
