# 16.6 — Auditoría de salud de la base de conocimiento de soporte

## Descripción

Prompt para auditar el corpus completo de la base de conocimiento (KB) de soporte como colección — no para crear un artículo puntual (`16-03-articulo-base-conocimiento`) ni para recomendar actualizar documentación como efecto colateral de un patrón de tickets (`16-05-analisis-tendencias-tickets`). Evalúa staleness (artículos desactualizados frente a versiones actuales del producto), duplicados o solapamiento, cobertura real frente a las categorías recurrentes de tickets, y artículos sin uso.

**Cuándo usarlo:** periódicamente (ej. trimestral) como mantenimiento de la KB, o cuando el equipo de soporte reporta que los artículos existentes ya no reflejan el producto actual o que cuesta encontrar la respuesta correcta.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — el prompt solo analiza y recomienda; no publica, edita ni elimina artículos por sí mismo. El riesgo indirecto es que una KB no auditada acumule artículos desactualizados que generen respuestas incorrectas a clientes si el equipo de soporte confía en ellos sin verificar |
| Entradas requeridas | inventario de artículos de la KB (título, fecha de última actualización, categoría, métricas de uso/vistas si existen), versión actual del producto o changelog reciente, categorías de tickets recurrentes (de `16-05` si existe, o el historial de tickets directamente) |
| Herramientas permitidas | lectura del inventario de la KB, changelog/release notes del producto y el historial o análisis de tendencias de tickets; no publica, edita ni elimina artículos — produce el análisis y la lista de acciones recomendadas |
| Autonomía permitida | A0 — Analizar (staleness, duplicados, cobertura, uso); A1 — Proponer (qué actualizar, fusionar, archivar o crear); nunca A2/A3 — la publicación o eliminación real de artículos requiere revisión y ejecución humana del responsable de la KB |
| Criterios de detención | detener y señalar si no hay fecha de última actualización disponible para evaluar staleness — no asumir que un artículo está vigente solo porque no hay evidencia de que esté desactualizado; si no hay métricas de uso, limitar el análisis de "sin uso" a lo que pueda inferirse de otra forma y declararlo como proxy, no como dato real de uso |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada artículo marcado como desactualizado cita el cambio de producto (changelog/release) que lo hace obsoleto; cada duplicado cita los dos o más artículos que se solapan y el grado de solape |
| Siguiente prompt recomendado | `16-03-articulo-base-conocimiento` para redactar o actualizar los artículos priorizados por esta auditoría; `16-05-analisis-tendencias-tickets` si la auditoría revela categorías de tickets recurrentes sin ningún artículo que las cubra |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Audita el corpus completo de la base de conocimiento de soporte como colección: identifica artículos desactualizados frente al producto actual, duplicados o solapados, huecos de cobertura frente a categorías de tickets recurrentes, y artículos sin uso, con una lista de acciones priorizadas.

Entradas:
- inventario de artículos de la KB: [PEGAR O ENLACE — título, fecha de última actualización, categoría, vistas/uso si existen]
- changelog o release notes recientes del producto: [PEGAR O ENLACE]
- categorías de tickets recurrentes: [PEGAR RESULTADO DE 16-05 O HISTORIAL DE TICKETS DIRECTAMENTE]
- periodo considerado para "reciente": [ej. ÚLTIMOS 6 MESES]

Pasos:
1. EVALUACIÓN DE STALENESS (desactualización)
   Para cada artículo, compara su fecha de última actualización contra el changelog/release notes del producto. Si un artículo describe un flujo, pantalla o comportamiento que cambió después de su última actualización, márcalo como desactualizado y cita el cambio específico del changelog que lo invalida. No marques un artículo como desactualizado solo por su antigüedad si el flujo que describe no ha cambiado.

2. DETECCIÓN DE DUPLICADOS Y SOLAPAMIENTO
   Identifica artículos que cubren la misma pregunta o el mismo flujo con contenido redundante (no artículos relacionados que se complementan, sino los que compiten por la misma búsqueda). Para cada par o grupo, indica el grado de solape y cuál debería ser el artículo canónico tras la fusión.

