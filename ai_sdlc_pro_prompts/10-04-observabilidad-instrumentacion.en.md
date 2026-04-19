# 10.4 — Observability: Instrumentation and Monitoring

## Description

Prompt to design and implement an application observability strategy: metrics, structured logs, and distributed traces pillars; alerts, dashboards, SLOs/SLAs, and signal correlation to detect and diagnose production problems.

**When to use:** when adding observability to a new system, when reviewing monitoring coverage before a major deployment, or when blind spots in production failure detection are identified.

---

## Required prior context

> Include the block from `00-framework.md` before this prompt.
> If a result from `13-04` (Threat Modeling) exists, attach it to identify critical components requiring greater observability coverage.

---

## Full prompt

```text
Objective:
Design and implement a complete observability strategy for the application,
covering the three pillars (metrics, logs, traces), defining SLOs, actionable alerts,
and dashboards to detect and diagnose problems before they impact users.

Steps:

1. INVENTORY OF COMPONENTS TO INSTRUMENT
   Map all system components requiring observability:
   - backend services and APIs (names, language, framework)
   - databases and caches (type, engine, how they are accessed)
   - message queues or async workers
   - external and third-party services (with their own SLA)
   - infrastructure: containers, nodes, load balancers
   - frontend (if applicable): Core Web Vitals, JS errors, real user experience

2. PILLAR 1 — METRICS
   For each service, define RED + USE metrics:
   
   RED (for request-oriented services):
   - Rate: requests per second (req/s)
   - Errors: error rate (% of 4xx/5xx responses)
   - Duration: latency distribution (P50, P95, P99)
   
   USE (for infrastructure resources):
   - Utilization: % CPU, memory, disk, network connections
   - Saturation: queue sizes, wait time
   - Errors: system errors, hardware failures
   
   Business metrics (domain Golden Signals):
   - metrics reflecting business health: orders processed/min, active users, conversions
   - metrics that alert before the user notices: retry rate, validation errors
   
   For each metric, specify:
   - name and unit (e.g., `http_request_duration_seconds`, `gauge` / `counter` / `histogram`)
   - labels/dimensions for segmentation (endpoint, method, status_code, region)
   - instrumentation instruction: code or configuration required to expose it

3. PILLAR 2 — STRUCTURED LOGS
   Define the logging strategy:
   
   a) Format and structure:
      - use structured JSON (not plain text) — enables efficient searching and filtering
      - mandatory fields in every log: timestamp (ISO 8601), level, service, trace_id, span_id, message
      - contextual fields: request_id, user_id (anonymized if GDPR applies), endpoint, duration_ms
   
   b) Log levels and when to use them:
      - ERROR: failure requiring immediate attention
      - WARN: recoverable anomalous condition that may escalate
      - INFO: relevant business events (request completed, job executed)
      - DEBUG: diagnostic detail (only enabled in non-prod environments)
   
   c) What NOT to log (security and privacy):
      - passwords, tokens, API keys, card numbers
      - PII without anonymization (full names, emails, user IPs under GDPR)
      - full stack traces in client responses (internal logs only)
   
   d) Retention and costs:
      - define retention period by level: ERROR 90d, INFO 30d, DEBUG 7d
      - configure sampling for high-volume logs (e.g., 10% of successful requests)

4. PILLAR 3 — DISTRIBUTED TRACES
   If the system has more than one service or component:
   
   a) Context propagation:
      - implement W3C Trace Context (`traceparent` header) between services
      - propagate trace_id and span_id in all HTTP calls, queue messages, jobs
   
   b) Instrumented spans:
      - span per business operation (endpoint, DB query, external service call)
      - attributes in each span: operation name, status, duration, error (if applicable)
      - sampling: 100% of traces with errors, 10% of successful traces (adjust by volume)
   
   c) Correlation:
      - ensure trace_id appears in logs and metrics for cross-signal correlation
      - configure the observability stack to navigate: alert → trace → logs

5. SLO AND ALERT DEFINITION
   
   a) SLOs (Service Level Objectives):
      For each critical service, define:
      - SLI (indicator): e.g., "% of requests with P95 latency < 500ms"
      - SLO target: e.g., 99.5% over a 30-day window
      - Error budget: (100% - SLO)% — how much failure margin exists
      - Burn rate: how fast the error budget is being consumed
   
   b) Actionable alerts (avoid alert fatigue):
      For each alert, define:
      - trigger condition with precise threshold
      - severity: page (overnight) / ticket (business hours) / info (log only)
      - evaluation window and cooldown period
      - attached playbook: what to do when it fires (link to runbook 11-04)
      - recipient: team, Slack channel, PagerDuty, OpsGenie
      
      Minimum recommended alerts:
      - error rate > 1% over 5 min → page
      - P99 latency > threshold × 2 over 5 min → page
      - CPU or memory > 85% sustained for 10 min → ticket
      - error budget < 10% remaining → ticket
      - external service with > 5% errors → ticket

6. DASHBOARDS
   Design the structure of operational dashboards:
   
   a) System health dashboard (overview):
      - global and per-service error rate
      - P95 and P99 latency per service
      - throughput (req/s) per service
      - SLO status (% compliance, remaining error budget)
      - active incidents
   
   b) Per-service dashboard (drill-down):
      - service RED metrics
      - latency distribution by endpoint
      - top 10 endpoints by error
      - slow or error traces
      - related logs (direct integration from dashboard)
   
   c) Infrastructure dashboard:
      - CPU, memory, disk per node/container
      - active DB connections, pool usage
      - message queue sizes

7. RECOMMENDED OBSERVABILITY STACK
   Propose the stack based on project infrastructure:
   
   Cloud-native option:
   - Metrics: Prometheus + Grafana / CloudWatch / Datadog
   - Logs: Loki + Grafana / CloudWatch Logs / Datadog Logs
   - Traces: Tempo + Grafana / X-Ray / Datadog APM
   - Alerts: Alertmanager / CloudWatch Alarms / PagerDuty
   
   Self-hosted OSS option:
   - Prometheus (metrics) + Loki (logs) + Tempo (traces) + Grafana (visualization)
   - OpenTelemetry Collector as universal export agent
   
   For each selected stack component, provide:
   - installation or basic configuration instructions
   - export configuration from the application (SDK, agent, sidecar)

Deliverables:
- instrumentation map per component (metrics, logs, traces defined),
- SLO catalog with SLI, target, and error budget,
- alert catalog with condition, severity, and playbook,
- recommended dashboard structure,
- proposed observability stack with initial configuration.
```

