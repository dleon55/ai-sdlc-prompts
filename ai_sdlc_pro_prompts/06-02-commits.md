# 6.2 — Generación de mensajes de commit de calidad

## Descripción

Prompt para generar mensajes de commit pequeños, claros y trazables, alineados al estándar del proyecto. Incluye alternativas si el cambio debe dividirse en múltiples commits.

**Cuándo usarlo:** antes de hacer commit de cualquier cambio, para garantizar trazabilidad y consistencia con el historial del repositorio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — solo redacta texto sobre un diff ya existente, no ejecuta cambios |
| Entradas requeridas | issue, tipo de cambio, componente, descripción breve del cambio ya realizado |
| Herramientas permitidas | ninguna de ejecución — redacción de texto únicamente |
| Autonomía permitida | A1 — Proponer (el commit/push real lo ejecuta el flujo estándar de git, no este prompt) |
| Criterios de detención | si el cambio descrito mezcla intenciones no relacionadas, detener y recomendar dividir en commits separados antes de proponer el mensaje final |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | mensaje de commit válido bajo Conventional Commits (ver `CONTRIBUTING.md`) |
| Siguiente prompt recomendado | ninguno — es el último paso antes de `git push` |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera mensajes de commit pequeños, claros, trazables y alineados al estándar del proyecto.

Entradas:
- issue,
- tipo de cambio,
- componente,
- descripción breve.

Restricciones:
- nunca agrupes cambios sin relación funcional o técnica en un mismo commit; si la descripción breve mezcla dos intenciones distintas, recomienda dividir antes de proponer el mensaje final,
- nunca sugieras reescribir historial ya publicado (`git rebase`, `git commit --amend`, `git push --force`) sin aprobación humana explícita — el mensaje propuesto es para un commit nuevo, no para modificar uno existente,
- sigue estrictamente el formato Conventional Commits (`tipo(componente): descripción #issue`), usando únicamente los tipos definidos en `CONTRIBUTING.md` (feat, fix, refactor, docs, test, chore, entre otros permitidos),
- no inventes número de issue ni componente si no fueron provistos en las entradas; márcalo como pendiente de completar en vez de asumirlo.

Entrega:
1. commit principal sugerido
2. commits alternativos si el cambio debe dividirse
3. justificación de por qué conviene dividir el trabajo
```

---

## Uso con fórmula estándar

```text
Usa el prompt de mensajes de commit y adáptalo a:
- issue: [NÚMERO O REFERENCIA]
- tipo de cambio: [feat / fix / refactor / docs / test / chore]
- componente: [MÓDULO O ARCHIVO AFECTADO]
- descripción breve: [QUÉ SE HIZO EN UNA LÍNEA]
- objetivo puntual de salida: commit principal + alternativas si aplica dividir
```

### Ejemplo real

```text
Usa el prompt de mensajes de commit y adáptalo a:
- issue: #842
- tipo de cambio: fix
- componente: api/notificaciones
- descripción breve: corrige envío duplicado de notificaciones push al actualizar orden
```

---

## Formatos de commit recomendados

```text
fix(api/notificaciones): corrige envío duplicado al actualizar orden #842

feat(auth): agrega validación de expiración de token en middleware #123

refactor(db): extrae consulta de usuarios a repositorio separado #456

docs(readme): actualiza instrucciones de despliegue en Docker #78

test(pagos): agrega casos borde para monto negativo en procesador #99
```

## Salida esperada

| Commit | Descripción | Justificación |
|---|---|---|
| Principal | `fix(api/notificaciones): corrige envío duplicado al actualizar orden #842` | Aísla el fix funcional solicitado en el issue; es el cambio mínimo necesario para resolver #842 |
| Alternativa 1 | `refactor(api/notificaciones): extrae lógica de deduplicación a función utilitaria` | El diff original incluía una refactorización no solicitada; se separa para no mezclar la intención de fix con una mejora de diseño |
| Alternativa 2 | `chore(logging): agrega logs de depuración en servicio de notificaciones` | Los logs agregados durante la investigación no son parte del fix; deben ir en un commit aparte o descartarse antes de mergear |
