Analyze the following CAIQ response data and return a JSON object with scores (0-4) plus a readability assessment. Use the rules below to guide your scoring.

---

## 1. Scores to Provide

1. **CSP Implementation Description Score** - integer (0-4)
2. **Final Overall Score** - integer (0-4)
3. **Readability Feedback** - textual analysis of clarity, organization, grammar, etc.

> **Note**: The CAIQ Answer might be "Yes," "No," or "NA."
> - If "No," the maximum possible score for that component (and for the overall score) is **2**.
> - "Yes" or "NA" answers can reach up to **4**, depending on completeness.

---

## 2. Scoring Criteria (0-4)

Use these definitions for each component and for the Final Overall Score:

- **0 - Fails / Non-Compliant / Major Contradiction**
  - Incoherent or no meaningful content.
  - Severe contradiction (e.g., chosen answer says "Yes," but text says "we do not implement this control").
  - Empty or irrelevant text for the element being scored.

- **1 - Weak / Minimal**
  - Very limited detail or vague explanation.
  - Minimal effort or incomplete information.

- **2 - Basic / Partial**
  - Basic explanation covering some requirements, but key details missing.
  - Partial alignment with guidelines.
  - If the vendor's answer is "No," a well-explained response can earn a 2, but **cannot** exceed 2.

- **3 - Strong / Meets Expectations**
  - Solid coverage of the relevant control requirements.
  - Clear, specific implementation details with no major gaps.
  - Aligns well with applicable guidelines or best practices.

- **4 - Excellent / Exceeds Expectations**
  - Comprehensive, highly detailed explanation.
  - Clearly addresses CSP vs. CSC roles if relevant.
  - Fully aligns with recommended guidelines and provides strong supporting evidence.

---

## 3. Contradictions and Capping Rules

### Major Contradiction → Automatic 0
If the explanation clearly conflicts with the stated answer (Yes/No/NA), that component (or the Final Overall Score if it invalidates the entire response) should be **0**. Document the contradiction in the **Readability Feedback**.

### "No" Cap at 2
If the vendor's official answer is **"No"**, the highest possible score for that component (and for the Final Overall Score) is **2**.

---

## 4. Readability Feedback

After assigning numeric scores, **evaluate the clarity and organization** of the response. Provide constructive feedback on:
- Clarity of language and logical flow
- Grammar, spelling, and terminology consistency
- Comprehensibility for both technical and non-technical audiences
- Any confusing or ambiguous statements

This **Readability Feedback** does **not** directly alter the numeric scores but helps the respondent improve.

---

## 5. Output Format

Your analysis must be returned in **JSON** with at least these fields:

```json
{
  "Question ID": "[Original Question ID]",
  "SSRM Control Ownership Score": "(integer 0-4)",
  "SSRM Control Ownership Score Justification": "Justification and reasoning for the score",
  "SSRM Control Ownership Feedback": "Feedback on the SSRM Control Ownership information",
  "SSRM Control Ownership Feedback Justification": "Justification and reasoning for the feedback",
  "CSP Implementation Description Score": "(integer 0-4)",
  "CSP Implementation Description Score Justification": "Justification and reasoning for the score",
  "CSP Implementation Description Feedback": "Feedback on the CSP Implementation Description information",
  "CSP Implementation Description Feedback Justification": "Justification and reasoning for the feedback",
  "CSC Responsibilities Feedback": "Feedback on the CSC Implementation Description information",
  "CSC Responsibilities Feedback Justification": "Justification and reasoning for the feedback",
  "Score": "(integer 0-4)",
  "Score Justification": "Justification and reasoning for the overall score",
  "Readability Feedback": "Feedback on the overall readability"
}
```

If any contradictions or special conditions arise, include a brief rationale in Readability_Feedback or as an additional note.

## 6. Application Notes
- While the Final Overall Score often reflects a blend or average of the three component scores, you may adjust it for overarching contradictions.
- For "NA", the score must range between 0 and 4 if the explanation is thorough and well-justified.
- If ownership is shared, evaluate how thoroughly each party's responsibilities are described.
- Provide feedback (in the Readability_Feedback field) for any missing or unclear detail.

Your analysis must be returned in the specified JSON format.
