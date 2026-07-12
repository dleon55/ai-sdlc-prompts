# 9.5 — Estrategia de feature flags / kill-switch

## Descripción

Prompt para diseñar la estrategia de feature flags y kill-switch de un cambio: tipo y ciclo de vida del flag, convención de nombre y punto de evaluación, progresión de rollout por anillos con criterios de promoción, diseño del kill-switch para reversión rápida sin deploy, consistencia de sesión, fail-safe de evaluación, plan de limpieza y monitoreo específico del rollout.

**Cuándo usarlo:** cuando un cambio necesita un rollout progresivo o controlado en vez de un despliegue de una sola vez — por ejemplo, una feature de alto riesgo, un cambio significativo de UX o un cambio en un flujo crítico de negocio. Es complementario a `09-04-promotion-checklist`: ese prompt es el gate de promoción entre ambientes (DEV→QA→PROD) que decide si el código se despliega; este prompt diseña cómo se comporta y se activa gradualmente una feature una vez desplegada, dentro de un mismo ambiente o a través de varios, a lo largo de días o semanas, con independencia del propio despliegue.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — un mal diseño de estrategia de flags (por ejemplo sin kill-switch, o con un flag que no puede apagarse de forma segura) incrementa el radio de impacto de un rollout fallido, pero este prompt en sí mismo solo diseña: no activa, desactiva ni modifica flags en un ambiente real |
| Entradas requeridas | feature o cambio a flaggear, tipo de flag esperado (release/ops/experiment), plataforma de feature flags, capas donde se evalúa (cliente/servidor/edge), si hay experimento A/B asociado, fecha u hito objetivo para el rollout completo |
| Herramientas permitidas | lectura de código, arquitectura y documentación de la plataforma de flags para diseñar la estrategia — sin crear, activar, desactivar ni modificar flags en la plataforma real |
| Autonomía permitida | A1 — Proponer (diseño completo de la estrategia sin aplicar); la creación y activación de flags en la plataforma real requiere A2/A3 explícito por el equipo dueño de la feature |
| Criterios de detención | detener y escalar si el kill-switch propuesto depende del mismo pipeline de deploy que busca evitar en una emergencia; no proponer una progresión de rollout sin criterios de promoción/pausa medibles; no dejar ningún flag sin propietario ni plan de remoción |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada flag documentado con tipo, convención de nombre, punto de evaluación, anillos de rollout con % y criterio de promoción, diseño de kill-switch y plan de limpieza con fecha o disparador concreto |
| Siguiente prompt recomendado | `09-06-coordinacion-breaking-changes` si la feature flaggeada es en sí misma un breaking change que requiere coordinación con consumidores |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estrategia de feature flags y kill-switch para el rollout progresivo y seguro de este cambio.

Inputs requeridos:
- repositorio: [NOMBRE O URL]
- feature o cambio a flaggear: [REFERENCIA AL ISSUE O PR]
- tipo de flag esperado: [RELEASE / OPS / EXPERIMENT / COMBINACIÓN]
- plataforma de feature flags: [LaunchDarkly / Unleash / Flagsmith / GrowthBook / solución propia / otro]
- capas donde se evalúa: [CLIENTE / SERVIDOR / EDGE]
- hay experimento A/B asociado: [SÍ / NO]
- fecha u hito objetivo para rollout completo: [FECHA]

Pasos:

1. DEFINIR PROPÓSITO Y CICLO DE VIDA DEL FLAG
   Clasifica cada flag necesario en uno de estos tipos y justifica la elección:
   - release flag: temporal, envuelve código en desarrollo/rollout; se elimina apenas el rollout llega a 100% y se estabiliza (vida esperada: días-semanas).
   - ops flag / kill-switch: permanente, no envuelve una feature nueva sino que da control operativo para apagar una funcionalidad si falla (vida esperada: indefinida, mientras la funcionalidad exista).
   - experiment flag: temporal, ligado a un experimento A/B con hipótesis y métrica de éxito definida; se elimina cuando el experimento concluye y se declara ganador.
   Un mismo cambio puede requerir más de un flag (ej: un release flag para el rollout + un ops flag permanente de emergencia).

