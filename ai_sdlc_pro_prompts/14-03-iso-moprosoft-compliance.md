# 14.3 — Auditoría de cumplimiento de procesos ISO 29110 / MOPROSOFT

## Descripción

Prompt estructurado de aseguramiento de calidad (QA / Audit) para certificar que los entregables funcionales, de diseño y técnicos del ciclo de desarrollo cumplen rigurosamente con los requerimientos de los perfiles básicos de ISO/IEC 29110 y el modelo de procesos MOPROSOFT.

**Cuándo usarlo:** antes del despliegue en entornos controlados (Staging / Prod), como parte de las puertas de calidad (Quality Gates) en la liberación.

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
