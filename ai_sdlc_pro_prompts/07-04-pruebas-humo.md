# 7.4 — Pruebas de humo

## Descripción

Prompt para definir un plan de pruebas de humo que valide rápidamente que el sistema sigue operativo después de un cambio o despliegue: autenticación, flujos críticos, módulos, integraciones mínimas y errores visibles.

**Cuándo usarlo:** inmediatamente después de un despliegue o merge, para una validación rápida de salud del sistema antes de pruebas completas.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Define un plan de pruebas de humo para validar rápidamente que el sistema sigue operativo después del cambio.

Incluye:
- login/autenticación si aplica,
- flujo crítico principal,
- acceso a módulos,
- operaciones básicas,
- integraciones mínimas,
- errores visibles.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas de humo y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama o versión desplegada: [REFERENCIA]
- ambiente: [QA / STAGING / PROD]
- módulos críticos: [MÓDULOS QUE DEBEN FUNCIONAR]
- documentos a revisar: flujos críticos documentados, última versión estable
- objetivo puntual de salida: checklist de humo ejecutable en menos de 15 minutos
- nivel de profundidad: bajo
```

---

## Salida esperada

| Paso | Operación | Resultado esperado | Crítico | Estado |
|---|---|---|---|---|
| 1 | Login / autenticación | Acceso concedido | Sí | |
| 2 | Acceso al módulo principal | Carga sin error | Sí | |
| 3 | Operación básica crítica | Resultado correcto | Sí | |
| 4 | Integración mínima | Responde sin error | Sí | |
| 5 | Sin errores visibles en UI | Sin alertas críticas | Sí | |