---

## Standard formula usage

```text
Use the observability and instrumentation prompt and adapt it to:
- repository: [NAME OR URL]
- technology stack: [language, framework, database, messaging]
- infrastructure: [cloud provider / on-premise / containers / serverless]
- current observability stack: [none / Prometheus+Grafana / Datadog / CloudWatch / other]
- number of services: [monolith / N microservices]
- SLAs committed to customers: [response time, availability]
- target environment: [production / staging / both]
- documents to review: system architecture, existing runbooks, threat model 13-04
- specific output goal: SLO catalog + alerts + dashboard structure
- depth level: high
```

---

## Expected output

### SLO catalog

| Service | SLI | SLO | Window | Error budget |
|---|---|---|---|---|
| API Gateway | % requests with P95 < 500ms | 99.5% | 30 days | 0.5% ≈ 3.6 h/month |
| Auth Service | % successful logins / valid attempts | 99.9% | 30 days | 0.1% ≈ 44 min/month |
| Payment worker | % jobs processed without error | 99.95% | 30 days | 0.05% ≈ 22 min/month |

### Alert catalog

| Alert | Condition | Severity | Playbook | Recipient |
|---|---|---|---|---|
| High error rate | error rate > 1% for 5 min | Page | Runbook 11-04 § Error rate | #oncall + PagerDuty |
| High latency | P99 > 1s for 5 min | Page | Runbook 11-04 § Latency | #oncall |
| Error budget < 10% | burn rate > 14.4× over 1h | Ticket | See SLO dashboard | #tech-lead |
| DB pool exhaustion | active connections > 90% of pool | Ticket | Runbook 11-04 § DB | #backend |
