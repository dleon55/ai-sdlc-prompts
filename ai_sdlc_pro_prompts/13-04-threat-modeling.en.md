# 13.4 — Threat Modeling

## Description

Prompt to perform threat modeling of a system, component, or feature before or during its design. Identifies attack surfaces, malicious actors, threat vectors, and mitigation controls using the STRIDE methodology. Generates security input for prompts `13-01` (SAST) and `13-03` (Secure SDLC review).

**When to use:** in the design phase of new security-impacting features, when designing integrations with external systems, when changing the authentication or authorization model, or when introducing handling of sensitive data.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | security |
| Expected risk | medium — this is design-time analysis with no code execution, but a threat missed at this stage can become a real, unnoticed vulnerability during implementation |
| Required inputs | description of the system/component to model, solution design (`04-01`) or use cases (`04-03`) if they exist, architecture or flow diagrams (`04-02`), authentication model and sensitive data involved |
| Allowed tools | reading of existing design, architecture, and code — no execution or changes; the DFD and attack trees are generated as structured text |
| Permitted autonomy | A0 — Analyze the design and generate the STRIDE threat model |
| Stop criteria | do not invent components, flows, or integrations that are not described in the actual design or code; if no design is available, request it before modeling speculative threats |
| Expected output | see `## Expected output` |
| Minimum evidence | each threat references the actual affected component/flow, STRIDE category, risk score (likelihood × impact), and proposed mitigation control |
| Recommended next prompt | `13-01-sast-analisis-seguridad-codigo`, using this threat model as context for known attack surfaces once the design is implemented |

---

## Mandatory previous context

> Include the block from `00-framework.md` before this prompt.
> Attach the solution design (`04-01`) or use cases (`04-03`) if available.
> Attach existing architecture or flow diagrams (`04-02`).

---

## Complete prompt

