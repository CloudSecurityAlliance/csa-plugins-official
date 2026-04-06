# Concept Types

Security knowledge documents contain different types of concepts. Identifying the type correctly matters because it affects how the concept is decomposed, what metadata to capture, and how downstream mapping tools interpret it.

## Primary Concept Types

| Type | What It Is | Example Sources |
|------|-----------|----------------|
| **Control** | A specific security requirement or capability that can be implemented, assessed, and audited | NIST 800-53, CCM, ISO 27001 Annex A |
| **Requirement** | A mandatory statement (SHALL/MUST) that must be satisfied for conformance | ISO 27001 clauses, PCI-DSS requirements |
| **Recommendation** | A non-mandatory statement (SHOULD/MAY) suggesting best practice | NIST guidance documents, best practice guides |
| **Outcome** | A desired result or state to achieve, without specifying how | NIST CSF subcategories, high-level framework goals |
| **Capability** | A concrete product/service feature that implements a control | AWS S3 encryption, Azure AD MFA |
| **Article** | A legal provision in a regulation | EU AI Act articles, GDPR articles |
| **Clause** | A section in a standard that may contain requirements | ISO 27001 clauses 4-10 |
| **Category/Domain** | A grouping of related concepts at a higher level | CCM domains, CSF categories, NIST control families |
| **Technique** | An adversary behavior or attack method | ATT&CK techniques, CAPEC patterns |
| **Procedure** | A step-by-step process for achieving something | Assessment procedures, audit procedures |
| **Function** | A high-level organizational activity | CSF functions (Identify, Protect, Detect, Respond, Recover) |

## How to Identify Concept Types

**Look at the language:**
- "shall" / "must" → Requirement
- "should" / "recommended" → Recommendation
- "ensure that" / "the organization shall" → Requirement (outcome-phrased)
- Numbered items with verifiable criteria → Control
- Legal text with "Article N" → Article

**Look at the structure:**
- Flat numbered list with testable items → Controls
- Hierarchical legal text → Articles/Clauses
- Goal-oriented statements without implementation detail → Outcomes
- Detailed step-by-step instructions → Procedures

**A document may contain multiple types.** For example:
- ISO 27001 has both Clauses (requirements in clauses 4-10) and Controls (Annex A)
- NIST CSF has Functions, Categories, and Subcategories (all different granularity of outcomes)
- EU AI Act has Titles, Chapters, Articles, and Paragraphs

## Hierarchy vs. Type

Don't confuse hierarchy level with concept type. A "domain" is a hierarchy level (grouping), not a concept type. The concepts within a domain might be controls, requirements, or outcomes. Both the hierarchy level AND the concept type should be captured.

Example:
- CCM IAM = Domain (hierarchy level), contains Controls (concept type)
- CCM IAM-12 = Control (hierarchy level AND concept type)
- CSF Identify = Function (hierarchy level AND concept type)
- CSF ID.AM-1 = Subcategory (hierarchy level), Outcome (concept type)

## Alignment with NIST IR 8477

NIST IR 8477 uses the term "concept type" to describe the same idea: "There are many types of cybersecurity and privacy concepts, including controls, requirements, recommendations, outcomes, technologies, functions, processes, techniques, roles, and skills."

When this plugin produces structured data that will be used with the NIST IR 8477 mapping plugin, the concept types identified here are the same concept types that NIST IR 8477 §3 asks you to document as part of the use case.
