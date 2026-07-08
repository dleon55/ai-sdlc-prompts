# 11.8 — FinOps Audit and Cloud Cost Efficiency

## Description

Prompt focused on engineering financial operations (FinOps). It takes infrastructure code (Terraform, AWS CDK, docker-compose) or architecture metrics, detects over-provisioned resources and expensive architectures, and proposes serverless alternatives, spot instances, or caching strategies to reduce monthly billing.

**When to use it:** Before provisioning new infrastructure, during periodic billing reviews, or when evaluating architectures for cloud migrations.

---

## Editorial Contract

| Field | Value |
|---|---|
| Type | analysis |
| Expected risk | medium — the corrected IaC code it proposes is a text suggestion, not auto-applied, but a poorly evaluated `instance_type` or `lifecycle_rule` change could degrade availability if applied without validation |
| Required inputs | infrastructure code (Terraform, CDK, Kubernetes manifests) or architecture description, cloud provider |
| Allowed tools | reading IaC code and architecture — the corrected code is delivered as text for human review, not applied or deployed |
| Permitted autonomy | A1 — Propose |
| Stop criteria | do not recommend Spot Instances or storage-tier changes for interruption-intolerant workloads without explicitly flagging that risk |
| Expected output | see `## Expected output` |
| Minimum evidence | each resource flagged as "waste" cites the exact IaC file/resource and its associated savings estimate |
| Recommended next prompt | `09-03-workflows-github-actions` if the optimization requires changes to the deployment pipeline |

---

## Mandatory previous context

> Include the block from the `00-framework.md` file before this prompt.

---

## Complete prompt

```text
Objective:
Act as an Infrastructure Architect and FinOps Specialist. Analyze the provided infrastructure and detect budget leaks, over-provisioned resources, and cost optimization opportunities.

Inputs:
- cloud_provider: [AWS / GCP / Azure / On-Premise]
- code_or_architecture: [PASTE TERRAFORM FILES, KUBERNETES MANIFESTS OR TEXTUAL DIAGRAM]

Analysis Activities:
1. EFFICIENCY ANALYSIS: Identify EC2/VM instances that could be replaced by Serverless (Lambda/CloudRun) or auto-scaling Containers.
2. STORAGE OPTIMIZATION: Review retention policies (S3 Lifecycle policies, EBS volumes) and suggest more economical tiers (e.g., Glacier).
3. TRAFFIC & NETWORKING: Detect hidden costs due to data transfer (Data Transfer Out, NAT Gateways, Cross-AZ traffic) and propose mitigations (CDNs, VPC Endpoints).
4. PURCHASING STRATEGY: Recommend the use of Spot Instances or Reserved Instances/Savings Plans based on the workload type.

Mandatory Output:
1. WASTE DETECTION: List of currently expensive or misconfigured resources.
2. FINOPS OPTIMIZED ARCHITECTURE: Suggestion for infrastructure refactoring.
3. CORRECTED CODE: Adjustments to Terraform/Manifests (e.g., adding `lifecycle_rule`, changing `instance_type`).
4. FINANCIAL IMPACT: Qualitative (or quantitative if possible) estimation of monthly savings.
```

---

## Use with standard formula

```text
Use the FinOps audit prompt and adapt it to:
- cloud_provider: [PROVIDER]
- code_or_architecture: [IAC CODE OR DESCRIPTION]
- specific output objective: identify waste and generate optimized IaC.
- depth level: high
```

---

## Expected output

| Section | Expected content |
|---|---|
| Waste Detection | Critical points generating unnecessary billing |
| Optimized Architecture | Redesign proposal aimed at cost efficiency |
| Corrected IaC Code | Refactored Terraform/Kubernetes blocks |
| Financial Impact | Projection of savings derived from the actions |
