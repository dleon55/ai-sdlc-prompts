# 7.10 — Implementación de pruebas de humo

## Descripción

Prompt para generar el script ejecutable de pruebas de humo a partir del checklist definido en `07-04`. Produce un artefacto automatizable que valida en minutos que el sistema está operativo después de un despliegue.

**Cuándo usarlo:** después de completar el diseño de pruebas de humo (`07-04`), como paso inmediato post-despliegue para decidir si el ambiente está listo para pruebas completas o requiere rollback.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el **Perfil de stack de pruebas** generado por `07-00` (ejecútalo una vez por proyecto si aún no existe).
> Adjunta o referencia el checklist de pruebas de humo generado por `07-04`.

---

## Prompt completo

```text
Objetivo:
Implementa las pruebas de humo definidas en el checklist adjunto como un script
automatizable que valide la salud del sistema en menos de 15 minutos.

Pasos:
1. Evalúa qué forma de automatización es más adecuada según el proyecto:
   - script de API/HTTP: si los checks son llamadas a endpoints de salud o APIs,
   - script de UI: si requiere interacción con la interfaz (usa el framework E2E disponible),
   - script de shell: si valida procesos, servicios o conectividad a nivel de sistema,
   - combinación de los anteriores si el sistema es mixto.
2. Por cada elemento del checklist, implementa la verificación correspondiente:
   - condición de éxito clara y verificable,
   - mensaje de resultado legible: PASS / FAIL + detalle del error si falla,
   - tiempo máximo de espera por verificación.
3. Organiza los checks en orden de criticidad: los más bloqueantes primero.
4. Implementa un resumen final: total de checks, passed, failed, tiempo total.
5. El script debe retornar código de salida 0 si todo pasa, distinto de 0 si alguno falla
   (para integración con pipelines CI/CD).

Restricciones:
- El script completo debe ejecutarse en menos de 15 minutos.
- No debe generar ni modificar datos de negocio en producción.
- Debe poder ejecutarse sin intervención manual desde línea de comandos o pipeline.

Entrega:
- script de humo ejecutable,
- instrucciones de uso (variables de entorno requeridas, cómo ejecutarlo),
- integración sugerida con el pipeline CI/CD del proyecto.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de implementación de pruebas de humo y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama o versión desplegada: [REFERENCIA]
- ambiente: [QA / STAGING / PROD]
- tipo de script preferido: [AUTO-DETECTAR / API / UI / Shell / Mixto]
- framework E2E disponible: [Playwright / Cypress / ninguno / etc.]
- checklist de humo: [ADJUNTA O REFERENCIA AL DOCUMENTO DE 07-04]
- documentos a revisar: endpoints de salud disponibles, flujos críticos documentados
- objetivo puntual de salida: script ejecutable en pipeline que corra en < 15 minutos
- nivel de profundidad: bajo
```

---

## Salida esperada

Un script autocontenido, por ejemplo:

```
scripts/smoke-test.[sh|py|js|ts]
tests/smoke/smoke.spec.[ext]
```

Con salida en consola como:

```
[SMOKE TEST] Iniciando verificación — ambiente: staging
  [PASS] Login / autenticación (1.2s)
  [PASS] Acceso al módulo principal (0.8s)
  [PASS] Operación básica crítica (2.1s)
  [FAIL] Integración con servicio X — timeout después de 10s
  [PASS] Sin errores visibles en UI (1.5s)

Resultado: 4/5 checks pasaron — FALLO (exit code 1)
Tiempo total: 5.6s
```