3. ANÁLISIS DE COBERTURA FRENTE A TICKETS RECURRENTES
   Cruza las categorías de tickets recurrentes provistas contra el inventario de la KB: ¿existe al menos un artículo vigente para cada categoría de alto volumen? Si una categoría recurrente no tiene ningún artículo o solo tiene uno desactualizado, señálalo como hueco de cobertura prioritario.

4. IDENTIFICACIÓN DE ARTÍCULOS SIN USO
   Si hay métricas de vistas/uso, identifica artículos con uso consistentemente bajo o nulo en el periodo. Si no hay métricas de uso disponibles, usa como proxy la ausencia de menciones o enlaces desde tickets recientes, y declara explícitamente que es un proxy, no una medición directa de uso.

5. PRIORIZACIÓN DE ACCIONES
   Para cada hallazgo, recomienda una acción: actualizar (artículo desactualizado pero la categoría sigue siendo relevante), fusionar (duplicados), crear (hueco de cobertura en categoría de alto volumen), o archivar (sin uso y sin categoría de tickets asociada). Prioriza por impacto: huecos de cobertura en categorías de alto volumen primero, luego desactualizados de alto tráfico, luego duplicados, luego archivado de baja prioridad.

Restricciones:
- no marques un artículo como desactualizado sin citar el cambio específico de producto (changelog/release) que lo invalida — la antigüedad sola no es evidencia de desactualización,
- no recomiendes archivar un artículo solo por bajo uso aparente si no hay métricas reales y el proxy usado (ausencia de menciones en tickets) es débil — decláralo como "candidato a revisar", no como "archivar directamente",
- no publiques, edites ni elimines ningún artículo — este prompt es de solo análisis y recomendación; la ejecución real la hace un humano, apoyado en `16-03` para redactar el contenido actualizado,
- si no hay fecha de última actualización para algún artículo, no lo excluyas del análisis de cobertura/duplicados, pero señala explícitamente que no puede evaluarse su staleness.

Salida:
- tabla de artículos desactualizados, con el cambio de producto que los invalida
- tabla de duplicados/solapados, con el artículo canónico recomendado
- huecos de cobertura frente a categorías de tickets recurrentes
- artículos candidatos a archivar, con la fuerza de la evidencia de "sin uso" declarada
- lista de acciones priorizada
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de la base de conocimiento y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- inventario de la KB: [ENLACE AL INVENTARIO DE ARTÍCULOS]
- changelog reciente: [ENLACE A RELEASE NOTES]
- categorías de tickets recurrentes: [RESULTADO DE 16-05 O HISTORIAL]
- periodo considerado "reciente": [ÚLTIMOS 6 MESES]
- documentos a revisar: inventario de KB, changelog, historial de tickets
- objetivo puntual de salida: lista priorizada de acciones sobre el corpus de la KB
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Artículos desactualizados | Título, cambio de producto que lo invalida |
| Duplicados/solapados | Artículos involucrados, grado de solape, canónico recomendado |
| Huecos de cobertura | Categoría de tickets sin artículo vigente que la cubra |
| Candidatos a archivar | Artículo, evidencia de "sin uso" (real o proxy declarado) |
| Acciones priorizadas | Actualizar/fusionar/crear/archivar, en orden de impacto |

### Ejemplo (fragmento)

| Artículo | Última actualización | Problema detectado |
|---|---|---|
| "Cómo restablecer tu contraseña" | Hace 14 meses | Desactualizado: el release notes de hace 6 meses muestra que el flujo de restablecimiento ahora requiere verificación por SMS, no solo email — el artículo aún describe el flujo antiguo |
| "Recuperar acceso a tu cuenta" | Hace 3 meses | Duplicado ~80% con "Cómo restablecer tu contraseña"; ambos compiten por la misma búsqueda de usuarios — se recomienda fusionar en un solo artículo canónico, usando el más reciente como base |

**Hueco de cobertura prioritario:** la categoría de tickets "errores de sincronización con la app móvil" representa el 12% de los tickets de los últimos 6 meses (según `16-05`) y no tiene ningún artículo de KB asociado — se recomienda crear un artículo nuevo antes que actualizar artículos de categorías de menor volumen.
