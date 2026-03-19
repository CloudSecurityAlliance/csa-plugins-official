# Phase 5: Timeline & Attack Chain

## Purpose

Reconstruct the chronological sequence of events and the technical attack path. Use the unified fact sheet from Phase 3 as your primary input.

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

### Regulatory Compliance Timeline Overlay

After reconstructing the timeline, overlay regulatory notification deadlines to assess compliance. This is especially important for incidents involving personal data or critical infrastructure.

**Key regulations and their notification windows:**

| Regulation | Notification Deadline | Who Must Be Notified | Applies When |
|-----------|----------------------|---------------------|-------------|
| GDPR (Art. 33/34) | 72 hours to DPA; "without undue delay" to data subjects | Supervisory authority + affected individuals | Personal data of EU/EEA residents involved |
| SEC (8-K Item 1.05) | 4 business days after determining materiality | SEC + investors via 8-K filing | Material cybersecurity incident at a public company |
| HIPAA (Breach Notification Rule) | 60 days to individuals; 60 days to HHS (if 500+) | HHS, affected individuals, media (if 500+ in a state) | Protected health information involved |
| U.S. State Breach Laws | Varies: "most expedient time possible" to 30-90 days | Affected residents, state AG (varies) | PII of state residents involved |
| NIS2 (EU) | 24h early warning, 72h full notification | National CSIRT/competent authority | Essential or important entities in the EU |
| DORA (EU) | "Without undue delay" (specific timelines per RTS) | Competent financial authority | Financial entities in the EU |
| PIPEDA (Canada) | "As soon as feasible" | Privacy Commissioner + affected individuals | Real risk of significant harm to Canadians |
| APRA CPS 234 (Australia) | 72 hours (material incidents); 10 days (control weaknesses) | APRA | APRA-regulated financial entities |

**Assessment framework:** For each applicable regulation:
1. **When did the notification clock start?** — The trigger event (discovery, determination of materiality, confirmation of personal data involvement)
2. **What was the deadline?** — Calculate from the trigger event
3. **Was it met?** — Compare actual notification date to the deadline
4. **What are the consequences of missing it?** — Fines, enforcement actions, litigation risk

**Teaching moment** (if teaching mode is on):
> **The "awareness" ambiguity:** Most regulations start the clock when the organization "becomes aware" of the breach — but awareness is slippery. Does it start when a SOC analyst sees an alert? When the CISO is briefed? When the forensic investigation confirms data exfiltration? Vendors often exploit this ambiguity to buy time. When analyzing the timeline, note exactly when different levels of awareness occurred and which interpretation the vendor appears to be using.

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
2. **Regulatory Compliance Overlay** — which deadlines applied, whether they were met, consequences
3. **Attack Chain** — stage-by-stage reconstruction with confidence tags
4. **Key Contradictions** — highlighted timeline conflicts
5. **Unknowns** — what we don't know and what it would take to find out

Proceed directly to Phase 6 (impact analysis) — no pause needed here since the analyst will review findings at the Phase 7 pause.
