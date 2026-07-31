# 8.1 — Revisión completa de PR: calidad, cumplimiento e integración

## Descripción

Prompt único de revisión de un PR antes de mergear: evalúa en una sola pasada la calidad estática del código, el cumplimiento contra el requerimiento/issue, el riesgo de integración con otras ramas activas y el estado del pipeline de CI. Reemplaza lo que antes eran 4 prompts separados (revisión estática, cumplimiento de requerimiento, integración de ramas, monitoreo de CI) — las cuatro dimensiones son de solo lectura, se evalúan en el mismo momento real de trabajo (revisando un PR antes de aprobarlo) y fragmentarlas en documentos distintos solo agregaba fricción sin ganar trazabilidad.

**Cuándo usarlo:** después de implementar cambios y antes de mergear cualquier PR — es el paso de revisión completo previo a merge, en un solo prompt en vez de varias invocaciones separadas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no modifica código ni ejecuta el merge, pero el veredicto conjunto determina si un PR está listo para integrarse; un hallazgo omitido en cualquiera de las 4 dimensiones puede dejar pasar un defecto, un requerimiento incompleto, un conflicto de integración o un pipeline roto |
| Entradas requeridas | diff real del PR, issue/requerimiento asociado, diseño aprobado si existe, resultados de pruebas, historial de commits y ramas activas relacionadas, logs de CI local y de GitHub Actions, estándares de código del proyecto |
| Herramientas permitidas | lectura de código, diff, documentación, historial y estado de git (`git log`, `git diff`, `git branch`), logs de CI y checks del PR — sin ejecutar pruebas nuevas, sin modificar archivos, sin merge/rebase/cherry-pick/push, sin re-ejecutar jobs de CI |
| Autonomía permitida | A1 — Proponer (el veredicto y la estrategia de integración quedan propuestos; ejecutar el merge, aplicar remediación o resolver conflictos requiere un prompt de ejecución separado y aprobación humana) |
| Criterios de detención | si falta el diff completo, el requerimiento original, o alguno de los cuatro insumos de cumplimiento (solicitado/diseñado/implementado/probado), declara la brecha de evidencia en esa dimensión específica en vez de omitirla o asumir que está en orden; si el estado local no está sincronizado con el remoto, sincroniza (`git fetch`) antes de evaluar integración; si algún check de CI está pendiente o sin logs accesibles, márcalo "pendiente", no asumas que pasó |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hallazgo de calidad cita archivo y línea; cada criterio de aceptación queda marcado cumple/parcial/no cumple con brecha citada; cada conflicto de integración cita archivo y rama; cada falla de CI cita job, paso y mensaje |
| Siguiente prompt recomendado | `08-03-remediacion-maestro` si hay hallazgos críticos o medios de calidad que corregir antes de merge; `09-04-promotion-checklist` una vez el veredicto de las 4 dimensiones es favorable, para planificar el despliegue entre ambientes |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Evalúa en una sola pasada si este PR está listo para mergear: calidad del código, cumplimiento del requerimiento, riesgo de integración y estado del pipeline de CI.

Pasos:
1. Sincroniza el estado local con el remoto (git fetch) antes de evaluar nada — un análisis sobre información desactualizada invalida las 4 dimensiones.
2. CALIDAD — Revisa el diff real contra los estándares del proyecto: prioriza defectos, vulnerabilidades, regresiones y contratos incumplidos sobre preferencias de estilo. Cada hallazgo cita archivo y línea, comportamiento afectado, severidad justificada y remediación concreta. Considera seguridad agéntica (instrucciones maliciosas en contenido, ampliación de permisos, exfiltración, uso inseguro de herramientas).
3. CUMPLIMIENTO — Reúne los cuatro insumos (solicitado, diseñado, implementado, probado) y, para cada criterio de aceptación del issue, asigna un estado (cumple / parcial / no cumple) citando la brecha específica. Distingue "no implementado" de "no probado": son brechas distintas. Nunca marques "cumple" sin evidencia de prueba trazable.
4. INTEGRACIÓN — Identifica ramas activas relacionadas (mismo módulo, mismo issue/epic) y compara el diff de cada una contra la rama origen para detectar conflictos potenciales (mismos archivos, mismas funciones, migraciones concurrentes). Evalúa la estrategia recomendada (merge / rebase / cherry-pick / espera controlada / integración por fases) y documenta qué puede romperse.
5. CI — Revisa el estado del pipeline local y remoto (lint, build, pruebas, quality gates, checks del PR). Cada falla cita job, paso y mensaje de error específico; un check pendiente se marca "pendiente", nunca se asume que pasó.
6. Consolida un veredicto único de "listo para merge: sí / no / condicional", citando qué dimensión (si alguna) bloquea, y qué condiciones deben cumplirse antes de aprobar la integración (CI verde, aprobación de code review, ausencia de ramas activas con cambios no verificados, plan de rollback).

