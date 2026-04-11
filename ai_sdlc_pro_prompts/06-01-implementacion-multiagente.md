# 6.1 — Implementación multi-agente segura

## Descripción

Prompt de ejecución controlada para implementar la solución aprobada en un entorno donde múltiples agentes pueden estar modificando el repositorio en paralelo. Prioriza cambios mínimos, commits atómicos y detección de conflictos.

**Cuándo usarlo:** durante la fase de ejecución, después de que el plan (`05-01`) y los riesgos (`05-02`) han sido aprobados.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Modo: ejecución controlada

Objetivo:
Implementa la solución aprobada respetando un entorno multi-agente con cambios concurrentes.

Reglas:
1. Revisa cambios recientes antes de editar.
2. Trabaja con cambios mínimos y controlados.
3. No modifiques archivos fuera del alcance.
4. Haz commits atómicos por unidad lógica.
5. Si detectas cambios ajenos en la misma zona, detén y documenta.

Actividades:
1. Identificar archivos a modificar
2. Aplicar cambios por componente
3. Mantener compatibilidad con contratos y flujos existentes
4. Actualizar pruebas y documentación relacionadas
5. Preparar propuesta de commit

Entrega:
- archivos modificados,
- resumen de cambio por archivo,
- riesgos residuales,
- mensaje de commit sugerido.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de implementación multi-agente y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE TRABAJO]
- ambiente: [DEV / QA]
- componentes: [ARCHIVOS Y MÓDULOS A MODIFICAR]
- documentos a revisar: plan de implementación aprobado, diseño técnico
- objetivo puntual de salida: cambios aplicados con commits atómicos y sin conflictos
- nivel de profundidad: alto
```

---

## Salida esperada

| Archivo | Cambio aplicado | Riesgo residual | Commit sugerido |
|---|---|---|---|
