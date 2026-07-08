# 14.3 — Auditoría de cumplimiento de procesos ISO 29110 / MOPROSOFT

## Descripción

Prompt estructurado de aseguramiento de calidad (QA / Audit) para certificar que los entregables funcionales, de diseño y técnicos del ciclo de desarrollo cumplen rigurosamente con los requerimientos de los perfiles básicos de ISO/IEC 29110 y el modelo de procesos MOPROSOFT.

**Cuándo usarlo:** antes del despliegue en entornos controlados (Staging / Prod), como parte de las puertas de calidad (Quality Gates) en la liberación.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | validación |
| Riesgo esperado | medio — es una auditoría de solo lectura, pero un veredicto de "Aprobado" indebido puede autorizar la liberación de un entregable no conforme a producción |
| Entradas requeridas | workspace/subproyecto y estándar de compliance a auditar (ISO 29110 / MOPROSOFT / MAAGTICSI), artefactos generados (Plan de Implementación, Casos de Prueba, Código de Pruebas, Memoria Técnica) |
| Herramientas permitidas | lectura de artefactos, código y documentación del proyecto — sin ejecución de pruebas ni cambios en el repositorio |
| Autonomía permitida | A0 — Analizar la conformidad de cada artefacto; A1 — Proponer el veredicto y las acciones de remediación obligatorias |
| Criterios de detención | no emitir veredicto "Aprobado" si falta trazabilidad bidireccional requerimiento-diseño-código-pruebas; marcar como "Rechazado" o "Aprobado con Reservas" ante cualquier no conformidad sin evidencia de mitigación |
| Salida esperada | ver `Salida:` dentro de `## Prompt completo` |
| Evidencia mínima | cada no conformidad reportada referencia el artefacto o control específico incumplido y la acción de remediación obligatoria asociada |
| Siguiente prompt recomendado | `08-03-remediacion-maestro` si el veredicto es "Rechazado" o "Aprobado con Reservas"; `09-04-promotion-checklist` si el veredicto es "Aprobado" para continuar con la promoción del cambio |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Audita el entregable actual de ingeniería de software para verificar su conformidad con las prácticas exigidas por los estándares ISO 29110 (Perfil Básico) y MOPROSOFT.

Entradas:
- workspace/subproyecto: [WORKSPACE/SUBPROYECTO]
- artefactos generados (Plan de Implementación, Casos de Prueba, Código de Pruebas, Memoria Técnica): [LEER O PEGAR DETALLES]
- estándar/compliance: [ISO 29110 / MOPROSOFT / MAAGTICSI]

Actividades:
1. Revisa los artefactos contra el checklist básico de calidad:
   - ¿El requerimiento está mapeado a un diseño técnico formal (ADR/Casos de Uso)?
   - ¿Se diseñaron e implementaron pruebas de verificación y validación (Unitarias, Integración, Humo)?
   - ¿Existe trazabilidad bidireccional entre requerimiento, diseño, código y pruebas?
   - ¿Se registró la memoria técnica del cambio y se actualizó la documentación de usuario/operación?
2. Identifica no conformidades y desviaciones.
3. Evalúa si el código cumple con las directrices de seguridad de la información del proyecto (ISO 27001).

Restricciones:
- no emitas veredicto "Aprobado" si falta trazabilidad bidireccional completa entre requerimiento, diseño, código y pruebas,
- ante cualquier no conformidad detectada sin evidencia de mitigación, marca el veredicto como "Rechazado" o "Aprobado con Reservas" — nunca "Aprobado" por omisión o duda,
- no ejecutes pruebas ni modifiques el repositorio — la auditoría es exclusivamente de lectura sobre artefactos y documentación existentes,
- cada no conformidad reportada debe referenciar el artefacto o control específico incumplido junto con la acción de remediación obligatoria asociada.

Salida:
1. Reporte de Cumplimiento Normativo (Checklist Aprobado/Faltante)
2. Matriz de Trazabilidad de Requerimiento a Pruebas
3. Listado de No Conformidades Detectadas (Acción de Remediación Obligatoria)
4. Veredicto Final de Aprobación para Liberación (Aprobado / Aprobado con Reservas / Rechazado)
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de cumplimiento ISO/MOPROSOFT y adáptalo a:
- repositorio: [NOMBRE O URL]
- workspace/subproyecto: [SI APLICA]
- estandar/compliance: ISO 29110
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA]
- ambiente: STAGING
- componentes: memoria tecnica, planes de prueba, codigo fuente
- documentos a revisar: plan_implementacion, walkthrough, test_build
- objetivo puntual de salida: reporte formal de auditoría de liberación y trazabilidad
- nivel de profundidad: alto
```

---

## Salida esperada

| Control | Estándar | Estado | Evidencia | Acción de remediación |
|---|---|---|---|---|
| Requerimiento mapeado a diseño técnico (ADR) | ISO 29110 §Diseño | Cumple | ADR-042 referenciado en issue #128 | — |
| Trazabilidad requerimiento-código-pruebas | MOPROSOFT DS.3 | No cumple | Sin matriz de trazabilidad para el módulo de pagos | Generar matriz de trazabilidad antes de liberar |
| Pruebas de verificación (unitarias/integración) | ISO 29110 §Construcción | Cumple parcialmente | Cobertura unitaria 68%, sin pruebas de integración | Completar pruebas de integración del flujo de pago |
| Memoria técnica del cambio | MOPROSOFT ASEG | No cumple | No se encontró documento de memoria técnica | Redactar memoria técnica y anexarla al release |
| Cumplimiento de seguridad de la información (ISO 27001) | ISO 27001 | Cumple | Escaneo SAST sin hallazgos críticos | — |

**Veredicto final:** Aprobado con Reservas — la liberación puede continuar únicamente tras generar la matriz de trazabilidad y completar las pruebas de integración faltantes.
