# 7.3 — Diseño de pruebas E2E

## Descripción

Prompt para diseñar pruebas end-to-end de los casos de uso impactados por el cambio: desde el actor hasta el resultado final, incluyendo evidencia requerida y regresiones relacionadas.

**Cuándo usarlo:** después de las pruebas de integración (`07-02`), para validar el flujo completo desde la perspectiva del usuario.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño — produce un plan de pruebas E2E en formato tabla, no código ejecutable |
| Riesgo esperado | bajo — es un documento de planificación; no modifica sistemas ni ejecuta pruebas |
| Entradas requeridas | caso de uso o requerimiento a cubrir, criterios de aceptación, referencia al plan de integración previo (`07-02`) |
| Herramientas permitidas | solo lectura de documentación (casos de uso, criterios de aceptación, flujos documentados); no requiere acceso de escritura ni ejecución |
| Autonomía permitida | A1 — Proponer (entrega un plan/artefacto sin aplicar; la ejecución ocurre en `07-09`) |
| Criterios de detención | detener y pedir aclaración si el caso de uso o los criterios de aceptación no están definidos con suficiente detalle para derivar pasos, resultado esperado y evidencia |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de la tabla debe especificar actor, flujo, precondiciones, pasos, resultado esperado, evidencia requerida y regresiones relacionadas |
| Siguiente prompt recomendado | `07-09-implementacion-pruebas-e2e` para convertir este plan en scripts E2E ejecutables |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña pruebas end-to-end para los casos de uso impactados por el cambio.

Pasos:
1. Identifica el actor (rol de usuario) y el flujo principal de punta a punta, desde la entrada del usuario hasta el resultado observable en el sistema.
2. Define las precondiciones necesarias (estado de datos, sesión, permisos) para que el flujo sea reproducible.
3. Detalla los pasos como el usuario los ejecutaría, en el orden exacto, sin saltar interacciones intermedias relevantes.
4. Define el resultado esperado observable (UI, respuesta, estado persistido) y la evidencia mínima requerida para considerarlo validado (captura, log, registro en base de datos).
5. Identifica regresiones relacionadas: qué otros flujos podrían romperse por este cambio y deberían re-verificarse.
6. Prioriza los flujos críticos de negocio (los que generan ingreso, afectan seguridad o tienen mayor volumen de uso) antes que flujos secundarios o poco usados.

Restricciones:
- ejecutar siempre contra un ambiente QA/STAGING, nunca directamente contra producción,
- si el caso de uso o los criterios de aceptación no están definidos con suficiente detalle para derivar pasos y resultado esperado, detente y pide aclaración en vez de asumir el comportamiento,
- cada caso debe ser independiente: no debe depender del estado dejado por otro caso E2E previo.

Entrega:
- matriz de pruebas E2E,
- regresiones relacionadas a re-verificar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de pruebas E2E y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA DE PRUEBAS]
- ambiente: [QA / STAGING]
- componentes: [FLUJOS Y MÓDULOS A PROBAR]
- documentos a revisar: casos de uso, criterios de aceptación, flujos documentados
- objetivo puntual de salida: plan de pruebas E2E con evidencia requerida por caso
- nivel de profundidad: alto
```

---

## Salida esperada

| Actor | Flujo | Precondiciones | Pasos | Resultado esperado | Evidencia | Regresiones |
|---|---|---|---|---|---|---|
| Usuario autenticado | Actualizar dirección de envío en el perfil | sesión activa, al menos una dirección guardada | 1. Ir a Perfil → Direcciones. 2. Editar dirección existente. 3. Guardar cambios. | la dirección se actualiza y aparece preseleccionada en el próximo checkout | captura de pantalla del perfil actualizado + registro en base de datos | checkout con dirección por defecto |
