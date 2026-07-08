# 10.1 — Actualizar documentación técnica

## Descripción

Prompt para revisar y proponer actualizaciones a la documentación técnica afectada por un cambio: README, docs, arquitectura, diagramas, contratos, casos de uso, notas de despliegue y troubleshooting.

**Cuándo usarlo:** al cierre de cada cambio, antes de hacer merge a la rama principal.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — propone contenido de documentación, no modifica código ni sistemas en ejecución; el riesgo real es que la documentación quede desactualizada o induzca a error si no se revisa |
| Entradas requeridas | issue o requerimiento de referencia, rama integrada, componentes modificados, documentos existentes a revisar (README, docs/, arquitectura, contratos API) |
| Herramientas permitidas | solo lectura del repositorio (código y documentación existente); no aplica cambios directamente sobre los documentos, solo entrega contenido propuesto |
| Autonomía permitida | A1 — Proponer: entrega lista de documentos a actualizar con contenido propuesto, sin aplicar el cambio |
| Criterios de detención | si el cambio real o los componentes modificados no están claros, debe solicitar esa información antes de proponer contenido inventado |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada documento propuesto referencia una ruta real existente en el repositorio y una razón de cambio ligada al issue o rama declarados |
| Siguiente prompt recomendado | `10-02-memoria-tecnica` para consolidar el registro de auditoría del cambio; `10-03-release-changelog` si el cambio se agrupa en un release |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actualiza o propone actualización de la documentación técnica afectada por el cambio.

Pasos:
1. Identifica los documentos existentes en el repositorio relacionados con los componentes modificados: README, docs/, diagramas de arquitectura, contratos de API, casos de uso, notas de despliegue y troubleshooting.
2. Para cada documento, determina si el cambio lo vuelve desactualizado (contenido que ya no es cierto), incompleto (falta cubrir el nuevo comportamiento) o si requiere un documento nuevo que hoy no existe.
3. Prioriza: actualiza primero README y contratos de API (afectan a quien integra o usa el sistema) antes que notas internas de troubleshooting o diagramas secundarios.
4. Redacta el contenido propuesto en el mismo formato y nivel de detalle del documento original, citando la sección exacta a modificar (encabezado o línea de referencia) en vez de reescribir el archivo completo.
5. Si el cambio introduce un paso de despliegue nuevo (variable de entorno, migración, feature flag), añade una nota de despliegue explícita aunque no exista una sección previa para ello.
6. Señala cualquier documento que quede inconsistente con el código pero que no puedas actualizar por falta de información, en vez de inventar contenido.

Restricciones:
- no apliques los cambios directamente sobre los archivos, solo entrega el contenido propuesto,
- no inventes rutas de documentos que no existen en el repositorio; si el documento no existe pero debería, indícalo explícitamente como "documento nuevo a crear",
- si el cambio real o los componentes modificados no están claros, detente y solicita esa información antes de proponer contenido inventado,
- cada documento propuesto debe referenciar una ruta real existente en el repositorio (o marcarse como nuevo) y una razón de cambio ligada al issue o rama declarados.

Entrega:
- documentos a actualizar,
- contenido propuesto,
- razón del cambio.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de actualización de documentación técnica y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA INTEGRADA]
- componentes: [COMPONENTES MODIFICADOS]
- documentos a revisar: README, docs/, arquitectura, contratos API
- objetivo puntual de salida: lista de documentos a actualizar con contenido propuesto
- nivel de profundidad: medio
```

---

## Salida esperada

| Documento | Ruta | Razón del cambio | Contenido propuesto |
|---|---|---|---|
| README — sección "Configuración" | `README.md` | Se agregó la variable de entorno `RATE_LIMIT_WINDOW_MS` requerida por el nuevo limitador de tasa (issue #482) | Añadir fila a la tabla de variables de entorno: `RATE_LIMIT_WINDOW_MS` — ventana en ms para el rate limiting, default `60000` |
| Contrato de API — endpoint POST /orders | `docs/api/orders.md` | El endpoint ahora responde 429 cuando se excede el límite de tasa (issue #482) | Añadir código de respuesta `429 Too Many Requests` con ejemplo de payload de error y cabecera `Retry-After` |
| Notas de despliegue | `docs/deployment.md` | Nueva variable de entorno obligatoria en producción antes del despliegue (issue #482) | Añadir paso "3. Configurar `RATE_LIMIT_WINDOW_MS` en el ambiente; sin ella el servicio usa el default de 60s" |
