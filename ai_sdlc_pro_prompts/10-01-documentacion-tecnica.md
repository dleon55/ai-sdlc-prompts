# 10.1 — Actualizar documentación técnica

## Descripción

Prompt para revisar y proponer actualizaciones a la documentación técnica afectada por un cambio: README, docs, arquitectura, diagramas, contratos, casos de uso, notas de despliegue y troubleshooting.

**Cuándo usarlo:** al cierre de cada cambio, antes de hacer merge a la rama principal.

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
