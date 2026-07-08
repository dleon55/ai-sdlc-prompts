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

Revisa y actualiza:
- README,
- docs,
- arquitectura,
- diagramas,
- contratos,
- casos de uso,
- notas de despliegue,
- troubleshooting.

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
