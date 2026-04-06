# Phase 1: Source Identification

## Purpose

Understand what the user has and check if SecID already knows about it.

## Steps

### Step 1: Identify the Document

Ask the user or determine from the file/URL:

- **Title**: What is this document called?
- **Publisher**: Who published it? (NIST, ISO, CSA, EU, etc.)
- **Version**: What version/revision/edition? (e.g., r5, 2022, v4.1)
- **Document type**: Standard, regulation, framework, guidance, benchmark, best practice?
- **Content type**: What kind of concepts does it contain? Controls, requirements, outcomes, capabilities, articles?

If the user provided a file, examine it to determine these. If they provided a name or description, confirm your understanding before proceeding.

### Step 2: Check SecID

Construct a candidate SecID string and check whether SecID knows about this source.

**How to construct the SecID:**

| Document Type | SecID Pattern | Example |
|--------------|---------------|---------|
| Standard/Framework with controls | `secid:control/{namespace}/{name}@{version}` | `secid:control/nist.gov/800-53@r5` |
| Regulation | `secid:regulation/{namespace}/{name}` | `secid:regulation/europa.eu/ai-act` |
| Methodology | `secid:methodology/{namespace}/{name}` | `secid:methodology/nist.gov/ir-8477` |
| Best practice/guidance | `secid:reference/{namespace}/{name}` | `secid:reference/cloudsecurityalliance.org/ccm-guidance` |

Use the `describe` tool first to check if the source exists in SecID's registry:

```
describe(secid: "secid:control/nist.gov/800-53@r5")
```

Then try `resolve` to check if SecID v2 has structured data:

```
resolve(secid: "secid:control/nist.gov/800-53@r5")
```

**If SecID tools are not available** (degraded mode): Skip this step. Inform the user: "SecID tools aren't available — skipping the check for existing structured data. You can add SecID as a remote MCP server: `https://secid.cloudsecurityalliance.org/mcp`." Proceed with the user's file.

### Step 3: Present Findings

Based on the SecID check, present one of these outcomes:

**SecID has structured data (v2):**
> "SecID has a pre-structured version of {title} ({version}). It includes structured data and the recipe used to produce it. Would you prefer to use that instead, or continue with your file?"

User chooses. Their file is the default — don't push SecID.

**SecID knows about it but has no structured data:**
> "SecID recognizes this source ({secid string}) and can resolve it to {url}, but doesn't have structured data yet. We'll process your file. At the end, you'll have the option to contribute the structured data back."

**SecID doesn't know about it:**
> "This source isn't in SecID's registry yet. We'll process your file. At the end, you'll have the option to contribute both the structured data and the SecID registry entry."

Note the SecID status — Phase 7 uses this to decide whether to nudge for contribution.

## Output

A **source identification record**:

- Title
- Publisher
- Version
- Document type
- Content type (what kinds of concepts it contains)
- SecID string (if constructable)
- SecID status: `has_data` | `known_no_data` | `unknown` | `secid_unavailable`

Carry this forward — every subsequent phase references it.

## Teaching Moment (if teaching mode is on)

> **Why SecID matters here:** SecID is a community registry of security knowledge. If someone has already processed this exact document into structured data, you don't need to redo the work. And if you do process it, contributing back means the next person doesn't have to either. This is how a community corpus gets built — one document at a time, each building on the last.
