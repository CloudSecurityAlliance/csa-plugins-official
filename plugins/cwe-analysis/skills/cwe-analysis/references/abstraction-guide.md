# CWE Abstraction Level Guide

The CWE hierarchy has four abstraction levels. Choosing the right level is critical — too abstract and the assignment is useless, too specific and it may not accurately describe the weakness.

## Definitions

- **Pillar** — The highest, most abstract level. Describes a broad concept (e.g., CWE-284 "Improper Access Control"). Never assign a Pillar directly — it's too vague for a CVE record. Pillars are organizational categories, not weakness descriptions.

- **Class** — A broad category of weakness (e.g., CWE-74 "Injection"). Use only when no Base or Variant fits. A Class describes a general pattern of weakness but lacks specificity about the mechanism.

- **Base** — The most common and appropriate level for CVE assignment (e.g., CWE-89 "SQL Injection"). Describes a specific weakness type without being tied to a particular technology. Most CWE assignments should be at Base level.

- **Variant** — The most specific level, tied to a particular technology or context (e.g., CWE-564 "SQL Injection: Hibernate"). Preferred when one exists that matches. Variants narrow a Base to a specific technology, language, or framework.

## Decision Tree

```
Is there a Variant that matches the vulnerability? --> Use the Variant
   | No
   v
Is there a Base that matches? --> Use the Base
   | No
   v
Is there a Class that matches? --> Use the Class (document why no Base/Variant fits)
   | No
   v
Pillar? --> Never assign directly. If nothing more specific fits, document why.
```

The decision tree starts at the most specific level and works upward. At each step, if you cannot find a match, move one level up. If you end up at Class, document your reasoning. If you end up at Pillar, something has gone wrong — either the vulnerability is too vaguely described to classify, or there is a more specific CWE you haven't found yet.

## Discouraged CWEs

These CWEs appear frequently in CVE records but should be avoided or replaced with more specific alternatives:

| CWE | Name | Why Discouraged | Use Instead |
|-----|------|-----------------|-------------|
| CWE-20 | Improper Input Validation | Too broad — nearly every vulnerability involves input in some way | The specific injection or validation failure CWE (CWE-89, CWE-79, etc.) |
| CWE-NVD-noinfo | Insufficient Information | Placeholder, not a real weakness | Investigate further or use Best Fit confidence with the closest real CWE |
| CWE-noinfo | Insufficient Information | Same as above | Same as above |
| CWE-Other | Other | Not a real weakness classification | Find the actual CWE that describes the weakness |

When you encounter these in existing CVE records, treat them as starting points for investigation, not as valid assignments. The goal is always to reach the most specific accurate CWE.

## MITRE CNA Mapping Guidance Summary

MITRE's official guidance for CVE Numbering Authorities (CNAs) aligns with this framework:

- CNAs should assign the most specific CWE possible
- Use Base or Variant level when available
- If uncertain, CWE-NVD-noinfo is acceptable temporarily but should be refined
- Multiple CWEs can be assigned when a vulnerability involves a chain of weaknesses
- Reference: https://cwe.mitre.org/documents/cwe_usage/guidance.html

This plugin follows MITRE's guidance while adding the confidence framework to make uncertainty explicit rather than hidden behind placeholder CWEs.
