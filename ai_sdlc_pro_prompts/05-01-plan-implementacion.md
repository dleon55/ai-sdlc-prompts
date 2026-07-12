# 5.1 — Plan de implementación detallado

## Descripción

Prompt para elaborar un plan de implementación ejecutable y trazable: actividades previas, cambios por componente, migraciones, pruebas, despliegue, rollback y evidencias esperadas por paso.

**Cuándo usarlo:** después del diseño aprobado (`04-01`), antes de ejecutar cualquier cambio en el repositorio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — no ejecuta cambios, pero es la base sobre la que se autorizará la implementación real; un plan incompleto u optimista puede derivar en ejecución sin rollback o evidencia definidos |
| Entradas requeridas | diseño aprobado (`04-01`), arquitectura, contratos, rama objetivo, ambiente de destino, componentes a modificar |
| Herramientas permitidas | solo lectura de diseño/arquitectura/contratos; no ejecuta comandos ni modifica el repositorio, produce el plan como documento |
| Autonomía permitida | A1 — Proponer (plan o artefacto sin aplicar); no autoriza por sí sola ejecutar, commitear ni desplegar |
| Criterios de detención | detener si no existe diseño aprobado del cual partir; no dejar pasos sin evidencia esperada, dependencia o riesgo declarado; señalar explícitamente si algún paso requiere ambiente de producción |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | bloque JSON de metadatos parseable al inicio, cada paso (1–9) con evidencia esperada definida, registro de métricas PSP/TSP completo |
| Siguiente prompt recomendado | `05-02-riesgos-implementacion`, en paralelo, antes de pasar a `06-01-implementacion-multiagente`; `07-00-deteccion-stack-pruebas` para detectar el stack de pruebas activo antes de definir las pruebas requeridas por paso (paso 4) |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Elabora un plan de implementación detallado, ejecutable y trazable para la solución propuesta.

Pasos:
0. Abre con un bloque JSON de metadatos parseable (claves: status, task_count, impacted_components, estimated_hours) — permite que herramientas de orquestación o CI lean el plan sin re-interpretar texto libre.
1. Lista las actividades previas necesarias antes de tocar código (accesos, creación de rama, backups, feature flags, aviso a stakeholders).
2. Detalla los cambios por componente, con el mismo alcance y granularidad que el diseño aprobado (`04-01`) — si agregas un componente que el diseño no contemplaba, señálalo explícitamente como desviación en vez de incluirlo sin comentario.
3. Especifica los ajustes de datos o migraciones necesarios, indicando si son reversibles y qué ocurre con los datos existentes durante y después de la migración.
4. Define las pruebas requeridas por paso (unitarias, integración, E2E, performance), priorizando las que cubren el camino crítico del cambio antes que casos periféricos si el tiempo de QA es limitado.
5. Define las validaciones a ejecutar en cada ambiente (dev/QA/staging) antes de promover el cambio al siguiente, y qué resultado habilita el paso al ambiente posterior.
6. Describe la estrategia de integración con ramas: orden de merges, resolución de conflictos esperada y quién aprueba cada integración.
7. Detalla el despliegue: orden de despliegue por componente, ventanas de mantenimiento si aplica, y quién ejecuta cada paso.
8. Detalla el rollback por paso — si algún paso no tiene rollback posible, decláralo explícitamente en vez de omitirlo o asumir que no hará falta.
9. Define la evidencia esperada por paso (logs, capturas, resultados de test, métricas) que demuestre de forma verificable que el paso se completó.
10. Cierra con el Registro de Métricas PSP/TSP: tiempo de diseño estimado en minutos, tiempo de codificación estimado en minutos y conteo estimado de defectos, para comparar después contra lo real.

Restricciones:
- no ejecutes comandos ni modifiques el repositorio o el ambiente — este prompt produce el plan como documento; ejecutar, commitear o desplegar requiere aprobación explícita y un prompt separado,
- no dejes ningún paso (1 a 9) sin dependencia, riesgo o evidencia esperada declarados; si alguno de esos campos no aplica, dilo explícitamente en vez de dejarlo vacío,
- si algún paso requiere ambiente de producción, señálalo de forma explícita y no lo mezcles con pasos de dev/QA/staging,
- si no existe un diseño aprobado (`04-01`) del cual partir, detente y solicítalo — no derives el plan de supuestos propios,
- el bloque JSON de metadatos debe ser válido y parseable (sin comentarios, sin claves faltantes) — no lo reemplaces por una descripción en texto libre.

Formato para pasos 1 a 9:
| Paso | Actividad | Componente | Dependencia | Riesgo | Evidencia esperada |
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan de implementación y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES A MODIFICAR]
- documentos a revisar: diseño aprobado, arquitectura, contratos
- objetivo puntual de salida: plan de implementación ejecutable paso a paso
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección / Paso | Actividad | Componente | Dependencia | Riesgo | Evidencia esperada |
|---|---|---|---|---|---|
| Metadatos JSON (0) | `{"status":"planned","task_count":6,"impacted_components":["build.py","tests/test_i18n.py"],"estimated_hours":6}` | - | - | - | - |
| Paso 2 — Cambios por componente | Agregar función `check_i18n_parity()` en `build.py` que compare encabezados `##` entre cada `.md` y su `.en.md` | `build.py` | Diseño aprobado en `04-01` | Falsos positivos por diferencias de formato menores entre idiomas | Test unitario en `tests/test_i18n.py` en verde + log de build mostrando el chequeo ejecutado |
| Paso 8 — Rollback | Revertir el commit que agrega el chequeo; el build vuelve a generar `index.html` sin la validación de paridad | `build.py` | Paso 2 completado | Bajo — cambio aislado en un solo script, sin efecto en datos | Ejecución de build post-revert cuyo log no incluye el paso de validación |
| Métricas PSP/TSP (10) | Diseño: 45 min · Codificación: 180 min · Defectos proyectados: 1 | - | - | - | - |