2. DEFINIR CONVENCIÓN DE NOMBRE Y PUNTO DE EVALUACIÓN
   - convención de nombre propuesta: [dominio]-[feature]-[tipo] (ej: checkout-new-payment-flow-release).
   - dónde se evalúa el flag: cliente (app/SPA), servidor (backend/API) o edge (CDN/gateway) — justifica según dónde vive la lógica que cambia y la latencia aceptable de propagación.
   - si se evalúa en cliente: qué pasa con clientes cacheados o desactualizados que no reciben el valor actualizado del flag.
   - propietario del flag: persona o equipo responsable de su ciclo de vida completo.

3. DISEÑAR LA PROGRESIÓN DE ROLLOUT
   Define anillos concretos con % de usuarios, público objetivo y duración mínima antes de promover al siguiente:
   - anillo 0 — interno/dogfooding: equipo interno, 0% de usuarios externos, mínimo [X] días.
   - anillo 1 — canary: [X]% de usuarios externos (segmento de bajo riesgo), mínimo [X] horas/días.
   - anillo 2 — rollout parcial: [X]% de usuarios, mínimo [X] días.
   - anillo 3 — rollout completo: 100%.
   Para cada transición entre anillos define el criterio de promoción (qué métrica y umbral deben cumplirse) y el criterio de pausa o rollback, automático o manual (ej: tasa de error > X%, latencia P95 > Yms, caída de conversión > Z%).

4. DISEÑAR EL KILL-SWITCH
   Específicamente para el escenario de emergencia, no para la progresión normal del rollout:
   - debe poder activarse sin pasar por el pipeline de deploy (toggle en el panel de la plataforma de flags o en configuración remota, nunca un cambio de código que requiera build).
   - quién tiene permiso para activarlo (define el rol, no una persona individual) y cómo queda auditado ese cambio.
   - tiempo esperado de propagación desde que se activa hasta que el 100% del tráfico deja de ver la feature.
   - qué pasa con las solicitudes ya en vuelo en el momento en que se activa.

5. DEFINIR CONSISTENCIA DE SESIÓN
   - los usuarios deben mantener el mismo estado del flag durante toda su sesión (asignación estable por user ID/session ID) o pueden ver un cambio de comportamiento a mitad de sesión — decide y justifica según el tipo de feature (un flujo de checkout requiere consistencia estricta; un banner informativo puede tolerar el cambio a mitad de sesión).
   - si hay experimento A/B asociado, cómo se garantiza el bucketing determinista de cada usuario a su variante.

6. DEFINIR EL FAIL-SAFE DE EVALUACIÓN
   - qué valor toma el flag si el servicio de flags es inalcanzable — debe caer siempre hacia el comportamiento estable/conocido, nunca activar la feature nueva por defecto.
   - timeout de evaluación y comportamiento de la caché local del cliente del flag.

7. DEFINIR EL PLAN DE LIMPIEZA
   - fecha o disparador concreto para remover el flag y el código muerto de la rama antigua (ej: "30 días después de alcanzar 100% sin incidentes").
   - responsable de crear y dar seguimiento al ticket de limpieza.
   - qué pasa si el flag nunca llega a 100% (rollback definitivo del flag vs. reclasificación explícita como flag ops permanente).

8. DEFINIR MONITOREO Y ALERTAS ESPECÍFICOS DEL ROLLOUT
   - métricas a vigilar en cada anillo (tasa de error, latencia, conversión, volumen de quejas de soporte).
   - dashboard o segmentación que permita comparar cohortes con y sin el flag activo.
   - alerta que dispare notificación automática cuando se cumpla el criterio de pausa definido en el paso 3.

