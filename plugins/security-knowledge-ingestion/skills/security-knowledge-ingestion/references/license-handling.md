# License Handling

License checks gate **contribution**, not **processing**. The user provided their data — they can process it however they want locally. License only matters when considering whether to contribute structured data back to SecID for public serving.

## Blocklist

These sources have known license restrictions that prevent public redistribution of full-text structured data. This is a **hard stop for data contribution** — but recipes (prompts, tools, conversion steps) are generally safe to contribute as long as they don't contain verbatim copyrighted excerpts. Before contributing a recipe, check that prompts and notes don't quote substantial portions of the source text — paraphrase or reference by section number instead.

| Source | Reason | What CAN be contributed |
|--------|--------|------------------------|
| ISO standards (full text) | Copyrighted by ISO, purchase required | Recipe only. Metadata (control count, hierarchy structure, IDs) is generally OK. |
| IEEE standards (full text) | Copyrighted by IEEE | Recipe only |
| HITRUST CSF | Licensed, requires signed agreement | Recipe only |
| PCI-DSS (full text from PCI SSC) | Requires acceptance of PCI SSC terms | Recipe only. Note: PCI-DSS is widely quoted/summarized in publicly available guidance. |
| BSI standards (full text, purchased) | Some BSI documents are licensed | Recipe only. Check individual document — some BSI publications are freely available. |

**If a source isn't on this list**, it doesn't mean it's safe to contribute — you still need to check the actual license.

## How to Find Licenses

Check in this order:

1. **The document itself** — look for license/copyright statements, usually on the title page, back matter, or footer
2. **The publisher's website** — look for terms of use, licensing page, or copyright notice on the page where the document is hosted
3. **The publisher's general terms** — e.g., nist.gov/terms, iso.org/terms
4. **Common knowledge** — US government publications are generally public domain (17 U.S.C. §105), EU official documents have specific reuse rules

## License Outcomes

| Status | Can contribute data? | Can contribute recipe? | User guidance |
|--------|---------------------|----------------------|---------------|
| **Public domain** (US gov, CC0) | Yes | Yes | "This is public domain — both data and recipe can be contributed." |
| **Open license** (CC-BY, CC-BY-SA) | Yes (with attribution) | Yes | "This has an open license — data and recipe can be contributed with proper attribution." |
| **Restricted/commercial** | No | Yes | "Licensed content — the structured data can't be contributed for public serving. You can still contribute the recipe." |
| **Unknown** | No (until confirmed) | Yes | "We couldn't confirm the license. You can use this locally. Contributing requires confirmed license. Recipe can always be contributed." |

## Government Publications

Many government publications are freely available and sometimes public domain, but not always:

| Jurisdiction | General Rule | Exceptions |
|-------------|-------------|------------|
| US federal | Public domain (17 U.S.C. §105) | Some NIST publications have third-party contributions with separate licenses |
| EU institutions | Reuse generally permitted (Decision 2011/833/EU) | Check individual documents for restrictions |
| UK government | Open Government Licence (usually) | Check Crown copyright terms |
| Other | Check specific jurisdiction | No assumption of openness |

## What This Means in Practice

**Phase 7 flow:**

1. User wants to contribute → check blocklist first
2. If not blocked → ask about or find the license
3. Present findings → user confirms
4. Based on license status → advise on what can be contributed (data + recipe, or recipe only)
5. Never auto-file, auto-push, or auto-contribute
