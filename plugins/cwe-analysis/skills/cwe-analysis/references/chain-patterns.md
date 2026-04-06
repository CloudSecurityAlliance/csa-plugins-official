# Common CWE Chain Patterns

These are common patterns, not exhaustive. Real vulnerabilities may follow chains not listed here. The chain tool (`cwe-tool.py chain`) can show what MITRE relationships exist between any set of CWEs.

A chain represents the causal flow from root weakness to final impact, with each link representing a distinct weakness that enables the next.

## Pattern 1: Web SQL Injection Chain

**Chain:** CWE-1287 (Improper Validation of Specified Type of Input) --> CWE-89 (SQL Injection) --> CWE-200 (Exposure of Sensitive Information)

**Causal flow:** The application fails to validate that input conforms to the expected type or format at the trust boundary. Unsanitized input reaches SQL query construction, allowing attacker-controlled queries. Exfiltrated data exposes sensitive information such as credentials, personal data, or internal system details.

**MITRE relationships:** CWE-89 is ChildOf CWE-943 (Improper Neutralization of Special Elements in Data Query Logic) in view 1000.

**Note:** Older references use CWE-20 (Improper Input Validation) as the root cause, but CWE-20 is discouraged for CVE assignment because it is too broad. Use the most specific input validation failure CWE that applies (e.g., CWE-1287, CWE-1284, CWE-1285).

## Pattern 2: Command Execution Chain

**Chain:** CWE-1287 (Improper Validation of Specified Type of Input) --> CWE-78 (OS Command Injection) --> CWE-269 (Improper Privilege Management)

**Causal flow:** The application fails to validate input type/format, allowing OS command metacharacters through the application boundary. Unsanitized input reaches shell execution, allowing arbitrary command execution on the host system. The attacker inherits the application's operating system privileges, which are often excessive.

**MITRE relationships:** CWE-78 is ChildOf CWE-77 (Command Injection) in view 1000.

**Note:** Same caveat as Pattern 1 — use the specific validation failure CWE, not the discouraged CWE-20.

## Pattern 3: XSS to CSRF Chain

**Chain:** CWE-79 (Cross-site Scripting) --> CWE-352 (Cross-Site Request Forgery)

**Causal flow:** Reflected or stored XSS allows an attacker to inject JavaScript into a page viewed by an authenticated user. The injected script performs authenticated actions on behalf of the victim, bypassing CSRF protections since the request originates from the victim's browser session with valid cookies and tokens.

**MITRE relationships:** CWE-79 is PeerOf CWE-352 in view 1000 (related but distinct weaknesses). CWE-79 is ChildOf CWE-74 (Injection) in view 1000. CWE-79 CanPrecede CWE-494 (Download of Code Without Integrity Check).

## Pattern 4: AI Prompt Injection Chain

**Chain:** CWE-1427 (Improper Neutralization of Input Used for LLM Prompting) --> CWE-1426 (Improper Validation of Generative AI Output) --> CWE-78 (OS Command Injection)

**Causal flow:** Prompt injection manipulates the LLM's behavior, causing it to generate malicious output instead of the intended response. The application fails to validate or sanitize the AI's output before acting on it. The AI-generated output contains OS commands that the application executes with its own privileges.

**MITRE relationships:** These are newer CWEs (added 2023-2024). Direct CanPrecede relationships may not yet exist in MITRE data, but the causal chain is well-documented in AI security research.

## Pattern 5: Supply Chain / Model Loading Chain

**Chain:** CWE-494 (Download of Code Without Integrity Check) --> CWE-502 (Deserialization of Untrusted Data) --> CWE-94 (Improper Control of Generation of Code)

**Causal flow:** A model artifact is downloaded without integrity verification (no hash check, no signature validation). The model file contains malicious serialized data that is deserialized without safety checks. Arbitrary code executes during the deserialization process, giving the attacker control over the system.

**MITRE relationships:** CWE-502 CanPrecede CWE-94 in some views. CWE-494 represents a trust boundary violation that enables the chain.

## Pattern 6: Authentication Bypass Chain

**Chain:** CWE-287 (Improper Authentication) --> CWE-862 (Missing Authorization) --> CWE-200 (Exposure of Sensitive Information)

**Causal flow:** The authentication mechanism is improperly implemented or bypassable, allowing an attacker to establish a session without valid credentials. Without proper authentication, authorization checks are also bypassed because they depend on knowing who the user is. The attacker accesses sensitive data or functionality intended for authenticated users.

**MITRE relationships:** CWE-287 and CWE-862 are PeerOf in some views (both ChildOf CWE-284). The causal link is logical rather than always explicitly modeled in MITRE data.

## Pattern 7: Path Traversal Chain

**Chain:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory) --> CWE-434 (Unrestricted Upload of File with Dangerous Type) --> CWE-94 (Improper Control of Generation of Code)

**Causal flow:** Path traversal allows writing files outside the intended directory, bypassing upload directory restrictions. The attacker uploads a file with executable content (e.g., a web shell) to a web-accessible location. The server executes the uploaded file when it is requested, giving the attacker arbitrary code execution.

**MITRE relationships:** CWE-22 CanPrecede CWE-434 in some exploitation scenarios. CWE-434 CanPrecede CWE-94 when the uploaded file is executable.

## Pattern 8: Compound Weakness (Convergent)

**Real-world example:** CVE-2026-31979 — Himmelblau symlink privilege escalation

**Topology:** CWE-59 (Improper Link Resolution Before File Access) + CWE-693 (Protection Mechanism Failure) → root privilege escalation

**Causal flow:** The Himmelblau daemon (running as root) writes Kerberos credential cache files to `/tmp/krb5cc_<uid>` without checking for symlinks (CWE-59). Separately, a code change removed `PrivateTmp=true` from the systemd unit, exposing the daemon's `/tmp` to unprivileged users (CWE-693). Neither alone is exploitable: the symlink-following code is harmless when `/tmp` is namespaced (no attacker access), and shared `/tmp` is harmless when the daemon validates symlinks. Combined, an unprivileged user creates a symlink pointing to `/etc/shadow`, and the root daemon follows it — full privilege escalation.

**Key difference from linear chains:** In a linear chain, each link is exploitable in sequence. In a compound weakness, the individual weaknesses may be unexploitable on their own. The chain notation uses "Contributing" rather than "Root Cause → Enabling" to signal convergence rather than sequence. Neither weakness "enables" the other — they are orthogonal (one is a code flaw, the other a configuration flaw).

**When to suspect compound weaknesses:** The vulnerability description says "only exploitable when..." or "requires... combined with..." or the patch fixes two seemingly unrelated issues.

## CWE Relationship Vocabulary

Understanding MITRE's relationship types helps interpret chain data:

- **CanPrecede** — CWE A can lead to CWE B. Present but sparse in MITRE data. Indicates a known causal or enabling relationship between two weaknesses.
- **CanFollow** — Inverse of CanPrecede. CWE B can follow from CWE A.
- **ChildOf** — Taxonomic hierarchy. CWE-89 is a child of CWE-943 in view 1000. This is a classification relationship, not a causal one.
- **PeerOf** — Similar weaknesses at the same abstraction level. CWE-862 and CWE-863 are peers (both deal with authorization).
- **Requires** — CWE A requires CWE B to be exploitable. The presence of one weakness is a precondition for exploiting another.

**Important:** These relationships are taxonomic, not exploit-flow maps. A valid exploit chain may connect CWEs that have no MITRE relationship. Use the relationships as hints, not proof. The absence of a CanPrecede link does not mean a chain is invalid — it may simply mean MITRE hasn't documented that particular connection.
