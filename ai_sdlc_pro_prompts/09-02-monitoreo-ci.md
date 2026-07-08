# 9.2 — Monitoreo de CI local y remoto

## Descripción

Prompt para revisar el estado del pipeline de CI local y en GitHub y determinar si los cambios están listos para integrarse: lint, build, pruebas, quality gates, artefactos y checks del PR.

**Cuándo usarlo:** antes de abrir o aprobar un PR, antes de hacer merge a cualquier rama protegida.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — es diagnóstico de solo lectura sobre el estado del pipeline, no modifica workflows, código ni re-ejecuta jobs |
| Entradas requeridas | logs de CI local y de GitHub Actions, estado de checks del PR, archivos de `.github/workflows/` |
| Herramientas permitidas | lectura de logs de CI y checks del PR — sin re-ejecutar jobs, sin modificar workflows |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si algún check del PR está en estado pendiente o sin logs accesibles, marcarlo como "pendiente" en el criterio de aprobación en vez de asumir que pasó o falló |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada falla reportada debe citar el job, el paso y el mensaje de error específico del log |
| Siguiente prompt recomendado | `09-01-integracion-ramas` si el pipeline está en verde y se procede a integrar con la rama destino |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Revisa el estado del pipeline de CI tanto localmente como en GitHub y determina si los cambios están listos para integrarse.

Valida:
- lint,
- build,
- pruebas,
- quality gates,
- workflows,
- artefactos,
- checks del PR.

Restricciones:
- este es un monitoreo de solo lectura: no re-ejecutes, canceles ni apruebes jobs de CI, y no modifiques archivos de workflow como parte de este análisis — cualquier acción sobre el pipeline requiere aprobación humana explícita fuera de este prompt,
- toda falla reportada debe citar el job y el paso exactos, junto con el mensaje de error específico del log — no generalices "los tests fallaron" sin señalar cuáles,
- distingue explícitamente una falla intermitente (flaky test, timeout de infraestructura, dependencia externa caída) de una regresión genuina causada por el cambio bajo revisión; si no hay evidencia suficiente para decidir, márcalo como "requiere reintento o investigación adicional" en vez de clasificarlo como una u otra,
- si un check sigue en estado pendiente o sin logs accesibles, no lo cuentes como aprobado ni como fallido — repórtalo como pendiente en el criterio de aprobación final.

Entrega:
1. estatus general,
2. fallas detectadas,
3. causa probable,
4. acción recomendada,
5. criterio de aprobación o rechazo.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de monitoreo CI y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA DEL PR O INTEGRACIÓN]
- ambiente: [QA / STAGING / PROD]
- componentes: [COMPONENTES MODIFICADOS]
- documentos a revisar: .github/workflows/, logs de CI, checks del PR
- objetivo puntual de salida: estado del pipeline + criterio de aprobación
- nivel de profundidad: medio
```

---

## Salida esperada

| Validación | Estado | Resultado | Causa probable | Acción |
|---|---|---|---|---|
| lint | | | | |
| build | | | | |
| pruebas | ⚠️ Falló | 2 de 148 pruebas fallaron en `test_build_unit.py::test_missing_field` | Timeout intermitente al leer `00-framework.md` en el runner de CI (falla aislada, no reproducible en local) | Reintentar el job antes de bloquear el PR; si persiste en un segundo intento, investigar como regresión |
| quality gates | | | | |
| workflows | | | | |
| artefactos | | | | |
| checks PR | ✅ Aprobado | Todos los checks requeridos (`lint`, `build`, `tests`) están en verde | — | Ninguna — listo para merge una vez resuelto el punto anterior |

**Criterio de aprobación:** [APROBADO / RECHAZADO / PENDIENTE]
