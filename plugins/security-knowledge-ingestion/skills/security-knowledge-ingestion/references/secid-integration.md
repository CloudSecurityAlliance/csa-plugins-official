# SecID Integration

## What SecID Is

SecID is a meta-identifier system for security knowledge. It provides a consistent way to reference any security knowledge source — standards, regulations, frameworks, vulnerabilities, weaknesses, attack techniques — using a PURL-compatible grammar.

Format: `secid:type/namespace/name[@version][#subpath]`

Examples:
- `secid:control/nist.gov/800-53@r5#AC-2` — NIST 800-53 control AC-2
- `secid:control/cloudsecurityalliance.org/ccm@4.1#IAM-12` — CCM control IAM-12
- `secid:regulation/europa.eu/ai-act#art-6` — EU AI Act Article 6
- `secid:methodology/nist.gov/ir-8477` — NIST IR 8477 methodology

**Live service:** https://secid.cloudsecurityalliance.org/

## MCP Tools Available

Three tools via the SecID MCP server:

### `resolve`
Given a full SecID string, returns URL(s) where the resource can be found.
```
resolve("secid:control/nist.gov/800-53@r5#AC-2")
→ URL to NIST's AC-2 control page
```

### `describe`
Given a SecID without a subpath, returns registry metadata about the source — what it is, what patterns it accepts, example IDs.
```
describe("secid:control/nist.gov/800-53@r5")
→ Description of NIST 800-53, accepted ID patterns, examples
```

### `lookup`
Search for an identifier across all sources of a given type. Use when you know the ID but not the source.
```
lookup(type="control", identifier="AC-2")
→ Matches from NIST, and any other source that has an AC-2
```

## SecID v2: Data Serving

SecID v2 extends beyond identification and resolution to also serve:
- **Structured data** — the decomposed concepts, hierarchy, and metadata for a source
- **Recipes** — the tools, prompts, and steps used to produce the structured data

When checking SecID in Phase 1, the response will indicate whether structured data is available (not just metadata/URLs).

## How This Plugin Uses SecID

| Phase | SecID Use |
|-------|-----------|
| Phase 1 | Check if SecID knows about the source and has structured data |
| Phase 4 | Optionally use SecID descriptions to verify concept types |
| Phase 7 | Suggest contributing new structured data and recipes back to SecID |

## Adding SecID MCP Server

If the user doesn't have SecID configured:

```
Remote MCP server URL: https://secid.cloudsecurityalliance.org/mcp
```

No API keys, no local install, no configuration needed.

## Constructing SecID Strings

| Document Type | SecID Type | Pattern |
|--------------|-----------|---------|
| Standard with controls | `control` | `secid:control/{domain}/{name}@{version}` |
| Regulation | `regulation` | `secid:regulation/{domain}/{name}` |
| Methodology | `methodology` | `secid:methodology/{domain}/{name}` |
| Framework/guidance | `control` or `reference` | Depends on whether it defines controls |
| Best practice | `reference` | `secid:reference/{domain}/{name}` |

The namespace is always the publisher's domain name: `nist.gov`, `iso.org`, `cloudsecurityalliance.org`, `europa.eu`.
