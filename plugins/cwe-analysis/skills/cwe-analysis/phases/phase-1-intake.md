# Phase 1: Vulnerability Intake

## Purpose

Understand what the analyst knows about the vulnerability before attempting CWE assignment. The quality of a CWE assignment depends entirely on the quality of the vulnerability understanding.

## Process

Gather the following from the analyst. Ask questions to fill gaps — don't proceed with incomplete information.

### Step 1: Identify the Vulnerability

- **Affected software/system** — name, version, component
- **Vulnerability type** (if known) — what category does the analyst think this falls into?
- **Existing identifiers** — CVE ID, bug tracker reference, advisory URL
- **Existing CWE assignment** — if one exists, note it for later review/improvement

### Step 2: Understand the Trigger

- **How is the vulnerability triggered?** — what input, action, or condition activates it?
- **Preconditions** — what must be true for exploitation? (authentication required, specific configuration, etc.)
- **Attack scenario** — step-by-step, how would an attacker exploit this?

### Step 3: Assess the Impact

- **What happens when exploited?** — code execution, data leak, DoS, privilege escalation, information disclosure, etc.
- **Scope of impact** — single user, all users, system-level?
- **Severity estimate** — is this critical, high, medium, low?

### Step 4: Determine Available Evidence

- **Is source code available?** — if yes, where? Which files/functions are relevant?
- **Is there a proof of concept?** — exploit code, reproduction steps?
- **Is there a patch?** — comparing before/after can reveal the weakness clearly

### Step 5: Check for AI/ML Dimension

- **Is this an AI/ML system?** — LLM, computer vision, recommendation engine, autonomous agent?
- **Does the vulnerability involve model behavior?** — prompt injection, adversarial inputs, model loading?
- **Does an AI component generate the attack output?** — AI executing commands, generating web content?

This determines whether AI relevance scoring applies in later phases.

## Teaching Moment

> **Why intake matters for CWE assignment:** A CWE describes a specific type of weakness in software. If you don't understand the vulnerability precisely — what's wrong with the code, not just what the attacker can do — you'll assign a CWE that describes the impact rather than the flaw. "The vulnerability allows code execution" could be CWE-78, CWE-89, CWE-94, CWE-502, or dozens of others. The intake phase narrows this down before you ever look at the CWE list.

## Output

Present a structured vulnerability summary:

- **Software:** [name, version, component]
- **Trigger:** [how it's exploited]
- **Impact:** [what happens]
- **Evidence available:** [code/PoC/patch]
- **AI/ML system:** [yes/no, details]
- **Existing identifiers:** [CVE, CWE if any]

Then pause: "Here's my understanding of the vulnerability. Anything to correct or add before I proceed to CWE identification?"

If source code is available, suggest proceeding to Phase 2 (Code Analysis). Otherwise, skip to Phase 3.