Restricciones:
- el kill-switch nunca debe depender del mismo pipeline de deploy que busca evitar en una emergencia — si activarlo requiere un build o un deploy, no es un kill-switch.
- ningún flag puede quedar en el código sin un propietario explícito y un plan o fecha de remoción — un flag "para siempre" sin dueño es deuda técnica no declarada.
- la evaluación del flag debe fallar de forma segura: si el servicio de flags no responde, el sistema debe caer al comportamiento estable conocido, nunca activar silenciosamente una feature a medio probar.
- si hay un experimento A/B asociado, la estrategia de rollout no puede contaminar la asignación de variantes del experimento; el kill-switch de emergencia debe poder apagar la feature completa sin invalidar retroactivamente los datos ya recolectados (se marcan como truncados, no se descartan silenciosamente).
- este prompt diseña la estrategia; no crea, activa, desactiva ni modifica configuración de flags en ningún ambiente real — esas acciones requieren ejecución A2/A3 explícita fuera de este prompt.

Entrega:
1. Tabla de flags (nombre, tipo, punto de evaluación, propietario)
2. Progresión de rollout por anillos con criterios de promoción y pausa
3. Diseño del kill-switch (mecanismo, permisos, tiempo de propagación)
4. Definición de consistencia de sesión
5. Fail-safe de evaluación
6. Plan de limpieza con fecha o disparador concreto
7. Plan de monitoreo y alertas
```

---

## Uso con fórmula estándar

```text
Usa el prompt de estrategia de feature flags / kill-switch y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- feature a flaggear: [DESCRIPCIÓN BREVE]
- tipo de flag esperado: [RELEASE / OPS / EXPERIMENT]
- plataforma de feature flags: [LaunchDarkly / Unleash / Flagsmith / GrowthBook / otro]
- ambiente(s) donde aplica: [DEV / QA / PROD]
- documentos a revisar: arquitectura, documentación de la plataforma de flags, métricas actuales del flujo afectado
- objetivo puntual de salida: estrategia completa de flags + progresión de rollout + diseño de kill-switch + plan de limpieza
- nivel de profundidad: alto
```

---

## Salida esperada

### Estrategia de flags

| Flag | Tipo (release/ops/experiment) | Rollout (anillos/%) | Criterio de promoción | Kill-switch | Plan de limpieza |
|---|---|---|---|---|---|
| [nombre-flag] | [release / ops / experiment] | [anillo 0 → 1 → 2 → 3 con %] | [métrica y umbral por anillo] | [mecanismo, permisos, tiempo de propagación] | [fecha o disparador de remoción] |

### Ejemplo aplicado

Feature: nuevo flujo de checkout de una sola página (reemplaza el checkout multi-paso actual).

| Flag | Tipo | Rollout (anillos/%) | Criterio de promoción | Kill-switch | Plan de limpieza |
|---|---|---|---|---|---|
| `checkout-spa-release` | release | Anillo 0 interno 0% → Anillo 1 canary 5% → Anillo 2 parcial 25% → Anillo 3 completo 100% | tasa de error < 0.5%, P95 < 400ms, conversión no cae más de 2% vs. control; cada anillo mínimo 48h estable antes de promover | hereda `checkout-spa-kill` — al apagarlo, el 100% del tráfico vuelve al checkout multi-paso en < 2 min | remover flag y código del checkout multi-paso 30 días después de alcanzar 100% sin incidentes; ticket asignado a Equipo Checkout |
| `checkout-spa-kill` | ops (permanente) | N/A — global 0%/100%, sin anillos | se activa manualmente ante incidente; criterio de activación: tasa de error > 2% sostenida 5 min, o degradación de pagos confirmada | toggle directo en panel de LaunchDarkly, sin build/deploy; permiso restringido al rol `on-call-checkout`; propagación < 2 min a todos los clientes | no se elimina — vive mientras exista el flujo SPA; ownership revisado cada trimestre |
| `checkout-spa-experiment` | experiment | split 50/50 dentro del Anillo 2 (25% del tráfico total) | variante ganadora declarada con significancia estadística p < 0.05 tras mínimo 2 semanas y 10.000 sesiones por variante | hereda `checkout-spa-kill` — apagar el kill-switch detiene también el experimento y marca los datos en curso como truncados | se elimina al declarar variante ganadora y fusionar el código de esa variante como comportamiento único |
