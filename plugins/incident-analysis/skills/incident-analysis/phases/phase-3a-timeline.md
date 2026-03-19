# Phase 3a: Timeline & Attack Chain

## Purpose

Reconstruct the chronological sequence of events and the technical attack path. Use the unified fact sheet from Phase 2 as your primary input.

## Timeline Reconstruction

Build a chronological timeline from the earliest known event to the most recent. For each entry:
- **Date** (as precise as available — exact date, week, month, or quarter)
- **Event** (what happened)
- **Confidence level** (from the confidence framework)
- **Source(s)** (which sources report this)
- **Notes** (contradictions, gaps, or context)

### Key Timeline Events to Capture

Not every incident will have all of these, but look for:
- When was the vulnerability/exposure introduced?
- When did the attacker first gain access?
- When was the breach/incident discovered? By whom?
- When was internal escalation triggered?
- When were affected parties notified?
- When was public disclosure made?
- When were patches/remediations applied?
- When did additional revelations emerge after initial disclosure?
- When did regulatory/legal actions begin?

### Timeline Contradictions

Highlight contradictions explicitly. Common patterns:
- Vendor says discovery date is later than external researcher's publication date
- Time gap between discovery and disclosure exceeds industry norms or legal requirements
- Remediation actions described don't align with the timeline of events
- Multiple disclosure dates from different sources

**Teaching moment** (if teaching mode is on):
> Timeline contradictions often reveal the most important truths. If a vendor says they discovered a breach on March 1, but a researcher published indicators of compromise on February 15, the vendor may be backdating their discovery. If there's a 6-month gap between discovery and disclosure with no explanation, that gap IS the story.

## Attack Chain Reconstruction

Produce a structured description of the technical attack path. Use MITRE ATT&CK terminology where applicable, but keep it readable for non-specialists.

### Attack Chain Stages

For each stage that applies to this incident:

1. **Initial Access** — How did the attacker get in? (phishing, vulnerability exploit, credential theft, supply chain, misconfiguration, insider)
2. **Execution** — What did the attacker run? (malware, scripts, legitimate tools)
3. **Persistence** — How did they maintain access? (backdoors, compromised accounts, scheduled tasks)
4. **Privilege Escalation** — How did they get higher access? (exploit, credential dump, misconfigured permissions)
5. **Lateral Movement** — How did they spread? (RDP, SSH, cloud service pivoting, API key reuse)
6. **Collection/Exfiltration** — What did they take and how? (database dumps, API access, cloud storage download)
7. **Detection** — How was the attack discovered? (monitoring, customer report, external researcher, attacker disclosure)
8. **Response** — What remediation was performed? (credential rotation, service shutdown, patch deployment)

Tag each stage with a confidence level. Many stages will be **Inferred** or **Speculative** — that's fine, label them clearly.

### Attack Chain Unknowns

Explicitly note what you don't know about the attack chain. "Initial access vector unknown" is more useful than guessing.

## Output

Present to the analyst:
1. **Timeline** — chronological event list with confidence tags
2. **Attack Chain** — stage-by-stage reconstruction with confidence tags
3. **Key Contradictions** — highlighted timeline conflicts
4. **Unknowns** — what we don't know and what it would take to find out

Proceed directly to Phase 3b (gap analysis) — no pause needed here since both 3a and 3b are presented together before the analyst review pause.
