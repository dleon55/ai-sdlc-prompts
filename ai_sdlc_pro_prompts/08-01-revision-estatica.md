# 8.1 — Revisión estática de código

## Descripción

Prompt para realizar una revisión estática del código relacionado con el cambio: calidad, mantenibilidad, seguridad, complejidad, manejo de errores y consistencia con los estándares del proyecto.

**Cuándo usarlo:** después de implementar cambios, antes de abrir un PR o hacer merge.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Realiza una revisión estática del código relacionado con el cambio y evalúa calidad, mantenibilidad, seguridad y consistencia con estándares del proyecto.

Revisa:
- estructura,
- claridad,
- duplicación,
- complejidad,
- manejo de errores,
- validaciones,
- logging,
- seguridad,
- consistencia de nombres,
- alineación con arquitectura.

Entrega:
1. hallazgos críticos
2. hallazgos medios
3. observaciones menores
4. deuda técnica detectada
5. recomendaciones puntuales
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión estática y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA CON LOS CAMBIOS]
- archivos a revisar: [RUTAS DE ARCHIVOS MODIFICADOS]
- documentos a revisar: estándares de código del proyecto, arquitectura
- objetivo puntual de salida: reporte de hallazgos clasificados por criticidad
- nivel de profundidad: alto
```

---

## Salida esperada

### Hallazgos críticos

| Archivo | Línea | Descripción | Riesgo | Acción recomendada |
|---|---|---|---|---|

### Hallazgos medios

| Archivo | Línea | Descripción | Riesgo | Acción recomendada |
|---|---|---|---|---|

### Observaciones menores

| Archivo | Descripción | Sugerencia |
|---|---|---|

### Deuda técnica detectada

| Ítem | Impacto | Prioridad |
|---|---|---|
