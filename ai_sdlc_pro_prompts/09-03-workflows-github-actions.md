# 9.3 — Revisión de workflows de GitHub Actions

## Descripción

Prompt para auditar los workflows del repositorio y verificar si cubren adecuadamente validación, pruebas, seguridad, despliegue y calidad. Detecta vacíos, riesgos y propone mejoras.

**Cuándo usarlo:** periódicamente como revisión de salud del pipeline, o al incorporar nuevos módulos o ambientes.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no modifica workflows directamente, solo audita y recomienda |
| Entradas requeridas | contenido de `.github/workflows/`, README de CI/CD |
| Herramientas permitidas | lectura de archivos de workflow — sin ejecución de jobs ni cambios al pipeline |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si un workflow referencia secretos o permisos no inspeccionables sin acceso a la configuración del repositorio, documentarlo como brecha de visibilidad en vez de asumir su estado |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada brecha reportada debe citar el archivo de workflow y el job específico |
| Siguiente prompt recomendado | `11-02-hardening-seguridad` si se detectan brechas de seguridad en el pipeline |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza los workflows del repositorio y determina si cubren adecuadamente validación, pruebas, seguridad, despliegue y calidad.

Pasos:
1. Inventaría todos los workflows en `.github/workflows/`: nombre, archivo, disparadores (push, pull_request, schedule, workflow_dispatch, release) y jobs que contiene cada uno.
2. Para cada job, identifica qué valida realmente (lint, build, tests, escaneo de seguridad, despliegue) y con qué herramienta — no asumas por el nombre del job, revisa los steps.
3. Compara el inventario contra las áreas de cobertura esperadas (validación/lint, build, pruebas unitarias, pruebas de integración, análisis de seguridad, despliegue por ambiente, notificaciones) y marca cada una como cubierta, parcial o faltante.
4. Para las áreas cubiertas, evalúa si la cobertura es suficiente: ¿el job realmente bloquea el merge o solo es informativo? ¿corre en cada push o solo en algunos casos? ¿tiene umbrales de fallo definidos (cobertura mínima, severidad de vulnerabilidades)?
5. Para las áreas faltantes o parciales, prioriza por riesgo: primero brechas de seguridad y despliegue sin control (pueden causar incidentes en producción), luego brechas de pruebas (pueden dejar pasar bugs), y por último brechas de notificación o eficiencia.
6. Verifica permisos y secretos usados por cada workflow (`permissions:`, `secrets.*`) y si siguen el principio de mínimo privilegio; si no puedes inspeccionar la configuración real del repositorio (secretos, environments protegidos), documenta esto como brecha de visibilidad en vez de asumir su estado.
7. Redacta mejoras recomendadas, priorizadas y accionables, indicando el archivo y el job específico a modificar.

Restricciones:
- no ejecutes ni dispares ningún workflow, y no modifiques archivos de `.github/workflows/` — esto es una auditoría de solo lectura,
- no asumas el estado de secretos, permisos o environments protegidos que no puedas inspeccionar directamente; decláralo como brecha de visibilidad en vez de inventar su configuración,
- cada brecha reportada debe citar el archivo de workflow y el job específico afectado — no generalices sin evidencia concreta,
- si un workflow depende de un servicio externo (registry, ambiente de despliegue) cuyo estado no puedes verificar, señálalo explícitamente en vez de dar por hecho que funciona.

Entrega:
- inventario completo de workflows,
- análisis de cobertura por área con brechas y riesgos,
- mejoras recomendadas priorizadas por riesgo.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión de workflows y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- documentos a revisar: .github/workflows/, README de CI/CD
- objetivo puntual de salida: inventario de workflows con brechas y mejoras recomendadas
- nivel de profundidad: medio
```

---

## Salida esperada

### Inventario de workflows

| Workflow | Archivo | Disparador | Jobs | Propósito |
|---|---|---|---|---|
| CI Build & Test | `.github/workflows/ci.yml` | `push` a cualquier rama, `pull_request` hacia `main`/`develop` | `lint`, `build`, `unit-tests`, `integration-tests` | Validar que el código compila, pasa lint y pruebas antes de mergear |
| Security Scan | `.github/workflows/security.yml` | `pull_request` hacia `main`, `schedule` semanal | `dependency-scan`, `sast`, `secret-scan` | Detectar dependencias vulnerables, código inseguro y secretos filtrados |
| Deploy Staging | `.github/workflows/deploy-staging.yml` | `push` a `develop` | `build-image`, `deploy-staging`, `smoke-test` | Desplegar automáticamente a Staging tras cada merge a `develop` |
| Deploy Production | `.github/workflows/deploy-prod.yml` | `release: published`, `workflow_dispatch` | `build-image`, `approve-gate`, `deploy-prod`, `notify` | Desplegar a producción con aprobación manual tras crear un release |

### Análisis de cobertura

| Área | Cubierta | Workflow | Faltante | Riesgo | Recomendación |
|---|---|---|---|---|---|
| validación / lint | Sí | CI Build & Test (`lint`) | — | bajo | mantener como está |
| build | Sí | CI Build & Test (`build`) | — | bajo | cachear dependencias para reducir el tiempo de pipeline |
| pruebas unitarias | Sí | CI Build & Test (`unit-tests`) | sin gate de cobertura mínima | medio | agregar umbral de cobertura que bloquee el merge si baja del objetivo |
| pruebas integración | Sí | CI Build & Test (`integration-tests`) | corre contra mocks, no contra una BD efímera real | medio | migrar el job a un contenedor de BD efímero para pruebas más realistas |
| análisis seguridad | Parcial | Security Scan (`dependency-scan`, `sast`) | sin escaneo de la imagen Docker final | alto | agregar `trivy` (o similar) al job de build de la imagen |
| despliegue DEV | No | — | no existe workflow de despliegue a DEV, se hace manual | medio | automatizar despliegue a DEV en cada push a `develop` o a feature branches |
| despliegue QA | No | — | no existe ambiente de QA separado de Staging | bajo | evaluar si se necesita un ambiente QA propio o si Staging cubre ese propósito |
| despliegue PROD | Sí | Deploy Production | sin rollback automático si el smoke test post-deploy falla | alto | agregar job de rollback automático ante fallo del smoke test |
| notificaciones | Parcial | Deploy Production (`notify`) | solo notifica despliegues a prod, no fallos de CI en `main`/`develop` | bajo | agregar notificación a Slack/Teams cuando CI falla en ramas protegidas |
