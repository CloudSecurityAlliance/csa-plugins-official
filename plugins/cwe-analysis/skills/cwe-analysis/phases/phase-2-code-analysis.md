# Phase 2: Code Analysis

## Purpose

Examine the actual vulnerable code path to identify where weaknesses manifest. This is optional — skip if no source code is available. But when code IS available, it dramatically improves CWE assignment accuracy by moving from description-based matching to evidence-based matching.

## When to Skip

Skip this phase if:
- No source code is available
- The analyst has already traced the code path and can describe it
- The vulnerability is well-documented with a clear patch diff

## Process

### Step 1: Locate the Entry Point

Find where external input enters the system:
- User-provided data (forms, API parameters, file uploads)
- Configuration values from external sources
- Data from other systems (APIs, databases, message queues)
- Model files or training data (for AI systems)

### Step 2: Trace the Data Flow

Follow the input from entry point to where it causes harm:
- What functions does it pass through?
- Where does it cross trust boundaries? (user input → internal API → database)
- Where should validation/sanitization exist but doesn't?
- Are there any transformations that change the input's nature?

### Step 3: Identify Weakness Points

Mark specific locations in the code where weaknesses manifest:
- **Root cause** — where is the fundamental flaw? (e.g., missing input validation)
- **Enabling weakness** — what allows the flaw to be exploitable? (e.g., dynamic query construction)
- **Symptom** — where does the vulnerability actually manifest? (e.g., unsanitized data reaches SQL engine)

### Step 4: Compare with Patch (if available)

If a fix exists, compare before/after:
- What changed? What was added, removed, or modified?
- Does the fix address the root cause or just the symptom?
- Does the fix introduce any new weakness patterns?

### Step 5: Document the Code Path

Create an annotated summary:
- File names and line numbers for each weakness point
- The data flow from input to impact
- Trust boundaries crossed
- Root cause vs. symptom distinction

## Teaching Moment

> **Root cause vs. symptom:** If user input reaches a SQL query without sanitization, the symptom is SQL injection (CWE-89). But the root cause may be missing input validation at the trust boundary (CWE-20), or the use of string concatenation for query construction instead of parameterized queries. Both matter for CWE assignment — the primary CWE should describe the most specific weakness, but the chain should capture the full picture.
>
> **Why patches reveal CWEs:** A diff between vulnerable and fixed code often reveals the weakness more clearly than the vulnerability description. If the fix adds parameterized queries, the weakness was CWE-89. If it adds an allowlist filter, the weakness may be CWE-20 or CWE-1287. The fix tells you what was missing.

## Output

Present an annotated code path:
- Entry point → data flow → weakness points → impact
- Specific files and line numbers where each weakness manifests
- Root cause vs. symptom distinction
- Trust boundaries crossed

Then pause: "Here's what I found in the code. Does this match your understanding of the vulnerability?"
