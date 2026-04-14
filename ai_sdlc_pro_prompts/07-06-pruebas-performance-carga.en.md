# 7.6 — Performance and load tests

## Description

Prompt to design a performance, load, stress and benchmark test strategy for the components impacted by a change: scenarios, acceptance thresholds, tools, test data and failure criteria.

**When to use it:** before deploying to production changes that affect APIs, database queries, batch processes, file generation or any component with performance requirements. Also as periodic system health review.

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Design the performance and load test strategy for the components affected by this change.

Required inputs:
- components to test: [LIST]
- test environment: [QA / STAGING — never PROD for load tests]
- concurrent users expected in production: [NUMBER]
- SLA or acceptable response time: [ex: P95 < 500ms, P99 < 1s]
- available tool: [k6 / Locust / JMeter / Artillery / hey / wrk / other]

Deliver:

1. TEST TYPES TO EXECUTE
   For each type, indicate objective, duration, load and failure criterion:
   a) Load test — normal expected load in production
   b) Stress test — load exceeding maximum expected (1.5x - 2x)
   c) Spike test — sudden traffic spike (10x for 30s)
   d) Soak test — sustained load over long period (detects memory leaks)
   e) Benchmark — measure baseline before and after change

2. TEST SCENARIOS
   For each critical endpoint/operation:
   - scenario name
   - path / operation
   - HTTP method or operation type
   - test payload (no real data — use synthetic data)
   - concurrent users
   - duration
   - acceptance threshold: response time P50, P95, P99
   - acceptance threshold: maximum allowed error rate (ex: < 0.1%)
   - acceptance threshold: minimum throughput (req/s)

3. TEST DATA
   - how to generate synthetic data for the test
   - volume of data in DB necessary for results to be representative
   - post-test cleanup

4. BASE SCRIPT (according to chosen tool)
   Generate the base test script ready to execute and adapt.

5. FAILURE THRESHOLDS (fail criteria)
   List the criteria that make the test fail automatically:
   - response time P95 > [X]ms
   - error rate > [Y]%
   - throughput < [Z] req/s

6. RESULTS INTERPRETATION
   - which metrics to review first
   - how to detect bottlenecks (CPU, memory, DB, network, locks)
   - what to investigate if P99 > P95 * 3 (abnormal distribution)

7. BEFORE / AFTER COMPARISON
   Table to record pre and post change metrics:
   | Scenario | P50 before | P95 before | P99 before | P50 after | P95 after | P99 after | Delta |
```

---

## Use with standard formula

```text
Use the performance and load tests prompt and adapt it to:
- repository: [NAME OR URL]
- issue or requirement: [REFERENCE]
- components to test: [LIST]
- environment: [QA / STAGING]
- target SLA: [ACCEPTABLE RESPONSE TIMES]
- expected concurrent users: [NUMBER]
- tool: [k6 / Locust / JMeter / Artillery]
- documents to review: architecture, API contracts, performance requirements
- specific output objective: complete strategy + base script + thresholds table
- depth level: high
```

---

## Expected output

### Test scenarios

| Scenario | Path | Concurrent | Duration | Max P95 | Max error | Type |
|---|---|---|---|---|---|---|
| List prompts | GET /api/prompts | 100 | 5m | 300ms | 0.1% | Load |
| Filter by category | GET /api/prompts?cat=07 | 100 | 5m | 300ms | 0.1% | Load |
| General stress | GET /* | 300 | 3m | 800ms | 1% | Stress |
| Homepage spike | GET / | 1000 | 30s | 1500ms | 2% | Spike |
| API soak | GET /api/prompts | 50 | 60m | 400ms | 0.1% | Soak |

### Base k6 script

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 },   // ramp-up
    { duration: '3m', target: 100 },   // sustained load
    { duration: '1m', target: 0 },     // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],   // P95 < 300ms
    http_req_failed: ['rate<0.001'],    // < 0.1% errors
  },
};

export default function () {
  const res = http.get('[BASE_URL]/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

### Before/after comparison

| Scenario | P50 before | P95 before | P99 before | P50 after | P95 after | P99 after | Δ P95 |
|---|---|---|---|---|---|---|---|
