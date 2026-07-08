# 11.8 — Auditoría de FinOps y Eficiencia de Costos Cloud

## Descripción

Prompt enfocado en operaciones financieras de ingeniería (FinOps). Se le proporciona código de infraestructura (Terraform, AWS CDK, docker-compose) o métricas de arquitectura, y detecta recursos sobre-aprovisionados, arquitecturas costosas y propone alternativas serverless, spot instances o estrategias de caché para reducir la facturación mensual.

**Cuándo usarlo:** Antes de aprovisionar nueva infraestructura, durante revisiones periódicas de costos (billing), o al evaluar arquitecturas para migraciones a la nube.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — el código IaC corregido que propone es una sugerencia de texto, no se aplica automáticamente, pero un cambio de `instance_type` o `lifecycle_rule` mal evaluado podría degradar disponibilidad si se aplica sin validar |
| Entradas requeridas | código de infraestructura (Terraform, CDK, Kubernetes manifests) o descripción de arquitectura, proveedor cloud |
| Herramientas permitidas | lectura de código IaC y arquitectura — el código corregido se entrega como texto para revisión humana, no se aplica ni se despliega |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | no recomendar Spot Instances o cambios de tier de almacenamiento para cargas de trabajo sin tolerancia a interrupciones sin señalar explícitamente ese riesgo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada recurso señalado como "desperdicio" cita el archivo/recurso IaC exacto y la estimación de ahorro asociada |
| Siguiente prompt recomendado | `09-03-workflows-github-actions` si la optimización requiere cambios en el pipeline de despliegue |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un Arquitecto de Infraestructura y Especialista en FinOps. Analiza la infraestructura proporcionada y detecta fugas de presupuesto, recursos sobre-aprovisionados y oportunidades de optimización de costos.

Entradas:
- proveedor_cloud: [AWS / GCP / Azure / On-Premise]
- codigo_o_arquitectura: [PEGA ARCHIVOS TERRAFORM, KUBERNETES MANIFESTS O DIAGRAMA TEXTUAL]

Actividades de Análisis:
1. ANÁLISIS DE EFICIENCIA: Identifica instancias EC2/VMs que podrían reemplazarse por Serverless (Lambda/CloudRun) o Contenedores auto-escalables.
2. OPTIMIZACIÓN DE ALMACENAMIENTO: Revisa las políticas de retención (S3 Lifecycle policies, EBS volumes) y sugiere tiers más económicos (ej. Glacier).
3. TRAFFIC & NETWORKING: Detecta costos ocultos por transferencia de datos (Data Transfer Out, NAT Gateways, Cross-AZ traffic) y propone mitigaciones (CDNs, VPC Endpoints).
4. ESTRATEGIA DE COMPRAS: Recomienda el uso de Instancias Spot o Reserved Instances/Savings Plans según el tipo de carga de trabajo.

Salida Obligatoria:
1. DETECCIÓN DE DESPERDICIO: Lista de recursos actualmente costosos o mal configurados.
2. ARQUITECTURA OPTIMIZADA FINOPS: Sugerencia de refactorización de infraestructura.
3. CÓDIGO CORREGIDO: Ajustes al Terraform/Manifests (ej. agregar `lifecycle_rule`, cambiar `instance_type`).
4. IMPACTO FINANCIERO: Estimación cualitativa (o cuantitativa si es posible) del ahorro mensual.

Restricciones:
- este es un análisis de solo lectura: no generes ni ejecutes comandos que terminen, redimensionen o modifiquen recursos en vivo (`terraform apply`, `aws ec2 terminate-instances`, `kubectl delete`, etc.) — el código corregido se entrega como propuesta de texto para revisión humana, nunca para aplicación directa.
- si una recomendación de ahorro reduce la disponibilidad, la redundancia o la capacidad de recuperación ante desastres (menos réplicas, eliminar un ambiente de DR, reducir la retención de backups, quitar multi-AZ), señálalo explícitamente como un trade-off de disponibilidad vs. costo — no lo presentes como una optimización sin contrapartida.
- basa cada hallazgo en datos reales de facturación o utilización cuando estén disponibles (cost explorer, billing export, métricas de uso) en vez de estimaciones genéricas; si no hay datos de billing disponibles y debes estimar, indícalo explícitamente como estimación y aclara el supuesto usado.
- no recomiendes Spot Instances ni cambios de tier de almacenamiento para cargas de trabajo sin tolerancia a interrupciones sin señalar ese riesgo de forma explícita.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría FinOps y adáptalo a:
- proveedor_cloud: [PROVEEDOR]
- codigo_o_arquitectura: [CÓDIGO IAC O DESCRIPCIÓN]
- objetivo puntual de salida: identificar desperdicio y generar IaC optimizado.
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Detección de Desperdicio | Puntos críticos que generan facturación innecesaria |
| Arquitectura Optimizada | Propuesta de rediseño orientado a la eficiencia de costos |
| Código IaC Corregido | Bloques de Terraform/Kubernetes refactorizados |
| Impacto Financiero | Proyección del ahorro derivado de las acciones |

### Ejemplo aplicado

| Sección | Ejemplo de contenido |
|---|---|
| Detección de Desperdicio | `aws_instance.worker_pool` (`infra/workers.tf:22`) mantiene 6 instancias `m5.2xlarge` fijas las 24h, con utilización promedio de CPU del 8% según CloudWatch (últimos 30 días) — candidato a autoscaling o a reemplazo por Lambda para procesamiento por lotes esporádico |
| Impacto Financiero | reemplazar `worker_pool` por un grupo de autoscaling (2-4 instancias `m5.large`) proyecta un ahorro estimado de ~$1.850/mes, calculado sobre el gasto real de los últimos 30 días en Cost Explorer para ese recurso |
