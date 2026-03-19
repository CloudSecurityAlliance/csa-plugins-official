# Methodology Rationale & Design Decisions

This document explains why the incident analysis methodology is structured the way it is — the goals it serves, the intellectual traditions it draws from, why each phase exists and is ordered the way it is, and how to think about modifying it.

If you're an analyst wondering "why do we do it this way?" — this document is for you. If you think something should be different — read this first, then open an issue to discuss it (see [Discussion & Feedback](#discussion--feedback) at the end).

## Goals & Philosophy

This plugin has three goals, in order of priority:

### 1. Produce rigorous, defensible incident analysis

Every claim is tagged with a confidence level. Every source is assessed for bias. Every AI inference is explicitly labeled. The output should withstand scrutiny from someone who wasn't part of the analysis — a CSA analyst briefing leadership, a controls mapper building on the findings, or an external reviewer evaluating the methodology.

Defensibility comes from transparency, not authority. We don't ask you to trust the analysis — we show you the evidence, the reasoning, and the uncertainty so you can evaluate it yourself.

### 2. Teach the methodology as it executes

This plugin doesn't just produce analysis — it shows its work and explains why each step matters. Teaching mode is on by default because learning is a first-class goal, not a secondary feature.

The reasoning: an analyst who understands the methodology will catch things the AI misses. An analyst who knows why we check community sources can recognize when the AI failed to find a critical Reddit thread. An analyst who understands bias assessment can spot when the AI gave too much weight to a vendor disclosure. An analyst who has internalized the confidence framework can flag when a claim was tagged "Confirmed" on thin evidence.

The AI handles breadth and systematization. The human provides judgment, domain expertise, and the ability to say "that doesn't smell right." Teaching the methodology equips the human to play that role effectively.

### 3. Keep the human in control at decision points

Pause points exist where analytical judgment matters most:
- **After collection** — "Are the sources complete? Am I missing something from my domain knowledge?"
- **After source analysis** — "Are these confidence levels right? Do I know something that changes the assessment?"
- **After impact assessment** — "Are the affected populations correct? Are severity ratings appropriate?"
- **After gap analysis** — "Are these speculative inferences warranted? Should I steer this differently?"

The AI does the systematic work (searching, cross-referencing, tabulating, checking regulatory deadlines). The human makes the judgment calls (is this source trustworthy? is this inference reasonable? did we miss an affected population?). The pause points are where those judgment calls happen.

### The Unifying Idea

This is a **human-AI collaboration tool, not an automation tool**. If the plugin could produce perfect analysis without human input, it wouldn't need pause points or teaching mode. It can't — and acknowledging that is a design strength, not a limitation.

## Intellectual Lineage

This methodology didn't emerge from a vacuum. It draws on established traditions and adapts them for OSINT-based, post-hoc cloud incident analysis. Understanding the lineage helps you evaluate the choices and follow the threads if you want to go deeper.

### Intelligence Community Analytic Cycle

The overall phase structure follows the intelligence community's cycle: **collection → processing → analysis → dissemination**. Our adaptation:
- Collection (Phases 1-2) gathers open-source information rather than classified intelligence
- Processing (Phases 3-4) establishes reliability and context rather than decrypting or translating
- Analysis (Phases 5-8) reconstructs events, assesses impact, identifies gaps, and generates recommendations
- Dissemination (Phase 9) produces a structured report rather than an intelligence brief

The key difference: intelligence analysis typically works from ongoing collection with evolving access. We work from a fixed, publicly available evidence base that we gather after the fact. This means our collection phase needs to be more systematic about exhausting available sources, because we can't task a collector to go find more.

**Further reading:** *Psychology of Intelligence Analysis* by Richards J. Heuer Jr. (CIA Center for the Study of Intelligence) — foundational text on analytic rigor and cognitive bias in intelligence work.

### NIST SP 800-61 (Incident Response Lifecycle)

