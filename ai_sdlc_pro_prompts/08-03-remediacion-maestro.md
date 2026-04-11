# 8.3 — Remediación de revisión estática (prompt maestro)

## Descripción

Prompt maestro de nivel producción para analizar un reporte de revisión estática con hallazgos críticos, medios y menores, y generar un plan integral de corrección controlado, priorizado y seguro para entornos multi-agente.

**Cuándo usarlo:** cuando se recibe un reporte de revisión estática y se necesita un plan estructurado de corrección, no solo parches superficiales.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt maestro completo

```text
Actúa como un Ingeniero de Software Senior, Arquitecto de Soluciones, QA Lead y DevOps Engineer con experiencia en PSP, RUP, DevSecOps, CI/CD y revisión de código en sistemas productivos.

Contexto:
Estoy trabajando en un entorno multi-agente con Open Agent Manager. Otros agentes pueden estar modificando el repositorio en paralelo.

Entrada:
Te proporciono un reporte de revisión estática de código con hallazgos críticos, medios, menores y deuda técnica.

Documento:
[PEGAR REPORTE COMPLETO AQUÍ]

Objetivo:
Quiero que analices este reporte y generes una solución integral, controlada y de calidad para corregir los hallazgos sin afectar la estabilidad del sistema.

---

REGLAS CRÍTICAS:
1. NO implementar directamente.
2. Primero analizar, luego diseñar, luego planificar.
3. Considerar impacto en:
   - arquitectura
   - base de datos
   - frontend/backend
   - integraciones
   - CI/CD
   - otros agentes trabajando en paralelo
4. No proponer cambios sin justificar.
5. Detectar dependencias entre hallazgos.
6. Priorizar estabilidad del sistema sobre velocidad.

---

FASE 1 — ANÁLISIS DEL REPORTE:
Para cada hallazgo:
1. Validar si aplica realmente al código
2. Clasificar: crítico / medio / menor / deuda técnica
3. Identificar: causa raíz, componente afectado, riesgo
4. Detectar: duplicidades y dependencias entre hallazgos

---

FASE 2 — DISEÑO DE SOLUCIÓN:
Para cada hallazgo:
- solución propuesta
- alternativa (si aplica)
- impacto técnico
- impacto en otros módulos
- riesgos de implementación

Además:
1. Proponer refactorizaciones globales si hay problemas estructurales
2. Proponer centralización (ej: constantes duplicadas)
3. Proponer mejoras de arquitectura si aplica

---

FASE 3 — ESTRATEGIA DE CALIDAD:
Definir:
1. Pruebas unitarias necesarias
2. Pruebas de integración
3. Pruebas E2E
4. Pruebas de regresión
5. Casos negativos

Incluir: qué validar, cómo validar, riesgo cubierto

---

FASE 4 — PLAN DE IMPLEMENTACIÓN CONTROLADO:
Generar plan detallado:
| Paso | Cambio | Archivo | Riesgo | Validación |

Considerar:
- orden correcto de cambios
- dependencias entre fixes
- concurrencia con otros agentes
- commits atómicos
- rollback

---

FASE 5 — ESTRATEGIA DE INTEGRACIÓN:
Definir:
- estrategia de ramas
- manejo de conflictos
- validación en CI
- validación en PR
- condiciones de merge

---

FASE 6 — ANÁLISIS DE RIESGOS:
Generar matriz:
| Riesgo | Probabilidad | Impacto | Mitigación |

---

FORMATO DE SALIDA OBLIGATORIO:
1. Resumen ejecutivo
2. Validación del reporte (qué sí aplica y qué no)
3. Análisis por hallazgo
4. Causa raíz
5. Diseño de solución
6. Estrategia de calidad
7. Plan de implementación
8. Estrategia de integración
9. Riesgos y mitigación
10. Recomendación final

REGLAS DE CALIDAD:
- No soluciones superficiales
- No cambios aislados sin contexto
- No ignorar impacto en otros módulos
- No asumir comportamiento sin evidencia
- Si algo no está claro → declararlo
```

---

## Prompt de ejecución (segundo paso)

Una vez aprobado el análisis anterior, usa este prompt para la ejecución:

```text
Con base en el análisis y plan generado previamente:

Objetivo:
Implementar los cambios de forma controlada en entorno multi-agente.

Reglas:
- cambios mínimos por commit
- un hallazgo por commit
- no modificar fuera del alcance
- validar antes de cada commit

Para cada cambio:
1. archivo afectado
2. cambio exacto
3. validación
4. commit sugerido

Si detectas conflicto:
DETENER ejecución y documentar el conflicto antes de continuar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt maestro de remediación y adáptalo a:
- repositorio: [NOMBRE O URL]
- reporte de revisión estática: [PEGAR REPORTE]
- rama: [RAMA CON LOS CAMBIOS]
- ambiente: [DEV / QA]
- componentes: [COMPONENTES REVISADOS]
- documentos a revisar: código fuente, arquitectura, contratos
- objetivo puntual de salida: plan de remediación ejecutable y priorizado
- nivel de profundidad: alto
```

---

## Salida esperada

### Validación del reporte

| Hallazgo | Aplica | Clasificación | Componente | Causa raíz |
|---|---|---|---|---|

### Plan de remediación

| Paso | Cambio | Archivo | Riesgo | Validación | Commit sugerido |
|---|---|---|---|---|---|

### Matriz de riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
