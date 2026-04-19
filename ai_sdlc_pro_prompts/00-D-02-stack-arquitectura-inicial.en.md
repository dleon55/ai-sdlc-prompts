# 0-D.2 — Initial Stack & Architecture: Selection and Documentation of Technical Foundation

## Description

Prompt for defining, justifying, and documenting the **initial technology stack and foundational architectural decisions** of a new project. Covers everything from language and runtime selection to infrastructure topology, data model, and integration patterns.

**When to use it:** after approving the Project Charter (`00-D-01`) and before generating individual ADRs (`04-04-adr-decisiones-arquitectura.md`), repository structure (`00-B-01`), or the implementation plan (`05-01-plan-implementacion.md`).

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.

---

## Full prompt

```text
Objective:
Define and document the initial technology stack and foundational architectural decisions for the project, with justification for each choice and evaluation of discarded alternatives.

Required inputs:
- project name: [NAME]
- domain description: [what the system does, who the users are, approximate volume]
- system type: [REST API / GraphQL / SPA web app / mobile / data pipeline / microservices / modular monolith / serverless / embedded / other]
- known constraints: [cloud budget, team skills, mandatory corporate technologies, deadlines, licenses, compliance: GDPR/HIPAA/PCI/SOC2/other]
- preliminary stack (if any): [language, framework, DB — may be tentative or empty]
- expected scale: [concurrent users, requests/sec, data volume, availability SLA]
- deployment platform: [AWS / GCP / Azure / on-premise / Kubernetes / VPS / serverless / hybrid]
- team: [roles and sizes — developers, QA, ops, AI agents]

Deliver the following sections:

1. EXECUTIVE STACK SUMMARY
   Complete table with columns: Layer | Chosen Technology | Version/tier | Status (confirmed / tentative) | Evaluated Alternative | Reason for Choice
   Cover layers:
   - Primary language / runtime
   - Application framework
   - Primary database (relational / document / column-store)
   - Secondary database or cache (Redis, Memcached, etc.)
   - Message broker / queue (if applicable: Kafka / RabbitMQ / SQS / Pub/Sub)
   - API gateway / reverse proxy
   - Authentication & authorization (OAuth2 / OIDC / JWT / SAML)
   - Object storage (S3, GCS, blob)
   - Infrastructure: compute (VM, container, serverless, bare metal)
   - Container orchestrator (Docker Compose / Kubernetes / ECS / Cloud Run)
   - CI/CD pipeline
   - Container registry
   - Observability: metrics (Prometheus / CloudWatch / Datadog)
   - Observability: distributed tracing (Jaeger / Zipkin / OTEL)
   - Observability: centralized logs (Loki / ELK / CloudWatch Logs)
   - Frontend (if applicable: framework, build tool, CDN)
   - Monorepo vs. multi-repo: decision and management tool

2. INFRASTRUCTURE TOPOLOGY
   - describe the deployment model in text: zones, networks, load balancers, edge
   - suggest an architecture diagram in Mermaid format (C4 level 2 — Container Diagram or Architecture Diagram)
   - specify if the system is multi-region or single-region and why

3. SELECTED ARCHITECTURAL PATTERNS
   For each chosen pattern, state: pattern | reason | when to apply it | when NOT to scale to it
   Candidates to evaluate:
   - modular monolith vs. microservices vs. modular monolith
   - CQRS (read/write separation)
   - Event sourcing
   - Saga pattern (for distributed transactions)
   - API Gateway + BFF (Backend for Frontend)
   - Circuit breaker and retry with exponential backoff
   - Strangler Fig (incremental migration)
   - Hexagonal / Ports & Adapters
   Select only those applicable to the project; justify the discarded ones.

4. INITIAL DATA MODEL
   - primary domain entities (max. 10): name, description, key relationships
   - propose whether the model is relational, document-oriented, hybrid, or event-driven
   - migration strategy: [Alembic / Flyway / Liquibase / Rails migrations / Prisma Migrate / other]
   - soft delete vs. hard delete policy
   - multi-tenancy strategy if applicable: [schema-per-tenant / row-level / database-per-tenant]

5. SECURITY BY DESIGN
   - authentication model: [token type, expiration, refresh strategy]
   - authorization model: [RBAC / ABAC / ACL / policy-based]
   - primary attack surface and planned controls
   - secrets management: [Vault / AWS Secrets Manager / GCP Secret Manager / Azure Key Vault / .env with rotation]
   - encryption: in transit (minimum TLS) and at rest (whose managed key)
   - compliance to meet: [applicable standards and required controls]

6. SCALABILITY AND RESILIENCE STRATEGY
   - horizontal vs. vertical scaling: decision and scaling trigger (CPU %, RPS, latency)
   - cache strategy: [L1/L2 levels, invalidation, TTL]
   - queue management and backpressure
   - target SLA/SLO: availability (99.9% / 99.95% / 99.99%), latency P50/P95/P99
   - DR (Disaster Recovery) strategy: target RPO and RTO

7. ANTICIPATED TECHNICAL DEBT AND ARCHITECTURAL RISKS
   Table with columns: Technical Decision | Generated Debt or Risk | When to Review | Impact if Not Reviewed
   (highlight conscious trade-offs: e.g. "we chose monolith now, extraction plan to microservices in phase 2")

8. ARCHITECTURAL EVOLUTION PLAN
   - milestones where the architecture must be reviewed (due to load, features, team growth)
   - criteria for moving from a simpler pattern to a more complex one (e.g., when to migrate from monolith to microservices)
   - dependencies that must be resolved before scaling

9. NEXT STEPS
   Ordered list of immediate actions:
   - ADRs to generate (use 04-04-adr-decisiones-arquitectura.md) for each critical decision
   - repository scaffolding (use 00-B-01-scaffolding-repositorio.md)
   - quality tooling setup (use 00-B-05-stack-calidad-codigo.md)
   - GitHub configuration (use 00-B-03-github-configuracion.md)
   - methodology definition (use 00-B-04-metodologia-framework.md)
   - AI agent governance (use 00-B-02-gobernanza-ia-agentes.md)

Output format:
- Structured document with all sections above
- Markdown tables where indicated
- Mermaid diagram for the topology (section 2)
- Technically precise language; justify each choice with engineering criteria
- Mark with [PENDING DECISION: reason] any point requiring more information or team vote
- Mark with [ADR REQUIRED] each decision that must be formalized in an Architecture Decision Record
```

---

## Usage notes

- This prompt produces the **technical foundation document** of the project. Each decision marked with `[ADR REQUIRED]` must subsequently be documented using prompt **`04-04-adr-decisiones-arquitectura.md`**.
- The Mermaid diagram generated in section 2 can be refined with prompt **`04-02-diagramas-mermaid.md`**.
- The stack table from section 1 feeds directly into repository scaffolding (`00-B-01`) and code quality configuration (`00-B-05`).
- For projects with strict security requirements, complement with **`13-04-threat-modeling.md`** before finalizing the architecture.
