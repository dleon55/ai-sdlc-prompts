# 0-D.2 — Stack y Arquitectura Inicial: Selección y documentación del fundamento técnico

## Descripción

Prompt para definir, justificar y documentar el **stack tecnológico inicial y las decisiones arquitectónicas fundacionales** de un proyecto nuevo. Cubre desde la selección de lenguaje y runtime hasta la topología de infraestructura, el modelo de datos y los patrones de integración.

**Cuándo usarlo:** después de aprobar el Project Charter (`00-D-01`) y antes de generar los ADRs individuales (`04-04-adr-decisiones-arquitectura.md`), la estructura del repositorio (`00-B-01`) o el plan de implementación (`05-01-plan-implementacion.md`).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Define y documenta el stack tecnológico inicial y las decisiones arquitectónicas fundacionales del proyecto, con justificación para cada elección y evaluación de alternativas descartadas.

Inputs requeridos:
- nombre del proyecto: [NOMBRE]
- descripción del dominio: [qué hace el sistema, quiénes son los usuarios, volumen aproximado]
- tipo de sistema: [API REST / GraphQL / web app SPA / mobile / data pipeline / microservicios / monolito modular / serverless / embebido / otro]
- restricciones conocidas: [presupuesto cloud, skills del equipo, tecnologías corporativas obligatorias, plazos, licencias, compliance: GDPR/HIPAA/PCI/SOC2/otro]
- stack preliminar (si lo hay): [lenguaje, framework, DB — puede ser tentativo o vacío]
- escala esperada: [usuarios concurrentes, requests/seg, volumen de datos, SLA de disponibilidad]
- plataforma de despliegue: [AWS / GCP / Azure / on-premise / Kubernetes / VPS / serverless / híbrido]
- equipo: [roles y tamaños — desarrolladores, QA, ops, AI agents]

Entrega los siguientes apartados:

1. RESUMEN EJECUTIVO DEL STACK
   Tabla completa con columnas: Capa | Tecnología elegida | Versión/tier | Estado (confirmado / tentativo) | Alternativa evaluada | Razón de elección
   Cubrir capas:
   - Lenguaje / runtime principal
   - Framework de aplicación
   - Base de datos principal (relacional / documental / column-store)
   - Base de datos secundaria o caché (Redis, Memcached, etc.)
   - Message broker / cola (si aplica: Kafka / RabbitMQ / SQS / Pub/Sub)
   - API gateway / reverse proxy
   - Autenticación y autorización (OAuth2 / OIDC / JWT / SAML)
   - Objeto storage (S3, GCS, blob)
   - Infraestructura: cómputo (VM, contenedor, serverless, bare metal)
   - Orquestador de contenedores (Docker Compose / Kubernetes / ECS / Cloud Run)
   - CI/CD pipeline
   - Registro de contenedores
   - Observabilidad: metrics (Prometheus / CloudWatch / Datadog)
   - Observabilidad: trazas distribuidas (Jaeger / Zipkin / OTEL)
   - Observabilidad: logs centralizados (Loki / ELK / CloudWatch Logs)
   - Frontend (si aplica: framework, build tool, CDN)
   - Monorepo vs. multi-repo: decisión y herramienta de gestión

2. TOPOLOGÍA DE INFRAESTRUCTURA
   - describe en texto el modelo de despliegue: zonas, redes, load balancers, edge
   - sugiere un diagrama de arquitectura en formato Mermaid (C4 nivel 2 — Container Diagram o Architecture Diagram)
   - especifica si el sistema es multi-región o single-region y por qué

3. PATRONES ARQUITECTÓNICOS SELECCIONADOS
   Para cada patrón elegido, indica: patrón | razón | cuándo aplicarlo | cuándo NO escalar a él
   Candidatos a evaluar:
   - monolito modular vs. microservicios vs. modular monolith
   - CQRS (separación de lectura/escritura)
   - Event sourcing
   - Saga pattern (para transacciones distribuidas)
   - API Gateway + BFF (Backend for Frontend)
   - Circuit breaker y retry con backoff exponencial
   - Strangler Fig (migración incremental)
   - Hexagonal / Ports & Adapters
   Selecciona sólo los que aplican al proyecto; justifica las descartadas.

