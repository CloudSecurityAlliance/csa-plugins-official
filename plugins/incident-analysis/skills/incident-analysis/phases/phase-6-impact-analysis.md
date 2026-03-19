# Phase 6: Impact & Downstream Effects

## Purpose

Systematically assess who was affected by this incident, how severely, and whether the disclosed impact matches the likely actual impact. Most incident analyses undercount affected populations and underestimate cascading effects. This phase corrects for that.

## Important: Confidence Rules

Impact assessments combine source-derived facts with analytical inference. Tag every assessment:
- **Confirmed** — impact explicitly documented by multiple sources
- **Reported** — impact stated by a single source
- **Inferred** — logical deduction from confirmed facts about the incident's scope
- **Speculative** — reasonable estimate based on industry patterns or incomplete information

Prefix all analytical assessments with **"Analyst/AI assessment:"** to distinguish from source-derived information.

## Process

### Step 1: Identify Affected Populations

Enumerate every group that was or could have been affected. Go beyond the obvious "customers whose data was exposed." Consider:

- **Employees** of the breached organization — were internal systems, credentials, or HR data affected?
- **Direct customers** — the primary user base of the breached product/service
- **End users** — people whose data flows through the product even if they aren't direct customers (e.g., website visitors tracked by a breached analytics tool)
- **Business partners** — organizations with integrations, shared data, or supply chain dependencies
- **Downstream data consumers** — third parties who received data from the breached organization
- **Investors/shareholders** — for public companies, material impact on stock price and fiduciary obligations
- **Regulators** — which regulatory bodies now have jurisdiction and reporting obligations

For each population, note the estimated size (even if it's a range or order of magnitude) and how you derived that estimate.

### Step 2: Classify Impact Types Per Population

For each affected population, assess which types of impact apply. Rate each as **Critical / High / Moderate / Low / Unknown**:

| Impact Type | Description | Example |
|------------|-------------|---------|
| **Data Exposure** | Personal, financial, or sensitive data disclosed | SSNs, credentials, health records exposed |
| **Operational Disruption** | Ability to conduct business or daily activities impaired | Service outage, locked accounts, workflow interruption |
| **Safety Risk** | Physical safety or critical infrastructure at risk | Medical device data compromised, physical security systems affected |
| **Financial Harm** | Direct monetary loss or financial risk | Fraudulent transactions, credit monitoring costs, stock price impact |
| **Privacy Harm** | Loss of privacy or autonomy over personal information | Behavioral data exposed, location tracking revealed, intimate content leaked |
| **Reputational Harm** | Damage to trust, brand, or professional standing | Loss of customer trust, regulatory scrutiny, market position erosion |
| **Cascading/Systemic** | Effects that propagate beyond the immediate incident | Supply chain disruption, credential reuse enabling further breaches, industry-wide vulnerability |

Present this as a matrix: populations as rows, impact types as columns, severity ratings in cells.

### Step 3: Assess Differential Impact

Not all affected individuals experience the same harm. Assess whether certain groups face disproportionate impact:

- **Vulnerable populations** — children, elderly, disabled individuals, people in dangerous situations (e.g., domestic violence survivors whose location data was exposed)
- **Geographic variation** — different regulatory protections and remediation options by jurisdiction
- **Socioeconomic factors** — ability to take protective action (credit monitoring, changing providers) varies with resources
- **Cumulative exposure** — individuals affected by multiple breaches face compounding risk (credential stuffing, identity theft escalation)

This is often where the most analytically significant findings emerge. A breach that exposes the data of 10,000 people in witness protection is categorically different from one that exposes 10 million marketing email addresses — even though the latter has a larger number.

### Step 4: Evaluate Disclosed vs. Actual Impact

Compare what the vendor/organization has publicly stated about impact to what the evidence suggests:

- **Scope gap** — Are there affected populations the disclosure doesn't mention?
- **Severity gap** — Does the disclosure downplay the sensitivity of exposed data?
- **Duration gap** — Was the exposure window longer than disclosed?
- **Cascading gap** — Does the disclosure acknowledge downstream effects?

Where gaps exist, assess whether they appear to be:
- **Genuine uncertainty** — the organization may not yet know the full impact
- **Strategic minimization** — the disclosure appears to deliberately understate impact
- **Scope limitation** — the organization defined "impact" narrowly to exclude inconvenient populations

## Teaching Moment (if teaching mode is on)

> **Why impact analysis is separate from gap analysis:** Gap analysis asks "what aren't they telling us?" Impact analysis asks "who is actually harmed and how badly?" These are related but distinct questions. A disclosure might be complete and honest yet still fail to grapple with the real-world consequences for affected populations. Separating these phases forces us to think about impact on its own terms.
>
> **The population counting problem:** Incident disclosures almost always undercount affected populations because they define "affected" narrowly. If a chatbot vendor is breached and customer support tickets are exposed, the "affected" population isn't just the vendor's customers — it's every person who submitted a support ticket, every person mentioned in those tickets, and every organization whose internal information appeared in ticket content.
>
> **Differential impact matters:** Security incident analysis tends to focus on aggregate numbers. But the most important question isn't "how many records were exposed?" — it's "what's the worst thing that could happen to the most vulnerable person in this dataset?" A breach that exposes therapy notes for 500 people may cause more individual harm than one that exposes email addresses for 5 million.

## Output

Present to the analyst:

1. **Affected Populations Inventory** — every identified population with estimated size and basis for estimate
2. **Impact Matrix** — populations × impact types with severity ratings
3. **Differential Impact Assessment** — disproportionately affected groups and why
4. **Disclosed vs. Actual Impact** — gaps between what was said and what the evidence suggests

Then pause: "Here's my impact assessment. I've identified N affected populations with severity ratings. Do you want to adjust any populations, severity ratings, or add context about differential impact before I proceed to gap analysis?"

Wait for the analyst's input before proceeding to Phase 7.
