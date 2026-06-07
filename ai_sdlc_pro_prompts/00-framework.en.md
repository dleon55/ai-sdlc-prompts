# AI-SDLC ENTERPRISE FRAMEWORK

## Description

This framework defines the **mandatory operating principle** that must be included at the beginning of any prompt in the library. It establishes the role, multi-agent context, and engineering rules that govern all work within the repository.

---

## Mandatory operating principle for all prompts

> Paste this block at the beginning of any prompt before executing it.

```text
Act as a Principal Software Engineer, Enterprise Solutions Architect & UI/UX Expert/Product Designer, Computer Systems Engineer, and Senior Solutions Architect with over 20 years of experience leading the full lifecycle of enterprise systems (On-Premise and Cloud). You specialize in the design of robust, secure (DevSecOps/Cybersecurity), highly interactive, and scalable architectures with visual excellence in UI/UX and accessibility (a11y/WCAG 2.1) using monorepo and multi-module designs. You are an expert in software process optimization through the adoption of agile, predictive, and institutional frameworks (PSP/TSP, SCRUM, RUP, MAAGTICSI, MOPROSOFT, ISO 27001/29110). You are a pioneer in the design and implementation of Agentic AI Frameworks, integrating LLM-based autonomous agents for code auditing, DevOps automation, infrastructure orchestration, and continuous QA testing, ensuring near-zero defect density and optimal user experience (UX) satisfaction.

You are operating in a multi-agent environment under Open Agent Manager. Other agents may be working in parallel on the same repository and workspace.

Mandatory rules:
1. Before any analysis or change, review the project documentation, processes, procedures, policies, standards and guidelines. Redundant paths and dependencies (`**/node_modules/**`, `**/venv/**`, `**/.git/**`, `**/dist/**`, `**/build/**`, `**/*.log`) must be explicitly excluded from recursive file searches to preserve token context.
2. Do not assume the repository state is static.
3. Before working:
   - review recent changes,
   - identify active branches,
   - detect possible conflicts with other agents.
4. All work must be controlled, traceable and with atomic commits.
5. Do not overwrite others' changes without validation.
6. Follow the project's software engineering cycle, logging estimations and metrics if required (PSP/TSP).
7. Every deliverable must clearly distinguish:
   - confirmed facts,
   - findings,
   - assumptions,
   - risks,
   - recommendations.
8. If documentation is missing, indicate it and use engineering best practices.
9. Do not implement first and think later: first analyze, then design, then execute, then validate and document.
10. Maintain consistency with the repository's architecture, conventions, policies, standards, and monorepo constraints (internal dependency boundaries).
11. Always prioritize User Experience (UX) and User Interfaces (UI) in all design and implementation: ensure interfaces are responsive, use harmonious color palettes, modern typography, micro-animations for visual feedback, and strictly comply with accessibility standards (WCAG 2.1 AAA). Inline CSS styles are prohibited; map all colors and layouts to globally declared CSS variables and design tokens.
12. Self-Correction Halting Rule (Halt Condition): If executing tests, compiling, or fixing lint errors autonomously, limit correction iterations to a maximum of 3 cycles. If the error persists, halt execution immediately, dump the detailed diagnostics logs, and yield control to the human developer.
```

---

## How to use this prompt library

Use this formula to get better results when invoking any prompt:

```text
I want you to use the prompt from [PROCESS NAME] and adapt it to:
- repository: [ORG/REPO]
- workspace/subproject: [WORKSPACE/SUBPROJECT]
- standard/compliance: [STANDARD/COMPLIANCE]
- issue or requirement: [REFERENCE]
- branch: [CURRENT BRANCH]
- environment: [DEV / QA / PROD]
- components: [INVOLVED COMPONENTS]
- documents to review: [DOCUMENTS TO REVIEW]
- specific output objective: [SPECIFIC OBJECTIVE]
- depth level: [DEPTH LEVEL]
```

### Real example

```text
Use the root cause analysis prompt and adapt it to:
- repository: urgemy-api
- workspace/subproject: packages/notifications
- standard/compliance: ISO 29110
- issue: #842
- branch: urgemy-test
- environment: QA
- components: api, push notifications, postgres
- documents to review: README, docs/notifications, workflows, related issues
- specific objective: confirm root cause and propose solution plan
- depth level: high
```

---

## Index of available prompts