Our timeline reconstruction and response assessment draw on NIST's **detection → analysis → containment → eradication → recovery → post-incident activity** framework. Our adaptation:
- We're analyzing incidents after the fact, not responding in real-time, so our "detection" maps to understanding how the incident was discovered and how long it took
- Our regulatory compliance overlay (Phase 5) adds a dimension NIST doesn't emphasize — whether the response met legal notification obligations
- Our impact assessment (Phase 6) goes deeper than NIST's post-incident activity recommendations on measuring what actually happened to affected populations

**Further reading:** NIST Special Publication 800-61 Rev. 2, "Computer Security Incident Handling Guide."

### Structured Analytic Techniques (SATs)

The confidence framework and bias framework are directly influenced by the intelligence community's structured analytic techniques — systematic methods for managing uncertainty and mitigating cognitive bias. Our adaptation:
- The confidence framework (see `confidence-framework.md`) is a simplified version of multi-dimensional reliability ratings, focused on source agreement and independence
- The bias framework (see `bias-framework.md`) applies SAT principles to the specific source types common in OSINT incident analysis (vendor disclosures, news, researchers, community)
- The explicit labeling of AI inferences ("Analyst/AI assessment:") follows the SAT principle of separating observation from interpretation

**Further reading:** *Structured Analytic Techniques for Intelligence Analysis* by Richards J. Heuer Jr. and Randolph H. Pherson.

### NATO/Admiralty Reliability Rating System

