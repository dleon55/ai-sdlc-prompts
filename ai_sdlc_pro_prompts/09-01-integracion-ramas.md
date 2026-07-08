# 9.1 — Integración controlada con ramas

## Descripción

Prompt para planificar la integración de cambios con otras ramas activas: análisis de conflictos potenciales, estrategia recomendada (merge, rebase, cherry-pick) y riesgos de concurrencia con otros agentes o desarrolladores.

**Cuándo usarlo:** antes de hacer merge a cualquier rama destino, especialmente en entornos con cambios concurrentes.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no ejecuta el merge, pero una estrategia mal evaluada puede causar conflictos o sobrescribir cambios de otros agentes o desarrolladores |
| Entradas requeridas | historial de commits, listado de ramas activas, PRs abiertos relacionados |
| Herramientas permitidas | lectura del historial y estado de git (`git log`, `git diff`, `git branch`) — sin ejecutar merge, rebase, cherry-pick ni push |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el estado local no está sincronizado con el remoto (`git fetch` pendiente) o existen ramas activas de otros agentes con cambios no verificados, detener y solicitar sincronización antes de recomendar una estrategia definitiva |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada conflicto potencial debe citar el archivo o zona específica y la rama con la que colisiona |
| Siguiente prompt recomendado | `09-02-monitoreo-ci` una vez ejecutada la integración, para validar el estado del pipeline resultante |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza cómo integrar los cambios con otras ramas activas, evitando conflictos y asegurando consistencia funcional y técnica.

Pasos:
1. Verifica que el estado local esté sincronizado con el remoto (`git fetch`) antes de analizar nada; un análisis sobre información desactualizada puede recomendar una estrategia que ya no aplica.
2. Identifica las ramas activas relacionadas: mismas áreas del código, mismo módulo funcional o mismo issue/epic, y quién las está trabajando (agente o desarrollador).
3. Compara el historial de commits y el diff de cada rama relacionada contra la rama origen para detectar cambios potencialmente conflictivos: mismos archivos, mismas funciones, migraciones de esquema concurrentes.
4. Evalúa la estrategia de integración más adecuada según el tipo de conflicto y el estado de las ramas:
   - merge — cuando el historial debe preservarse y no hay conflictos relevantes,
   - rebase — cuando se busca un historial lineal y la rama origen no ha sido compartida con otros agentes,
   - cherry-pick — cuando solo se necesita un subconjunto de commits,
   - espera controlada — cuando otra rama activa está por mergearse y su resultado cambiaría el análisis,
   - integración por fases — cuando el cambio es grande y conviene dividirlo en pasos verificables.
5. Documenta los riesgos de integración: qué puede romperse, qué pruebas deben re-ejecutarse después de integrar y en qué estado queda cada componente si la integración se detiene a mitad de camino.
6. Define las condiciones que deben cumplirse antes de ejecutar el merge (CI verde, aprobación de code review, ausencia de ramas activas con cambios no verificados) y un plan de rollback si la integración falla.

Restricciones:
- no ejecutes merge, rebase, cherry-pick ni push — este prompt solo produce el análisis y la recomendación, la ejecución requiere aprobación humana explícita,
- si el estado local no está sincronizado con el remoto o existen ramas activas de otros agentes con cambios no verificados, detente y solicita sincronización antes de recomendar una estrategia definitiva,
- no asumas el contenido de una rama que no has podido inspeccionar directamente; si el acceso está limitado, señálalo como brecha de visibilidad en vez de inferir su estado,
- cada conflicto potencial reportado debe citar el archivo o zona específica y la rama con la que colisiona — no generalices "puede haber conflictos" sin evidencia concreta.

Entrega:
- estrategia de integración recomendada con justificación,
- plan de resolución de conflictos,
- condiciones de merge y plan de rollback.
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
| Ramas relacionadas | `feature/checkout-refactor` (rama origen), `feature/payment-retry` (toca `PaymentService`, PR #482 en review, CI verde), `hotfix/payment-timeout` (mergeada hace 2 días, ya integrada en `develop`) |
| Conflictos potenciales | `src/services/PaymentService.ts` — ambas ramas modifican `processPayment()`; `migrations/024_add_retry_column.sql` vs `migrations/025_add_payment_status.sql` — migraciones concurrentes sobre la misma tabla |
| Estrategia recomendada | espera controlada: esperar a que `feature/payment-retry` (PR #482) se mergee a `develop` primero, luego rebase de `feature/checkout-refactor` sobre `develop` — evita resolver el mismo conflicto dos veces y reduce el riesgo de reescribir historia compartida |
| Riesgos de integración | si `PaymentService.processPayment()` cambia de firma en `feature/payment-retry`, las pruebas de integración de checkout pueden fallar silenciosamente hasta el próximo run de CI; posible breaking change para consumidores internos del endpoint `/api/payments` |
| Condiciones de merge | CI verde en ambas ramas, code review aprobado, `feature/payment-retry` mergeado a `develop` antes de iniciar el rebase, sin ramas activas adicionales tocando `PaymentService` |
| Rollback | revert del merge commit en `develop` (`git revert -m 1 <sha>`) + re-ejecutar la suite de integración de pagos antes de reintentar la integración |
