# 10.2 — Memoria técnica del cambio

## Descripción

Prompt para generar una memoria técnica clara y ejecutiva del cambio realizado: contexto, problema, análisis, solución implementada, pruebas, riesgos, resultados y puntos pendientes.

**Cuándo usarlo:** al cierre de cada issue o sprint, como registro formal del trabajo realizado para auditoría y referencia futura.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — genera un documento de registro/auditoría; no ejecuta acciones sobre el sistema, pero al ser insumo de auditoría formal, imprecisiones afectan la trazabilidad del cambio |
| Entradas requeridas | issue o requerimiento, rama integrada, ambiente, componentes modificados, commits/PRs, diseño aprobado, resultados de pruebas ejecutadas |
| Herramientas permitidas | solo lectura (commits, PRs, diseño aprobado, resultados de pruebas); no ejecuta comandos ni modifica el repositorio |
| Autonomía permitida | A1 — Proponer: redacta el documento de memoria técnica; no lo publica ni archiva por sí mismo |
| Criterios de detención | si faltan resultados de pruebas o el diseño aprobado no está disponible, debe señalarlo explícitamente en la sección correspondiente en vez de inventar resultados |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada sección (causa raíz, pruebas ejecutadas, riesgos) debe estar respaldada por una referencia verificable (commit, PR o resultado de test), no ser genérica |
| Siguiente prompt recomendado | `10-03-release-changelog` si el cambio se agrupa en un release; `11-03-deuda-tecnica` para registrar los puntos pendientes como deuda técnica formal |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera una memoria técnica clara y ejecutiva del cambio realizado.

Pasos:
1. Contexto: resume en 2-3 frases el estado previo del sistema y por qué se necesitó el cambio, citando el issue o requerimiento de origen.
2. Problema o requerimiento: describe el problema concreto o la necesidad de negocio sin mezclarlo con la solución adoptada.
3. Análisis: documenta las alternativas consideradas y por qué se descartaron, referenciando el diseño aprobado si existe.
4. Causa raíz (si aplica): si el cambio es una corrección, identifica la causa raíz confirmada y distíngala de síntomas o causas hipotéticas descartadas durante el análisis.
5. Solución implementada: describe exactamente qué se implementó en términos verificables — no "se mejoró el sistema", sino qué lógica, endpoint o configuración cambió.
6. Componentes modificados: lista archivos, módulos o servicios afectados, con referencia a los commits o PRs correspondientes.
7. Pruebas ejecutadas: para cada tipo de prueba relevante (unitaria, integración, E2E, performance) indica si se ejecutó, el resultado y la referencia al artefacto (pipeline run, reporte). Si algún tipo relevante no se ejecutó, decláralo explícitamente en vez de omitirlo.
8. Riesgos: riesgos residuales que persisten después del cambio, priorizados por severidad, indicando si tienen plan de mitigación o quedan aceptados sin mitigar.
9. Resultados: estado final observable del sistema tras el despliegue (métricas, comportamiento validado en producción o staging), no solo la intención del cambio.
10. Puntos pendientes: tareas derivadas, deuda técnica nueva o seguimientos necesarios, cada uno con dueño sugerido cuando sea posible.

Restricciones:
- cada sección debe estar respaldada por una referencia verificable (commit, PR, resultado de test o pipeline run), no redactada de forma genérica,
- si faltan resultados de pruebas o el diseño aprobado no está disponible, señálalo explícitamente en la sección correspondiente en vez de inventar resultados,
- no mezcles el problema con la solución en las secciones de contexto y problema — cada una responde una pregunta distinta,
- distingue explícitamente entre riesgos mitigados y riesgos aceptados que quedan pendientes de resolución.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de memoria técnica y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA INTEGRADA]
- ambiente: [PROD / STAGING]
- componentes: [COMPONENTES MODIFICADOS]
- documentos a revisar: commits, PRs, diseño aprobado, resultados de pruebas
- objetivo puntual de salida: memoria técnica completa para auditoría
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido |
|---|---|
| Contexto | El servicio de pedidos (`orders-api`) venía recibiendo picos de tráfico automatizado desde mediados de junio que degradaban la latencia P95 de todos los endpoints (issue #482) |
| Problema / Requerimiento | Evitar que un cliente pueda saturar `POST /orders` sin bloquear tráfico legítimo, cumpliendo un SLA de P95 < 300ms |
| Análisis | Se evaluó rate limiting a nivel de gateway (Kong) vs. en aplicación; se eligió aplicación por permitir límites por usuario autenticado, no solo por IP |
| Causa raíz | Ausencia de control de tasa por usuario en `POST /orders`; el gateway solo limitaba por IP, insuficiente contra bots rotando IPs |
| Solución implementada | Middleware `rateLimiter` en `src/middleware/rateLimiter.ts`, límite de 100 req/min por `userId`, ventana configurable vía `RATE_LIMIT_WINDOW_MS` |
| Componentes modificados | `src/middleware/rateLimiter.ts`, `src/routes/orders.ts`, `docs/api/orders.md` (PR #501) |
| Pruebas ejecutadas | Unitarias: 12/12 verdes (PR #501, CI run #3892). Carga: k6 confirmó P95 280ms con 300 req/s sostenidos. E2E de checkout: no re-ejecutado, pendiente |
| Riesgos | Aceptado: usuarios con múltiples pestañas activas pueden alcanzar el límite; mitigado con mensaje de error claro y cabecera `Retry-After` |
| Resultados | Latencia P95 de `POST /orders` estable en producción tras 48h de monitoreo; 0 incidentes de saturación reportados |
| Puntos pendientes | Re-ejecutar la suite E2E de checkout con el middleware activo (ticket #503, sin dueño asignado aún) |
