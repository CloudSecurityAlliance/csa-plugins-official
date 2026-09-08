# Licensing

This is a **marketplace repository**: it carries several independently developed plugins, and
they do not all share one licence. This file is the map. Read it before assuming what governs a
given file.

## The rule

**A directory's own `LICENSE` governs that directory and everything beneath it.** The root
`LICENSE` applies only where no nearer `LICENSE` exists.

That precedence matters here because at least one plugin is deliberately licensed differently
from the rest, and a reader who sees only the root file would get the wrong answer.

## What applies where

| Path | Licence | Notes |
|---|---|---|
| repository root | **Apache 2.0** (`LICENSE`) | Covers the marketplace's own material: `README.md`, `CLAUDE.md`, `docs/`, `.claude-plugin/`. |
| `plugins/cwe-analysis/` | Apache 2.0 | |
| `plugins/incident-analysis/` | Apache 2.0 | |
| `plugins/nist-ir-8477-mapping/` | Apache 2.0 | |
| `plugins/security-knowledge-ingestion/` | Apache 2.0 | |
| `plugins/vulnerability-audit/` | Apache 2.0 | |
| `plugins/secid/` | **CC0 1.0** | Deliberate, and not a licence for software: the plugin here is the *methodology and identifier data*, while the SecID server and client code live in their own repositories under their own terms. CC0 puts the identifier mappings in the public domain, which is the point of an identifier registry. |
| `external_plugins/` | **per plugin** | Third-party contributions. Each carries its own licence; none is licensed by CSA. |
| bundled fonts, where present | **OFL / vendor terms** | e.g. `document-pipeline/scripts/fonts/` ships `OFL.txt` and `DejaVu-LICENSE.txt`. Fonts are never covered by a plugin's own licence. |

Where a plugin ships a `NOTICE` file, Apache 2.0 section 4(d) requires you to carry it with any
redistribution.

## Trademarks

**"Cloud Security Alliance", "CSA", "SecID" and the CSA logo are trademarks of the Cloud
Security Alliance.**

Apache 2.0 **section 6** is explicit that it grants no trademark rights, and CC0 grants none
either. So no licence in this repository lets you use CSA's marks. Concretely:

- You may use, modify and redistribute the code, including commercially.
- You may **not** present the result as a CSA product, or apply CSA's name, wordmark or logo to
  your own documents or tools.

This is why the public `document-pipeline` build ships no CSA logo and no CSA palette: a document
carrying CSA's mark is asserting that CSA published it, and a tool that applied the mark to
anyone's document would be handing out that assertion. See that plugin's `README.md`.

## Licence texts are copied, never retyped

Every Apache 2.0 file in this repository is the **verbatim** upstream text — md5
`3b83ef96387f14655fc854ddc3c6bd57`. Copyright and attribution go in `NOTICE`, which is what
section 4(d) is for; they are never written into the licence body or over its appendix.

This is worth stating because the opposite happened. Until 2026-09-08 all five Apache plugins
here carried an **altered** licence body — three word-level changes in the operative text:

| Section | Upstream | What was shipped |
|---|---|---|
| 1, *Contribution* | "submitted to Licensor" | "submitted to **the** Licensor" |
| 1, *Contributor* | "received by Licensor" | "received by **the** Licensor" |
| 4(d), *NOTICE* | "excluding **those** notices" | "excluding **any** notices" |

plus the appendix overwritten with a copyright line, and further divergence in one plugin. The
edits are legally meaningless in intent and legally significant in effect: a modified Apache text
is not Apache 2.0, it is a bespoke licence that resembles it, which is worse than either an
unaltered permissive licence or an honestly custom one.

No reader would catch that, which is the point. **Verify a licence file by checksum, not by
reading it**, and copy the text from `apache.org` or an existing verbatim copy.

## Adding a plugin

1. Put a `LICENSE` in the plugin's own directory — do not rely on the root file.
2. If it is Apache 2.0, the file must be the verbatim text (md5 above) and the copyright goes in
   a sibling `NOTICE`.
3. If it is anything else, add a row to the table above **and** say why in the Notes column. An
   unexplained licence difference reads as a mistake.
4. Bundled third-party assets — fonts, data, vendored code — keep their own licence files
   alongside them.
