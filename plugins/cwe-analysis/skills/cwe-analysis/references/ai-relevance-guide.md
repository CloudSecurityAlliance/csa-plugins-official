# AI Relevance Guide

This guide explains the two-view AI relevance model used to annotate CWE assignments for vulnerabilities in AI/ML systems. AI relevance is a **post-classification overlay** — apply it only after identifying the correct CWE based on weakness properties. The CWE should be chosen because it accurately describes the weakness, not because it has a high AI relevance score.

## The Two-View Model

AI security vulnerabilities can be understood from two complementary perspectives. A single vulnerability may score on one or both views.

### View 1: Attacks ON AI

**Question:** "Can this weakness be used to attack, compromise, or manipulate an AI system?"

This view covers weaknesses that target the AI system itself:

- **Model extraction / inversion / theft** — Extracting model weights, training data, or decision boundaries
- **Training data poisoning / backdoors** — Corrupting the training process to embed malicious behavior
- **Adversarial inputs / prompt injection** — Crafting inputs that cause the AI to behave incorrectly or maliciously
- **AI infrastructure attacks** — Targeting the serving infrastructure, model registries, or inference pipelines
- **Supply chain attacks (malicious models)** — Distributing tampered model files through repositories or package managers

### View 2: Attacks VIA AI

**Question:** "Would attackers specifically want AI to produce or execute this weakness?"

This view covers weaknesses that AI systems can create or trigger:

- **AI agent executes shell commands** — Command Injection (CWE-77/78) when an AI agent has shell access
- **AI generates malicious HTML/JS** — Cross-site Scripting (CWE-79) when AI output is rendered in browsers
- **AI makes requests to internal URLs** — Server-Side Request Forgery (CWE-918) when AI agents can make HTTP requests
- **AI writes to sensitive paths** — Path Traversal (CWE-22) when AI agents have file system access

**Key constraint:** This view only scores highly when AI output IS the attack payload. If the AI is merely incidental to the vulnerability (e.g., a SQL injection in a web form that happens to be on an AI company's website), View 2 does not apply.

## Scoring Scale

| Score | Label | Definition |
|-------|-------|------------|
| 0 | Not Applicable | This view does not apply to this CWE in AI contexts |
| 1 | Weakly Applicable | Edge cases only; requires unusual configurations or unlikely scenarios |
| 2 | Moderately Applicable | Relevant to AI systems but not a primary concern |
| 3 | Highly Applicable | Significant AI relevance; commonly encountered in AI security assessments |
| 4 | Primary Example | This CWE is exactly what this view describes; a canonical example |

## The 8 Score-4 CWEs

These CWEs represent the most direct intersection of traditional weakness classification and AI security.

### Attacks ON AI (View 1 = 4)

- **CWE-1427: Improper Neutralization of Input Used for LLM Prompting** — The canonical attack on LLMs. Prompt injection is the defining weakness of current-generation language model applications.
- **CWE-1039: Automated Recognition Mechanism with Inadequate Detection or Handling of Adversarial Input Perturbations** — Attacks on ML recognition systems. Adversarial examples that cause misclassification in vision, audio, or other ML models.
- **CWE-502: Deserialization of Untrusted Data** — Malicious model files. Serialized model formats (particularly Python-based formats) can execute arbitrary code when loaded.
- **CWE-1434: Insecure Default Initialization of Inference Engine Resource** — Misconfigured inference parameters such as temperature, top_k, or other generation settings that affect model behavior and safety.

### Attacks VIA AI (View 2 = 4)

- **CWE-77/78: Command Injection / OS Command Injection** — AI agents that execute shell commands. When an LLM agent has access to a shell, prompt injection can lead directly to command execution.
- **CWE-918: Server-Side Request Forgery (SSRF)** — AI agents that make HTTP requests to internal URLs. An LLM with web access can be manipulated into probing internal networks.
- **CWE-1426: Improper Validation of Generative AI Output** — The defensive linchpin. This CWE describes the failure to validate what the AI produces before the application acts on it. It is the missing check that enables most "attacks via AI" chains.

## Four Attack Surfaces

AI systems present four distinct attack surfaces, each with different CWE coverage:

### Supporting Infrastructure
Servers, APIs, databases, and networks hosting the AI system. These are well-covered by existing CWEs (injection, authentication, access control, etc.). Traditional security applies fully.

### AI System Core
The model itself, prompts, inference pipeline, and training process. This surface is poorly covered by existing CWEs — only approximately 4 AI-specific CWEs exist (CWE-1426, CWE-1427, CWE-1039, CWE-1434). Many AI-specific weaknesses lack precise CWE mappings.

### AI-Controlled/Generated Systems
Code, configurations, actions, and content that AI produces. Traditional CWEs apply to the OUTPUT — if the AI generates SQL, CWE-89 applies to that generated SQL. The twist is that the AI is the source of the malicious input, not a human attacker.

### AI Knowledge/Supply Chain
Training data, web search results, retrieval-augmented generation (RAG) sources, plugins, and integrations. Trust boundary analysis is critical here. Data from these sources crosses into the AI's context and can influence its behavior.

## When to Apply

Apply AI relevance scoring when the vulnerability involves an AI/ML system. This includes:

- Large language models (LLMs) and their applications
- Computer vision systems
- Recommendation engines
- Autonomous agents and AI assistants
- Any system that uses machine learning models for inference or decision-making

Do **NOT** apply when the vulnerability is in traditional software that happens to be used by an AI company. A SQL injection in a company's marketing website is not AI-relevant just because the company builds AI products.

## How to Use the Data

- `cwe-tool.py lookup <ID>` shows AI relevance scores if classification exists for that CWE
- `cwe-tool.py ai-relevant --min-score N` lists all CWEs at or above the specified threshold score
- AI relevance is annotation, not identification — the correct CWE may not be AI-tagged, and that is fine. Choose the CWE that describes the weakness, then check if it has AI relevance annotations.

The absence of an AI relevance score does not mean a CWE is irrelevant to AI systems. It may simply mean the classification has not yet been performed for that CWE. The bundled AI relevance data covers the most commonly encountered CWEs in AI security contexts but is not exhaustive.