```text
Objective:
Perform threat modeling of the indicated system or component using the STRIDE
methodology, identify attack surfaces, malicious actors, threat vectors,
and required mitigation controls.

Steps:

1. SYSTEM DESCRIPTION
   Describe the system or component to analyze:
   - system purpose
   - legitimate actors (users, systems, external services)
   - data processed, stored, or transmitted
   - trust boundaries: where the trust level changes between components
     (e.g., internet → load balancer, client → API, API → DB)
   - involved technologies: language, framework, database, queues, external APIs

2. DATA FLOW DIAGRAM (DFD level 0 and level 1)
   Generate in structured text (to convert to diagram) the components and flows:
   - external entities (users, external systems)
   - processes (services, functions, modules)
   - data stores (DB, cache, files, sessions)
   - data flows between components (indicate if trusted or untrusted)
   - trust boundaries (represent with dotted line)

3. THREAT IDENTIFICATION — STRIDE METHODOLOGY
   For each significant component and flow, evaluate the 6 STRIDE categories:

   S — Spoofing (Identity impersonation)
   Can an attacker impersonate a legitimate user or component?
   - Examples: stolen credentials, forged JWTs, ARP spoofing, DNS spoofing
   - Typical controls: strong authentication (MFA), mutual TLS certificates, digital signatures

   T — Tampering (Modification)
   Can an attacker modify data in transit or at rest without detection?
   - Examples: SQL injection, URL parameter manipulation, man-in-the-middle
   - Typical controls: HTTPS, message signing (HMAC), integrity validation, ORM

   R — Repudiation (Denial of actions)
   Can an actor deny having performed an action?
   - Examples: absence of audit logs, manipulable logs, no transaction signing
   - Typical controls: immutable audit logging, transaction signing, timestamps

   I — Information Disclosure
   Can an attacker access data they're not entitled to?
   - Examples: IDOR, stack trace in errors, exposed config files,
     data in logs, listable directories
   - Typical controls: access control, output encoding, secure error handling,
     least privilege principle

   D — Denial of Service
   Can an attacker degrade or interrupt the service?
   - Examples: request flood, costly unconstrained queries, unlimited uploads,
     infinite recursion, database lock
   - Typical controls: rate limiting, timeouts, pagination, input size validation,
     circuit breaker

   E — Elevation of Privilege
   Can an attacker obtain more privileges than assigned?
   - Examples: IDOR accessing other users' resources, bypassing role verification,
     command injection running as root, manipulable JWT role
   - Typical controls: backend authorization (never client-side only), signed tokens,
     resource ownership verification, sandbox

4. ATTACK TREES — top 3 highest-risk scenarios
   For the 3 most critical identified scenarios:
   - attack scenario name
   - attacker objective
   - required preconditions
   - attack steps (decision tree)
   - estimated likelihood: [HIGH / MEDIUM / LOW]
   - estimated impact: [CRITICAL / HIGH / MEDIUM / LOW]

5. THREAT CLASSIFICATION BY RISK
   Prioritize all identified threats with:
   - threat ID
   - STRIDE category
   - affected component
   - vector description
   - likelihood (1-3)
   - impact (1-3)
   - risk = likelihood × impact (1-9)
   - proposed mitigation control
   - status: [UNMITIGATED / MITIGATED / ACCEPTED]

6. ATTACK SURFACE
   Document the total attack surface of the system:
   - exposed HTTP/API endpoints (internal and external)
   - user interfaces (web, mobile, CLI)
   - message queues or event streams
   - file import/export
   - third-party integrations (webhooks, OAuth, APIs)
   - administration interfaces
   - maintenance scripts or batch jobs

7. SECURITY ARCHITECTURE RECOMMENDATIONS
   List the security controls to implement or validate before development,
   grouped by layer:
   - Network layer: WAF, firewall, segmentation, TLS
   - Application layer: authentication, authorization, validation, rate limiting
   - Data layer: encryption at rest, encryption in transit, minimal DB access
   - Operations layer: security logging, alerts, secret rotation

Constraints:
- don't invent components, flows, actors, or integrations that aren't described in the actual design or code; if no design is available, request it before modeling speculative threats,
- this is a read-only design exercise: don't implement mitigations or modify code, infrastructure, or configuration as part of this modeling,
- don't include real credentials, tokens, internal hostnames, or working exploit payloads in the DFD or threat descriptions — describe vectors abstractly, enough to communicate them without turning the document into an attack recipe,
- if the model reveals a threat that is already exploitable in the current system (not just in design), flag it as an urgent finding and route it to `13-01` or the security reporting channel instead of only documenting it as a future threat,
- every threat must reference the actual affected component or flow; don't assign likelihood or impact without justifying the criteria used.

Deliverables:
- textual DFD of the system with marked trust boundaries,
- complete STRIDE threat table with risk and mitigation,
- top 3 attack trees with attack steps,
- attack surface map,
- required security controls list by layer,
- this document serves as mandatory input for 13-01 (SAST) and 13-03 (Secure SDLC).
```

---

## Standard formula usage

```text
Use the threat modeling prompt and adapt it to:
- repository: [NAME OR URL]
- system or feature to model: [DESCRIPTION]
- legitimate actors: [USERS, EXTERNAL SYSTEMS]
- sensitive data involved: [PII / financial / credentials / none]
- external integrations: [LIST OF EXTERNAL APIS OR SERVICES]
- authentication model: [JWT / session / OAuth2 / API key]
- documents to review: solution design (04-01), use cases (04-03),
  diagrams (04-02), repository architecture
- specific output goal: STRIDE threat model + mitigation controls
- depth level: high
```

---

## Expected output

### Data flow diagram (textual)

```
[User] → (Login) → [User DB]
[User] → (API /prompts) → [Prompts service] → [Prompts DB]
[Prompts service] → (integration) → [External API]
---- Trust boundary: Internet / API ----
---- Trust boundary: API / Database ----
```

### STRIDE threat table

| ID | STRIDE | Component | Threat vector | Likelihood | Impact | Risk | Mitigation | Status |
|---|---|---|---|---|---|---|---|---|
| T-001 | Spoofing | API /login | Forged JWT with alg:none | 2 | 3 | 6 | Validate alg explicitly, use trusted library | Unmitigated |
| T-002 | Tampering | DB | Concatenated SQL in search | 3 | 3 | 9 | ORM / parameterized queries | Unmitigated |
| T-003 | Info Disclosure | API errors | Stack trace in 500 response | 3 | 2 | 6 | Generic error handling in production | Unmitigated |