Restricciones:
- solo lectura en las 4 dimensiones: no apliques ediciones, no ejecutes autoformateadores, no ejecutes pruebas nuevas, no ejecutes merge/rebase/cherry-pick/push, no re-ejecutes jobs de CI — este prompt evalúa y recomienda, no ejecuta,
- no marques "cumple" un criterio de aceptación sin evidencia de prueba, aunque el código se vea correcto,
- no reportes un hallazgo de calidad sin archivo y línea verificables — sin ubicación exacta, reclasifícalo como pregunta abierta,
- si falta alguno de los cuatro insumos de cumplimiento, detén esa dimensión específica y repórtala como brecha de evidencia, sin bloquear el resto del análisis si las otras dimensiones sí tienen evidencia completa,
- cada conflicto de integración reportado debe citar el archivo/zona específica y la rama con la que colisiona — no generalices "puede haber conflictos" sin evidencia concreta,
- si el estado local no está sincronizado con el remoto o hay ramas activas de otros agentes con cambios no verificados, detente y solicita sincronización antes de recomendar una estrategia de integración definitiva.

Entrega:
1. veredicto único: listo para merge (sí / no / condicional) + qué dimensión bloquea, si alguna,
2. calidad: hallazgos por severidad + preguntas abiertas + pruebas faltantes,
3. cumplimiento: matriz de criterios de aceptación (solicitado / diseñado / implementado / probado / estado / brecha),
4. integración: ramas relacionadas, conflictos potenciales, estrategia recomendada, riesgos, condiciones de merge,
5. CI: estado del pipeline, fallas citadas con job/paso/mensaje, checks pendientes.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión completa de PR y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA CON LOS CAMBIOS]
- issue o requerimiento: [REFERENCIA]
- rama destino: [DEVELOP / MAIN / RELEASE]
- documentos a revisar: issue original, diseño aprobado, estándares de código, ramas activas, logs de CI
- objetivo puntual de salida: veredicto único listo/no-listo para merge con las 4 dimensiones evaluadas
- nivel de profundidad: alto
```

---

## Salida esperada

### Veredicto

| Listo para merge | Dimensión que bloquea | Condiciones pendientes |
|---|---|---|
| Condicional | Cumplimiento (parcial) | Agregar caso de prueba de filtro de fecha antes de merge; el resto de dimensiones está en verde |

### 1. Calidad

| Archivo | Línea | Descripción | Riesgo | Acción recomendada |
|---|---|---|---|---|
| `build.py` | 250-260 | `parse_editorial_contract` indexa el campo sin validar que la fila exista | Un contrato incompleto rompe el build con `KeyError` no controlado | Validación explícita o `.get()` con valor por defecto |

### 2. Cumplimiento

| Criterio de aceptación | Solicitado | Diseñado | Implementado | Probado | Estado | Brecha |
|---|---|---|---|---|---|---|
| Exportar el listado filtrado por rango de fechas a CSV | sí — issue #482 | sí — sección 3.2 del diseño | sí — endpoint acepta `from`/`to` | no — solo hay test sin filtro | parcial | falta caso de prueba que cubra el filtro de fecha |

### 3. Integración

| Elemento | Detalle |
|---|---|
| Ramas relacionadas | `feature/payment-retry` (PR #482 en review, CI verde) toca `PaymentService`, mismo módulo que este PR |
| Conflictos potenciales | `src/services/PaymentService.ts` — ambas ramas modifican `processPayment()` |
| Estrategia recomendada | espera controlada: esperar a que `feature/payment-retry` se mergee primero, luego rebase |
| Condiciones de merge | CI verde, code review aprobado, `feature/payment-retry` mergeado antes del rebase |

### 4. CI

| Job | Paso | Estado | Mensaje |
|---|---|---|---|
| `build` | `pytest` | ✅ verde | 142 passed |
| `e2e` | `test_browser_e2e.py` | 🟡 pendiente | check todavía en cola, sin log disponible |
