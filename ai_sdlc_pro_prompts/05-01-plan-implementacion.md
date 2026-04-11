# 5.1 — Plan de implementación detallado

## Descripción

Prompt para elaborar un plan de implementación ejecutable y trazable: actividades previas, cambios por componente, migraciones, pruebas, despliegue, rollback y evidencias esperadas por paso.

**Cuándo usarlo:** después del diseño aprobado (`04-01`), antes de ejecutar cualquier cambio en el repositorio.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Elabora un plan de implementación detallado, ejecutable y trazable para la solución propuesta.

Incluye:
1. actividades previas,
2. cambios por componente,
3. ajustes de datos o migraciones,
4. pruebas requeridas,
5. validaciones en ambiente,
6. integración con ramas,
7. despliegue,
8. rollback,
9. evidencias esperadas.

Formato:
| Paso | Actividad | Componente | Dependencia | Riesgo | Evidencia esperada |
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan de implementación y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES A MODIFICAR]
- documentos a revisar: diseño aprobado, arquitectura, contratos
- objetivo puntual de salida: plan de implementación ejecutable paso a paso
- nivel de profundidad: alto
```

---

## Salida esperada

| Paso | Actividad | Componente | Dependencia | Riesgo | Evidencia esperada |
|---|---|---|---|---|---|