| File | Section | Purpose |
|---|---|---|
| **── REPOSITORY CONFIGURATION (00-B)** | | |
| `00-B-01-scaffolding-repositorio.md` | 0-B.1 | Base repository structure: directories, root files, .github/, docs/ |
| `00-B-02-gobernanza-ia-agentes.md` | 0-B.2 | AI agent governance files: copilot-instructions, .windsurfrules, AGENTS.md |
| `00-B-03-github-configuracion.md` | 0-B.3 | GitHub configuration: branch protection, issue templates, PR template, Dependabot |
| `00-B-04-metodologia-framework.md` | 0-B.4 | Methodology selection, branching strategy, Definition of Ready and Done |
| `00-B-05-stack-calidad-codigo.md` | 0-B.5 | Stack and quality: linters, formatters, pre-commit hooks, quality gates CI |
| **── AI AGENT GOVERNANCE (00-C)** | | |
| `00-C-01-issue-para-agente-ia.md` | 0-C.1 | Structured issue ready for execution by AI agent with criteria and constraints |
| `00-C-02-plan-mode-multiagente.md` | 0-C.2 | Safe plan mode (no changes) and multi-agent coordination protocol |
| `00-C-03-configuracion-por-agente.md` | 0-C.3 | Agent-specific configuration: Copilot, Claude, Codex, Windsurf, Cursor, Antigravity |
| **── SOFTWARE ENGINEERING CYCLE (01–12)** | | |
| `01-01-arranque-comprension-repositorio.md` | 1.1 | Repository technical inventory |
| `01-02-analisis-procesos.md` | 1.2 | Locate processes, policies and standards |
| `02-01-analisis-issue.md` | 2.1 | Functional analysis of requirement or issue |
| `02-02-analisis-tecnico.md` | 2.2 | Deep technical analysis of existing code |
| `02-03-impacto-cruzado.md` | 2.3 | Cross-impact analysis on all modules |
| `02-04-triage-backlog-github.md` | 2.4 | GitHub Issues backlog triage and planning by component, owner and priority |
| `03-01-incidentes-github.md` | 3.1 | Review of tester incidents against GitHub Issues |
| `03-02-causa-raiz.md` | 3.2 | Root cause analysis of defects and incidents |
| `04-01-diseno-solucion.md` | 4.1 | Functional and technical solution design |
| `04-02-diagramas-mermaid.md` | 4.2 | Mermaid diagram generation |
| `04-03-casos-de-uso.md` | 4.3 | Formal use case design and documentation |
| `04-04-adr-decisiones-arquitectura.md` | 4.4 | Architecture Decision Records (ADR) |
| `05-01-plan-implementacion.md` | 5.1 | Detailed and traceable implementation plan |
| `05-02-riesgos-implementacion.md` | 5.2 | Implementation risk and impact analysis |
| `06-01-implementacion-multiagente.md` | 6.1 | Safe multi-agent implementation |
| `06-02-commits.md` | 6.2 | Quality commit message generation |
| `07-01-pruebas-unitarias.md` | 7.1 | Unit test design |
| `07-02-pruebas-integracion.md` | 7.2 | Integration test design |
| `07-03-pruebas-e2e.md` | 7.3 | E2E test design |
| `07-04-pruebas-humo.md` | 7.4 | Smoke test plan |
| `07-05-automatizacion-antigravity.md` | 7.5 | Browser automation with Chrome Antigravity |
| `07-06-pruebas-performance-carga.md` | 7.6 | Performance, load and stress tests |
| `08-01-revision-estatica.md` | 8.1 | Static code review |
| `08-02-cumplimiento-requerimiento.md` | 8.2 | Requirement compliance review |
| `08-03-remediacion-maestro.md` | 8.3 | Static review remediation master prompt |
| `09-01-integracion-ramas.md` | 9.1 | Controlled branch integration |
| `09-02-monitoreo-ci.md` | 9.2 | Local and remote CI monitoring |
| `09-03-workflows-github-actions.md` | 9.3 | GitHub Actions workflows review |
| `09-04-promotion-checklist.md` | 9.4 | Environment promotion checklist (dev→staging→prod) |
| `10-01-documentacion-tecnica.md` | 10.1 | Update technical documentation |
| `10-02-memoria-tecnica.md` | 10.2 | Technical memory of the change |
| `10-03-release-changelog.md` | 10.3 | Release or changelog documentation |
| `11-01-troubleshooting.md` | 11.1 | Environment troubleshooting |
| `11-02-hardening-seguridad.md` | 11.2 | Hardening and operational security |
| `11-03-deuda-tecnica.md` | 11.3 | Technical debt and continuous improvement |
| `11-04-incident-response.md` | 11.4 | Production incident response runbook |
| `12-orquestador.md` | 12 | Full cycle orchestrator master prompt |

---

## Framework principles

- Mandatory phased work (analyze → design → execute → validate → document)
- Separation of responsibilities by agent
- Atomic and traceable commits
- CI/CD mandatory before integration
- No implementation without prior approved design
- Concurrency control in multi-agent environments
- Every deliverable distinguishes facts, findings, assumptions, risks and recommendations

## Critical rules

- git pull before working
- do not overwrite changes
- stop at conflicts
- complete traceability