4. MODELO DE DATOS INICIAL
   - entidades principales del dominio (máx. 10): nombre, descripción, relaciones clave
   - propone si el modelo es relacional, documental, híbrido o event-driven
   - estrategia de migraciones: [Alembic / Flyway / Liquibase / Rails migrations / Prisma Migrate / otro]
   - política de soft delete vs. hard delete
   - estrategia de multi-tenancy si aplica: [schema-per-tenant / row-level / database-per-tenant]

5. SEGURIDAD POR DISEÑO
   - modelo de autenticación: [tipo de token, expiración, refresh strategy]
   - modelo de autorización: [RBAC / ABAC / ACL / policy-based]
   - superficie de ataque principal y controles previstos
   - manejo de secretos: [Vault / AWS Secrets Manager / GCP Secret Manager / Azure Key Vault / .env con rotación]
   - cifrado: en tránsito (TLS mínimo) y en reposo (clave gestionada por quién)
   - compliance a cumplir: [normas aplicables y controles requeridos]

6. ESTRATEGIA DE ESCALABILIDAD Y RESILIENCIA
   - escalado horizontal vs. vertical: decisión y trigger de escalado (CPU %, RPS, latencia)
   - estrategia de caché: [niveles L1/L2, invalidación, TTL]
   - gestión de colas y backpressure
   - SLA/SLO objetivo: disponibilidad (99.9% / 99.95% / 99.99%), latencia P50/P95/P99
   - estrategia de DR (Disaster Recovery): RPO y RTO objetivo

7. DEUDA TÉCNICA Y RIESGOS ARQUITECTÓNICOS PREVISTOS
   Tabla con columnas: Decisión técnica | Deuda o riesgo generado | Cuándo revisar | Impacto si no se revisa
   (señala trade-offs conscientes: p.ej. "elegimos monolito ahora, plan de extracción a microservicios en fase 2")

8. PLAN DE EVOLUCIÓN ARQUITECTÓNICA
   - hitos donde la arquitectura deberá revisarse (por carga, features, equipo)
   - criterios para pasar de un patrón simple a uno más complejo (ejemplo: cuándo migrar de monolito a microservicios)
   - dependencias que deben resolverse antes de escalar

9. PRÓXIMOS PASOS
   Lista ordenada de acciones inmediatas:
   - ADRs a generar (usar 04-04-adr-decisiones-arquitectura.md) para cada decisión crítica
   - scaffolding del repositorio (usar 00-B-01-scaffolding-repositorio.md)
   - configuración de herramientas de calidad (usar 00-B-05-stack-calidad-codigo.md)
   - configuración de GitHub (usar 00-B-03-github-configuracion.md)
   - definición de metodología (usar 00-B-04-metodologia-framework.md)
   - gobernanza de agentes IA (usar 00-B-02-gobernanza-ia-agentes.md)

Formato de salida:
- Documento estructurado con todos los apartados anteriores
- Tablas en Markdown donde se indican
- Diagrama Mermaid para la topología (apartado 2)
- Lenguaje técnico preciso; justifica cada elección con criterios de ingeniería
- Señala con [DECISIÓN PENDIENTE: razón] cualquier punto que requiera más información o votación de equipo
- Señala con [ADR REQUERIDO] cada decisión que debe formalizarse en un Architecture Decision Record
```

---

## Notas de uso

- Este prompt produce el documento de **fundamento técnico** del proyecto. Cada decisión marcada con `[ADR REQUERIDO]` debe posteriormente documentarse con el prompt **`04-04-adr-decisiones-arquitectura.md`**.
- El diagrama Mermaid generado en el apartado 2 puede refinarse con el prompt **`04-02-diagramas-mermaid.md`**.
- La tabla de stack del apartado 1 alimenta directamente el scaffolding del repositorio (`00-B-01`) y la configuración de calidad de código (`00-B-05`).
- Para proyectos con requisitos de seguridad estrictos, complementa con **`13-04-threat-modeling.md`** antes de finalizar la arquitectura.