Our confidence levels are adapted from the NATO/Admiralty system, which rates both source reliability (A-F) and information credibility (1-6). Our adaptation simplifies this into a single dimension because:
- In OSINT analysis, source reliability and information credibility are more tightly coupled than in classified intelligence (we generally can't separate "reliable source, incredible information" as cleanly)
- Our analysts need a framework they can apply quickly during iterative analysis, not a two-axis matrix
- We added "Disputed" as an explicit level because source contradiction is common and analytically significant in OSINT

### Architecture Decision Records (ADRs)

This document itself is influenced by the ADR methodology — capturing not just what was decided, but why, what alternatives were considered, and what the context was. This is deliberate: if the reasoning is captured, future contributors can evaluate whether the reasoning still holds rather than treating decisions as arbitrary.

**Further reading:** Michael Nygard's original ADR proposal and the adr-tools project.

## Phase Rationale Summary

Each phase exists for a specific reason and is positioned deliberately in the sequence. This table gives the quick answer. The [Cross-Cutting Design Decisions](#cross-cutting-design-decisions) section below explains the deeper structural principles.

| Phase | Why It's a Separate Phase | Why It's in This Position | Key Alternative Considered |
|-------|--------------------------|--------------------------|---------------------------|
| **1. Discovery** | Incident selection shapes everything downstream — analyzing the wrong incident, or misunderstanding which incident the analyst means, wastes all subsequent work | Must be first — nothing else can proceed without a confirmed target | Considered skipping when the analyst already has an incident in mind; kept as an explicit step because even "I know what I want" benefits from quick verification and scoping |
| **2. Collection** | Comprehensive collection prevents confirmation bias — you can't analyze what you didn't gather. Historical context (new in this version) catches repeat patterns and broken remediation promises | Before analysis — all sources must be gathered before cross-referencing begins | Considered interleaving collection with analysis; rejected because premature analysis biases what you search for next |
| **3. Source Analysis** | Confidence classification and bias assessment are the evidentiary foundation — every later phase depends on knowing what's reliable and what's suspect | After collection (needs all sources), before deep analysis (establishes what we can trust) | Considered combining with collection; rejected because collection is about breadth (find everything) while analysis is about depth (evaluate what we found) |
| **4. Vendor Analysis** | Understanding what a breached product does and what access it had is mandatory context for supply chain and third-party incidents — without it, you can't assess blast radius or shared responsibility | After source analysis (needs reliable facts about the vendor), before timeline (informs what events to look for) | Considered making optional; kept mandatory because virtually all cloud incidents have a vendor/third-party dimension |
| **5. Timeline** | Chronological reconstruction reveals contradictions and compliance failures that narrative analysis misses. Regulatory overlay (new in this version) assesses whether notification deadlines were met | Needs source analysis and vendor context as inputs; produces the temporal structure that impact and gap analysis examine | Considered combining with attack chain only; added regulatory overlay because compliance deadlines are independently important and legally consequential |
| **6. Impact** | Most analyses undercount affected populations and underestimate severity — a dedicated phase forces systematic population-by-population assessment with explicit severity ratings | After timeline (need to know what happened before assessing who it hurt), before gap analysis (impact findings reveal disclosure gaps) | **New phase.** Previously folded into gap analysis, but impact assessment is factual/analytical while gap analysis is speculative — mixing them blurred confidence levels and buried impact findings |
| **7. Gap Analysis** | Reading between the lines — identifying what's not being said — is the highest-value analytical activity but also the most speculative, requiring explicit labeling and analyst judgment | After all factual phases are complete — speculation should be informed by the fullest possible picture | Considered combining with impact; rejected because gap analysis is deliberately speculative while impact assessment aims for evidentiary grounding |
| **8. Defensive Recommendations** | Analysis without actionable output is academic exercise — recommendations translate findings into things people can actually do | After gap analysis (needs all findings from Phases 4, 6, and 7), before report (recommendations are a core deliverable) | **New phase.** Previously implicit in gap analysis as "what should we do differently?" but was never systematically developed with prioritization tiers, finding traceability, and reality-checking |
| **9. Report** | The deliverable must stand alone — a reader who wasn't part of the analysis needs to understand everything from a single document | Last — synthesizes all prior work into a coherent whole | Considered incremental report generation during analysis; rejected because synthesis benefits from seeing the complete picture and avoids the report contradicting itself as understanding evolves |

## Cross-Cutting Design Decisions

These decisions span multiple phases or reflect fundamental design choices. Each follows the ADR pattern: decision, context, alternatives considered, and reasoning.

### 1. Pause Points as Human Judgment Gates

**Decision:** Four pause points where the analyst reviews output before the next phase proceeds — after collection (Phase 2), source analysis (Phase 3), impact assessment (Phase 6), and gap analysis (Phase 7).

**Context:** The AI is systematically thorough but lacks domain expertise and the ability to recognize when something "doesn't smell right." The analyst has domain knowledge, institutional context, and intuition developed from experience, but may not have time to be systematically exhaustive.

**Alternatives considered:**
- *Pause after every phase:* Rejected — it slows the workflow at phases where the AI's output is more mechanical (discovery, vendor research, timeline reconstruction, recommendation generation, report writing). These phases benefit from analyst review in the final report, but don't need a dedicated pause.
- *No pauses (fully autonomous):* Rejected — it contradicts the human-AI collaboration model. The AI will make mistakes that only a human with domain knowledge can catch.

**Reasoning:** Pauses are placed where analytical judgment matters most:
- **After collection:** The analyst knows sources the AI can't find (internal reports, personal contacts, subscription content, prior experience with this vendor)
- **After source analysis:** Confidence levels require judgment about source credibility that benefits from domain expertise
- **After impact:** Population identification and severity ratings directly affect the analysis's conclusions and recommendations — getting these wrong cascades
- **After gap analysis:** Speculative inferences are the highest-risk output; analyst review is essential before these feed into recommendations

### 2. Teaching Mode On by Default

**Decision:** Teaching annotations are included by default. The analyst can disable them with "skip teaching" or "expert mode."

**Context:** This plugin serves analysts with varying experience levels. Teaching mode explains why each step matters, names patterns, and points out analytical subtleties.

**Alternatives considered:**
- *Off by default, opt-in:* Rejected — the analysts who benefit most (less experienced) are the least likely to know to ask for it. Defaulting to off optimizes for experts at the expense of learners.
- *Separate "learning mode" that's fundamentally different:* Rejected — the teaching content is woven into the analytical workflow, not a separate track. Separating them would mean maintaining two parallel workflows.

**Reasoning:** The cost of teaching mode for experts is minimal — a few extra paragraphs they can skip or disable. The benefit for learning analysts is substantial — they develop the skills to evaluate and improve the AI's work. The "expert mode" escape hatch exists for analysts who don't need it.

### 3. Confidence Tagging on Every Claim

**Decision:** Every factual assertion in the analysis gets a confidence tag (Confirmed / Corroborated / Reported / Inferred / Speculative / Disputed).

**Context:** Incident analysis that doesn't distinguish "we know this" from "we think this" is dangerous — it presents speculation with the same weight as confirmed facts. The intelligence community learned this lesson through decades of analytic failures.

**Alternatives considered:**
- *Confidence only on "key" claims:* Rejected — it requires judgment about what's "key" before the analysis is complete. A claim that seems minor early on may turn out to be pivotal.
- *Binary (confirmed/unconfirmed):* Rejected — too coarse. The difference between "single credible source" and "pattern-based speculation" is analytically significant and affects how readers should weight the claim.

**Reasoning:** The six-level framework (adapted from NATO/Admiralty classification) provides enough granularity to be useful without being so complex that it's burdensome. The framework is described in `confidence-framework.md` and is loaded once, then applied throughout.

### 4. Explicit Bias Assessment

**Decision:** Every source is assessed for motivation and bias using a structured framework (`bias-framework.md`).

**Context:** OSINT incident analysis draws from sources with strong, predictable incentive structures. Vendor disclosures minimize scope. News outlets sensationalize. Security researchers may overstate novelty. Community sources mix genuine insiders with uninformed speculation.

**Alternatives considered:**
- *Trust "credible" sources at face value:* Rejected — "credible" is exactly what bias assessment is trying to determine. A vendor's disclosure is "credible" in the sense that they have direct knowledge, but biased in the sense that they're incentivized to minimize.
- *Only assess bias when sources conflict:* Rejected — bias shapes what sources say even when they don't contradict each other. Vendors and news outlets can agree on a misleading narrative if neither has incentive to challenge it.

**Reasoning:** Explicit bias assessment surfaces the question "who benefits from this version of events?" for every source. This doesn't mean dismissing biased sources — it means understanding how the bias shapes what they chose to report and how they framed it.

### 5. Separation of Factual Analysis from Speculative Analysis

**Decision:** Phases 1-6 aim for factual grounding (even impact assessment rates severity against evidence). Phase 7 is explicitly speculative. Phase 8 bridges back to actionable recommendations.

**Context:** Reading between the lines — identifying what's not being said, what can be inferred from gaps and patterns — is the highest-value analytical activity. But it's also the most prone to false positives and confirmation bias.

**Alternatives considered:**
- *Allow speculation throughout all phases:* Rejected — unlabeled speculation in earlier phases contaminates the evidentiary foundation. If a speculative claim in Phase 3 gets treated as confirmed in Phase 5, the timeline is built on a false premise.
- *Prohibit speculation entirely:* Rejected — gap analysis is where the most important insights often emerge. "The vendor didn't mention X" is speculative but can be the most valuable finding in the entire analysis.

**Reasoning:** By making Phase 7 the designated home for speculative analysis, we can apply stricter confidence rules (everything tagged Inferred or Speculative, everything prefixed "Analyst/AI assessment:") without suppressing valuable work. Analysts know what they're getting in Phase 7, and readers of the report can calibrate their trust accordingly.

### 6. Progressive Disclosure (Skill Architecture)

**Decision:** SKILL.md is a router that contains the workflow overview. Phase files are read on-demand when each phase is reached. Reference material (confidence framework, bias framework, this document) is loaded when first needed.

**Context:** The complete methodology, if loaded as a single document, would overwhelm both the AI's context and the analyst's attention. Not every phase's details are needed at every moment.

**Alternatives considered:**
- *Single monolithic skill file:* Rejected — it would be enormous and the AI would have to hold all phases in context simultaneously, degrading performance on the current phase.
- *Fully decomposed with no overview:* Rejected — the analyst and AI both need to understand the overall workflow and where they are in it. The routing file provides that context.

**Reasoning:** Progressive disclosure mirrors how human experts actually work — you don't review the entire methodology manual before starting each analysis. You know the overall flow, then dive into the details of the phase you're currently executing. The AI operates the same way: it reads SKILL.md for the overview, then reads each phase file as it gets there.

## Principles for Modification

This methodology is not sacred. It should evolve as the threat landscape changes, as we learn from applying it, and as the AI's capabilities improve. But changes should be deliberate and reasoned, not arbitrary.

If you're considering a modification, use these principles to evaluate it:

### When to Add a Phase

A new phase is warranted when:
- **It addresses a gap that produces materially worse analysis when missing.** Phases 6 (Impact) and 8 (Defensive Recommendations) were added because their absence meant analyses were missing critical dimensions — who was actually harmed, and what should be done about it.
- **It has a distinct analytical mode from adjacent phases.** If the new phase requires a different kind of thinking (factual vs. speculative, systematic vs. creative, collection vs. analysis), it deserves its own space.
- **Its outputs feed multiple downstream phases.** Impact assessment feeds both gap analysis and recommendations. If a new phase would similarly serve as an input to multiple later phases, that independence is worth preserving.

A new phase is probably NOT warranted when:
- It could be a section within an existing phase without losing analytical rigor
- It doesn't have a distinct confidence level or analytical mode
- It only serves one downstream consumer

### When to Add a Pause Point

A pause point is warranted when:
- **The analyst's domain knowledge could materially change the output.** Collection pauses because the analyst may know sources the AI can't find. Gap analysis pauses because speculative inferences need human judgment.
- **Getting it wrong cascades into later phases.** Impact severity ratings affect recommendations. Confidence levels affect the entire evidentiary foundation.
- **The output is high-stakes or high-uncertainty.** Speculative content (gap analysis) and severity ratings (impact) both benefit from human review before they feed into recommendations and the final report.

A pause is probably NOT warranted when:
- The phase's output is primarily mechanical (timeline reconstruction from already-validated facts)
- The analyst will review the output as part of the final report anyway
- Adding the pause would break analytical flow without adding judgment value

### When to Modify Phase Order

The current order follows a principle: **each phase should only consume outputs from phases that precede it**. If you're considering reordering:
- Map the data dependencies — what does each phase need as input?
- Verify the new order doesn't create circular dependencies or require a phase to consume outputs that don't exist yet
- Consider whether the new order changes where pause points should fall

### When to Retire a Phase

A phase should be retired when:
- Its function has been absorbed by improvements to adjacent phases
- The problem it addresses no longer exists (unlikely for core analytical functions, more likely for technology-specific phases)
- Experience shows it consistently produces low-value output that doesn't contribute to the final report

Before retiring a phase, check whether any downstream phase depends on its specific outputs.

### The Meta-Principle

Every structural decision in this methodology should be traceable to one of the three goals: rigorous analysis, teaching the methodology, or keeping the human in control. If a proposed change doesn't serve at least one of these goals, it probably doesn't belong. If it conflicts with one of them, the conflict needs to be explicitly acknowledged and reasoned about.

## Discussion & Feedback

This methodology is under active development. If you disagree with a design decision, think a phase should work differently, or believe the methodology has a gap — we want to hear from you.

**Methodology discussion is explicitly welcome.** A methodology that can't withstand scrutiny shouldn't be trusted, and one that doesn't evolve becomes stale. We treat methodology disagreements the same way we treat bugs — they're issues to be investigated, discussed, and resolved.

To start a discussion:

1. Go to: https://github.com/CloudSecurityAlliance/csa-plugins-official/issues
2. Click **"New Issue"**
3. Title it: `[incident-analysis] Methodology: <brief description>` (e.g., `[incident-analysis] Methodology: Phase 6 should include financial impact modeling`)
4. In the body, tell us:
   - **What you'd change** — which phase, decision, or structural element
   - **Why** — what problem does the current approach cause, or what improvement would your change enable?
   - **What you've considered** — have you thought about how this change would interact with other phases or design decisions? (This document's phase rationale and design decisions sections are useful context here)

We may agree immediately, we may push back with reasoning, or we may discover a better approach through discussion. All three outcomes are valuable.

See `../../FEEDBACK.md` for the full feedback guide, including bug reports, feature requests, and other ways to contribute.
