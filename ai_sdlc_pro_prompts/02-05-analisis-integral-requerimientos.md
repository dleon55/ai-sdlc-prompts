# 2.5 — Análisis Integral de Requerimientos y Generación de Issues (PRO)

## Descripción

Prompt de ingeniería de software senior diseñado para realizar un análisis exhaustivo de requerimientos nuevos. Integra visión de Arquitectura, Análisis Técnico-Funcional, DBA, DevOps y QA en un solo flujo. Su objetivo es transformar una idea o requerimiento ambiguo en un reporte de trazabilidad y un GitHub Issue que cumpla estrictamente con la **Definition of Ready (DoR)** del proyecto.

**Cuándo usarlo:** al recibir un requerimiento de usuario complejo, una solicitud de cambio (CR) o una idea de producto que aún no ha sido formalizada técnicamente.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — combina arquitectura, DBA, DevOps, seguridad y QA en un solo issue candidato a Definition of Ready; si la validación DoR o el análisis de impacto ISO/IEEE es incompleto, el issue puede pasar a implementación con supuestos no verificados |
| Entradas requeridas | requerimiento_usuario (idea o CR sin formalizar), repositorio, rama_base, documentación y código relacionado existentes |
| Herramientas permitidas | lectura de código, documentación y configuración — el bloque "GitHub Issue Markdown" es un artefacto de texto para copiar manualmente; el prompt no crea ni publica issues en GitHub |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no puede confirmarse el cumplimiento de la Definition of Ready (criterios de aceptación, alcance o impacto verificable), marcar el issue resultante como "no listo" en vez de presentarlo como Ready |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada afirmación en HECHOS debe corresponder a estado verificado del repositorio; SUPUESTOS y RIESGOS deben quedar declarados por separado, no mezclados con hechos |
| Siguiente prompt recomendado | `02-04-triage-backlog-github` si se generan varios issues a priorizar; `04-01-diseno-solucion` si el issue ya fue creado y se continúa al diseño; `02-07-matriz-trazabilidad-requerimientos` para agregar este requerimiento a la matriz de trazabilidad de todo el proyecto |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como una unidad de ingeniería multi-disciplinaria para analizar un requerimiento y generar la documentación técnica y funcional necesaria (Issues) para su implementación.

Entradas:
- repositorio: [NOMBRE O URL]
- requerimiento_usuario: [ENTRADA PRINCIPAL]
- rama_base: [RAMA DESTINO]

Actividades de Análisis:
1. DESCUBRIMIENTO: Identifica la intención central y el valor de negocio.
2. MAPEO TÉCNICO: Localiza componentes, procesos y archivos actuales afectados.
3. ANÁLISIS DE IMPACTO ISO/IEEE: Evalúa cambios en Arquitectura, Base de Datos, Infraestructura/Docker y Seguridad (DevSecOps).
4. TRAZABILIDAD: Relaciona el requerimiento con casos de uso y reglas de negocio.
5. VALIDACIÓN DoR: Asegura que el resultado final sea "Ready" para un desarrollador o agente IA.

Restricciones:
- distingue siempre requerimientos explícitos (dichos textualmente por quien solicita) de requerimientos inferidos (deducidos por el análisis técnico) — nunca los mezcles en la misma afirmación sin etiquetarlos,
- si detectas contradicciones entre el requerimiento_usuario, la documentación existente y el código actual, decláralas explícitamente en HALLAZGOS en vez de resolverlas silenciosamente eligiendo una versión,
- no llenes vacíos de información con supuestos no declarados: toda inferencia usada para completar un vacío debe quedar registrada en SUPUESTOS, nunca presentada como HECHO,
- no marques el issue como listo para Definition of Ready si algún criterio de aceptación, alcance o impacto no puede verificarse contra el repositorio real.

Salida Obligatoria:

1. REPORTE DE ANÁLISIS (Trazabilidad):
   - HECHOS: Estado actual confirmado en el repositorio.
   - HALLAZGOS: Inconsistencias, deuda técnica o dependencias detectadas.
   - SUPUESTOS: Clarificaciones necesarias o asunciones de diseño.
   - RIESGOS: Impactos potenciales en performance, seguridad o colisiones multi-agente.
   - RECOMENDACIONES: Sugerencias de implementación o decisiones de arquitectura (ADR).

2. GITHUB ISSUE MARKDOWN:
   Genera un bloque de código listo para copiar en GitHub con:
   - Título técnico-funcional.
   - User Story (As a... I want... So that...).
   - Acceptance Criteria (Gherkin: Given/When/Then).
   - Technical Tasks Checklist.
   - QA & Testing Strategy.
   - Labels recomendados.

3. MATRIZ DE IMPACTO:
   Tabla con módulos, tablas y servicios afectados y su severidad de impacto.

4. VALIDACIÓN DoR:
   Checklist explícito confirmando o negando cada criterio de Definition of Ready:
   - [ ] Criterios de aceptación verificables presentes
   - [ ] Alcance e impacto confirmados contra el repositorio real
   - [ ] Sin contradicciones abiertas entre requerimiento, documentación y código
   - Resultado: Ready / No Ready (con razón si es No Ready)
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis integral y adáptalo a:
- repositorio: [NOMBRE O URL]
- requerimiento_usuario: [ENTRADA PRINCIPAL]
- rama_base: [RAMA DESTINO]
- documentos a revisar: README, docs/, arquitectura actual, código relacionado.
- objetivo puntual de salida: [OBJETIVO ESPECÍFICO]
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Reporte (H/H/S/R/R) | Estructura formal de hallazgos de ingeniería |
| Matriz de Impacto | Módulos, tablas y servicios afectados |
| GitHub Issue | Markdown completo con User Story y Criterios de Aceptación |
| Validación DoR | Checklist confirmando que el issue está listo para ejecución |
| QA Strategy | Plan de pruebas unitarias y de integración sugerido |

### Ejemplo — matriz de impacto (extracto)

| Módulo / tabla / servicio | Tipo de cambio | Severidad de impacto |
|---|---|---|
| `build.py` (generador de `index.html` e `prompts-index.json`) | Modificación de la lógica de conteo y parseo de prompts | alta — un error aquí rompe el gate `build` del workflow `deploy.yml` y bloquea todo despliegue |
| `ai_sdlc_pro_prompts/*.en.md` (contenido, sin tocar tabla de Contrato editorial) | Adición de bloques `Restricciones:` y filas de ejemplo | media — cambio de contenido documental, sin impacto en build ni en runtime, pero requiere revisión de paridad ES/EN |
