# 9.2 — Monitoreo de CI local y remoto

## Descripción

Prompt para revisar el estado del pipeline de CI local y en GitHub y determinar si los cambios están listos para integrarse: lint, build, pruebas, quality gates, artefactos y checks del PR.

**Cuándo usarlo:** antes de abrir o aprobar un PR, antes de hacer merge a cualquier rama protegida.

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
| pruebas | | | | |
| quality gates | | | | |
| checks PR | | | | |

**Criterio de aprobación:** [APROBADO / RECHAZADO / PENDIENTE]
