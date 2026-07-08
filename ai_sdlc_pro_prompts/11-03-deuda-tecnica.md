# 11.3 — Deuda técnica y mejora continua

## Descripción

Prompt para identificar la deuda técnica del repositorio y generar un backlog priorizado de mejoras clasificado por arquitectura, código, pruebas, documentación, seguridad, CI/CD, observabilidad, datos y performance.

**Cuándo usarlo:** al cierre de un sprint, en revisiones técnicas periódicas, o cuando se quiere planificar mejoras estructurales del proyecto.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — genera un inventario y backlog priorizado; no modifica código ni sistemas |
| Entradas requeridas | rama principal, componentes o módulos a analizar, acceso a código fuente, tests, configuración CI/CD, arquitectura y documentación |
| Herramientas permitidas | solo lectura del repositorio (código, tests, configuración CI/CD, documentación) |
| Autonomía permitida | A0 — Analizar: inventario y recomendaciones, sin aplicar cambios |
| Criterios de detención | si no puede acceder a un área declarada como "a analizar" (módulo inexistente o fuera del repo), debe señalar la omisión en vez de completar la matriz con supuestos |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada ítem de la matriz referencia un archivo, módulo o configuración real del repositorio, con prioridad, impacto y esfuerzo justificados |
| Siguiente prompt recomendado | `05-01-plan-implementacion` para planificar la resolución de los ítems priorizados; `11-06-gestion-parches-actualizaciones` si la deuda identificada es de dependencias desactualizadas |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Identifica deuda técnica en el repositorio y propón un backlog priorizado de mejoras.

Pasos:
1. Recorre arquitectura: identifica acoplamientos fuertes, módulos que deberían estar separados y decisiones de diseño que ya no reflejan cómo creció el sistema.
2. Recorre código: identifica duplicación, funciones o clases con complejidad alta, código muerto y violaciones de las convenciones que el propio repositorio ya establece.
3. Recorre pruebas: identifica cobertura insuficiente en módulos críticos, pruebas frágiles (flaky) y ausencia de pruebas de integración o E2E donde el riesgo del componente lo justifica.
4. Recorre documentación: identifica documentación desactualizada respecto al código actual, decisiones de arquitectura sin registrar (ADR faltantes) y README desalineados con el comportamiento real.
5. Recorre seguridad: identifica prácticas inseguras de bajo alcance que ameritan quedar en el backlog (validaciones ausentes, dependencias desactualizadas) sin sustituir una auditoría completa (`11-02-hardening-seguridad`).
6. Recorre CI/CD: identifica pipelines lentos, pasos manuales automatizables y ausencia de gates de calidad (lint, tests, cobertura mínima) antes de merge.
7. Recorre observabilidad: identifica ausencia de métricas, logs o trazas en rutas críticas, o alertas mal calibradas (demasiado ruido o silencio total ante fallos reales).
8. Recorre datos: identifica esquemas sin migraciones versionadas, ausencia de índices en consultas frecuentes o inconsistencias entre el modelo de datos y su uso real en el código.
9. Recorre performance: identifica cuellos de botella conocidos, consultas N+1, operaciones síncronas que deberían ser asíncronas o ausencia de caché en rutas de alto tráfico.
10. Para cada ítem detectado, estima impacto (costo de dejarlo sin resolver) y esfuerzo (trabajo necesario para resolverlo), y prioriza primero lo que combina alto impacto con esfuerzo bajo o medio.

Restricciones:
- cada ítem del backlog debe referenciar un archivo, módulo o configuración real del repositorio — no generalices con frases como "mejorar la arquitectura" sin evidencia concreta,
- no propongas cambios de código ni los apliques: esta es una fase de inventario y priorización, no de implementación,
- si un área declarada para análisis no es accesible (módulo inexistente o fuera del repo), señala la omisión explícitamente en vez de completar la matriz con supuestos,
- no dupliques como ítem de backlog un hallazgo que corresponde a una auditoría de seguridad completa — referencia `11-02-hardening-seguridad` si el hallazgo es de esa naturaleza.

Entrega:
- matriz de deuda técnica,
- prioridad,
- impacto,
- esfuerzo estimado,
- recomendación de atención.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de deuda técnica y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- componentes: [MÓDULOS O ÁREAS A ANALIZAR]
- documentos a revisar: código fuente, tests, CI/CD, arquitectura, docs
- objetivo puntual de salida: backlog priorizado de deuda técnica con esfuerzo estimado
- nivel de profundidad: alto
```

---

## Salida esperada

| Ítem | Categoría | Descripción | Prioridad | Impacto | Esfuerzo | Recomendación |
|---|---|---|---|---|---|---|
| Duplicación de la validación de email en 4 módulos | código | la validación de formato de email está reimplementada en `auth/register.js`, `auth/reset.js`, `admin/invite.js` y `api/webhook.js`, con reglas ligeramente distintas | alta | alto — la inconsistencia ya causó que un email válido fuera rechazado en registro (issue #310) | bajo (2-3h) | extraer a una única función utilitaria `isValidEmail()` y reemplazar los cuatro usos |
| Sin pruebas de integración para el flujo de pago | pruebas | el módulo `billing/` solo tiene pruebas unitarias con mocks del gateway; no hay prueba que verifique el flujo completo contra el sandbox del proveedor | alta | alto — un cambio en la integración podría romper pagos en producción sin que ninguna prueba lo detecte | medio (1-2 días) | agregar suite de integración contra el sandbox de pago, ejecutada en CI antes de cada release |
