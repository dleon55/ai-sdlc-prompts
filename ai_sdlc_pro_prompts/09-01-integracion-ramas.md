# 9.1 — Integración controlada con ramas

## Descripción

Prompt para planificar la integración de cambios con otras ramas activas: análisis de conflictos potenciales, estrategia recomendada (merge, rebase, cherry-pick) y riesgos de concurrencia con otros agentes o desarrolladores.

**Cuándo usarlo:** antes de hacer merge a cualquier rama destino, especialmente en entornos con cambios concurrentes.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza cómo integrar los cambios con otras ramas activas, evitando conflictos y asegurando consistencia funcional y técnica.

Incluye:
1. ramas relacionadas,
2. cambios potencialmente conflictivos,
3. estrategia recomendada:
   - merge,
   - rebase,
   - cherry-pick,
   - espera controlada,
   - integración por fases.
4. riesgos de integración.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de integración controlada y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama origen: [RAMA CON LOS CAMBIOS]
- rama destino: [DEVELOP / MAIN / RELEASE]
- ambiente: [QA / STAGING / PROD]
- componentes: [COMPONENTES MODIFICADOS]
- documentos a revisar: historial de commits, ramas activas, PRs abiertos
- objetivo puntual de salida: estrategia de integración con plan de resolución de conflictos
- nivel de profundidad: alto
```

---

## Salida esperada

| Elemento | Detalle |
|---|---|
| Ramas relacionadas | Lista de ramas activas con cambios concurrentes |
| Conflictos potenciales | Archivos o zonas con riesgo de conflicto |
| Estrategia recomendada | merge / rebase / cherry-pick con justificación |
| Riesgos de integración | Qué puede romperse al integrar |
| Condiciones de merge | Criterios que deben cumplirse antes de integrar |
| Rollback | Cómo revertir si la integración falla |
