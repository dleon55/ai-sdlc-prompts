# 4.1 — Diseño funcional y técnico de solución

## Descripción

Prompt para diseñar la solución completa antes de implementar: objetivo, alcance, supuestos, restricciones, cambios por componente, riesgos, dependencias, estrategia de validación y rollback.

**Cuándo usarlo:** una vez completado el análisis funcional, técnico y de impacto, antes de planificar o ejecutar cualquier cambio.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña una solución completa, funcional y técnica, para el requerimiento o incidente analizado.

Incluye:
1. Objetivo de la solución
2. Alcance
3. Supuestos
4. Restricciones
5. Casos de uso impactados
6. Reglas de negocio
7. Cambios requeridos por componente
8. Riesgos
9. Dependencias
10. Estrategia de validación
11. Estrategia de rollback

Formato de salida:
1. Resumen de diseño
2. Diseño funcional
3. Diseño técnico
4. Componentes afectados
5. Riesgos y mitigaciones
6. Recomendación de implementación
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de solución y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: análisis previo, arquitectura, contratos
- objetivo puntual de salida: diseño completo con riesgos y estrategia de rollback
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen de diseño | Descripción ejecutiva de la solución |
| Diseño funcional | Cambios en flujos, reglas y casos de uso |
| Diseño técnico | Componentes, contratos, cambios por módulo |
| Componentes afectados | Lista precisa con tipo de cambio |
| Riesgos y mitigaciones | Riesgos identificados con plan de mitigación |
| Recomendación | Orden y prioridad de implementación |
