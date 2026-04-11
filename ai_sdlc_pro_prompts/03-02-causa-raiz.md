# 3.2 — Análisis de causa raíz

## Descripción

Prompt para investigar un defecto o incidente y determinar la causa raíz real, no solo el síntoma. Incluye formulación de hipótesis, validación con evidencia y recomendación de remediación.

**Cuándo usarlo:** al investigar defectos en QA o producción, cuando el síntoma está claro pero la causa no.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza un defecto o incidente y determina la causa raíz real, no solo el síntoma.

Actividades:
1. Define el síntoma observado.
2. Revisa evidencia:
   - logs,
   - código,
   - configuraciones,
   - consultas,
   - commits recientes,
   - despliegues recientes.
3. Formula hipótesis.
4. Valida hipótesis con evidencia.
5. Determina:
   - causa raíz,
   - factores contribuyentes,
   - impacto,
   - módulos afectados.
6. Si no se puede confirmar totalmente, indica evidencia faltante y nivel de confianza.

Salida:
1. Síntoma
2. Evidencia
3. Hipótesis
4. Causa raíz confirmada o probable
5. Factores contribuyentes
6. Riesgo asociado
7. Recomendación de remediación
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de causa raíz y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue: [NÚMERO O REFERENCIA]
- rama: [RAMA AFECTADA]
- ambiente: [QA / STAGING / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: logs, código, commits recientes, configuraciones
- objetivo puntual: confirmar causa raíz y proponer plan de solución
- nivel de profundidad: alto
```

### Ejemplo real

```text
Usa el prompt de análisis de causa raíz y adáptalo a:
- repositorio: urgemy-api
- issue: #842
- rama: urgemy-test
- ambiente: QA
- componentes: api, notificaciones push, postgres
- documentos a revisar: README, docs/notificaciones, workflows, issues relacionados
- objetivo puntual: confirmar causa raíz y proponer plan de solución
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Síntoma | Comportamiento observado con evidencia |
| Evidencia revisada | Logs, código, commits, configuraciones |
| Hipótesis | Posibles causas ordenadas por probabilidad |
| Causa raíz | Confirmada o probable con nivel de confianza |
| Factores contribuyentes | Condiciones que permitieron el problema |
| Riesgo | Impacto si no se corrige |
| Remediación | Plan de corrección recomendado |
