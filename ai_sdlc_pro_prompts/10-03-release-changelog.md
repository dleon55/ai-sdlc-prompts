# 10.3 — Documentación de release o changelog

## Descripción

Prompt para redactar las notas de release o changelog de un cambio con enfoque técnico y funcional: resumen, módulos impactados, correcciones, mejoras, riesgos y consideraciones de despliegue.

**Cuándo usarlo:** al preparar un release o al cerrar un sprint para documentar cambios entregados.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — documento de comunicación de un release; el riesgo es reputacional/operativo si omite breaking changes o notas de despliegue, no ejecuta acciones sobre el sistema |
| Entradas requeridas | versión o tag, rama de release, issues o PRs incluidos, commits del período |
| Herramientas permitidas | solo lectura (historial de commits, PRs mergeados, issues cerrados); no publica el release ni crea el tag |
| Autonomía permitida | A1 — Proponer: entrega el changelog listo para publicar; la publicación efectiva en GitHub Releases o CHANGELOG.md es una acción A3 separada y explícita |
| Criterios de detención | si detecta cambios que rompen compatibilidad sin nota de migración clara, debe detenerse y solicitar esa información antes de dar el changelog por completo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada entrada del changelog es trazable a un commit o PR real dentro del período declarado |
| Siguiente prompt recomendado | `10-02-memoria-tecnica` si aún no existe el registro de auditoría del cambio; `09-04-promotion-checklist` para validar que el release está listo para promoción |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Redacta las notas de release o changelog del cambio con enfoque técnico y funcional.

Pasos:
1. Recopila los commits y PRs mergeados dentro del período o versión declarada, filtrando por la rama de release.
2. Clasifica cada entrada en corrección, mejora, cambio interno (sin impacto de usuario) o breaking change; descarta del changelog visible los commits puramente de mantenimiento (formateo, dependencias menores) salvo que tengan impacto de seguridad.
3. Redacta el resumen ejecutivo primero (2-4 frases), orientado a quien lee el release sin contexto técnico previo.
4. Para cada corrección o mejora, describe el impacto observable para el usuario o integrador (no solo el título técnico del commit) y enlaza el número de PR o commit.
5. Identifica los módulos impactados agrupando por área funcional, priorizando los que tocan contratos públicos (API, CLI, esquema de datos) sobre cambios puramente internos.
6. Si detectas un cambio que rompe compatibilidad, documenta la nota de migración explícita (qué debe hacer quien actualiza) antes de dar el changelog por completo; si no existe esa nota, detente y solicítala.
7. Añade consideraciones de despliegue: variables nuevas, migraciones a ejecutar y orden de despliegue si hay dependencias entre servicios.

Restricciones:
- cada entrada del changelog debe ser trazable a un commit o PR real dentro del período declarado; no incluyas cambios fuera de ese rango,
- no publiques el changelog ni crees el tag — la publicación efectiva es una acción A3 separada y explícita,
- si detectas breaking changes sin nota de migración clara, detente y solicita esa información antes de entregar el changelog como completo,
- no mezcles lenguaje de marketing con el reporte técnico: describe el impacto real, sin exagerar beneficios ni ocultar riesgos conocidos.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de release/changelog y adáptalo a:
- repositorio: [NOMBRE O URL]
- versión: [TAG O VERSIÓN]
- rama: [RAMA DE RELEASE]
- issues incluidos: [LISTA DE ISSUES O PRs]
- documentos a revisar: commits del período, PRs mergeados, issues cerrados
- objetivo puntual de salida: changelog listo para publicar en GitHub Releases o CHANGELOG.md
- nivel de profundidad: medio
```

---

## Salida esperada

### Encabezado

```
## [vX.X.X] - YYYY-MM-DD
```

### Secciones del changelog

| Sección | Contenido |
|---|---|
| Resumen | v2.3.0 introduce rate limiting por usuario en la API de pedidos para prevenir abuso, corrige el timeout intermitente en `POST /payments` y actualiza la librería de autenticación por una vulnerabilidad de severidad media |
| Correcciones (fixes) | `POST /payments` ya no expira bajo carga concurrente alta (PR #498); corregido el cálculo de impuestos con descuentos combinados (PR #495) |
| Mejoras (features) | Nuevo rate limiting configurable por usuario en `POST /orders`, 100 req/min por defecto (PR #501) |
| Módulos impactados | `orders-api`, `payments-service`, `auth-lib` (bump v3.4.1 → v3.4.2) |
| Riesgos | Usuarios con integraciones que hacen ráfagas legítimas > 100 req/min pueden recibir 429 (mitigado documentando la cabecera `Retry-After`) |
| Notas de despliegue | Configurar `RATE_LIMIT_WINDOW_MS` en producción antes del despliegue; ejecutar la migración `2026_07_08_add_rate_limit_table` antes de desplegar `orders-api` |
| Compatibilidad | Sin breaking changes en esta versión; `auth-lib` v3.4.2 es compatible hacia atrás con v3.4.x |
