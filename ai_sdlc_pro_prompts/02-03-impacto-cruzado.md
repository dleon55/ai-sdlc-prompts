# 2.3 — Análisis de impacto cruzado

## Descripción

Prompt para evaluar el impacto del cambio en todos los módulos, procesos, datos, integraciones, ambientes y pipelines del sistema. Detecta impactos directos e indirectos y genera una matriz de severidad.

**Cuándo usarlo:** después del análisis técnico profundo (`02-02`) y antes del diseño de la solución (`04-01`).

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — aunque es de solo lectura, tiene alcance amplio (módulos, datos, integraciones, ambientes, pipelines, semver); subestimar un impacto puede dejar pasar una ruptura de retrocompatibilidad o un riesgo de producción no detectado |
| Entradas requeridas | resultado de `02-02` (flujo técnico y dependencias), arquitectura, contratos de API, esquema de base de datos, componentes involucrados |
| Herramientas permitidas | lectura de código, arquitectura, contratos y configuración — sin ejecución ni cambios |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si no hay evidencia suficiente para descartar impacto en un componente crítico (seguridad, datos, producción, semver), clasificarlo como riesgo alto no confirmado en vez de omitirlo de la matriz |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de la matriz de impacto debe citar el componente o contrato verificado, no solo asumido por nombre o convención |
| Siguiente prompt recomendado | `04-01-diseno-solucion` |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el impacto del cambio solicitado en otros módulos, procesos, datos, integraciones, ambientes, pipelines, subproyectos del monorepo y políticas de versionado (semver).

Actividades:
1. Evalúa impacto en:
   - subproyectos / workspaces del monorepo (por ejemplo, dependencias compartidas, utilerías comunes),
   - contratos de API y versionado semántico (semver) de paquetes locales,
   - frontend,
   - backend,
   - base de datos,
   - integraciones,
   - infraestructura,
   - CI/CD (pipelines de build independientes o compartidos),
   - seguridad y conformidad normativa (ISO, MAAGTICSI, etc.),
   - monitoreo,
   - documentación.
2. Detecta impactos directos e indirectos.
3. Evalúa afectación a otros casos de uso.

Restricciones:
- este es un análisis de solo lectura: no modifiques código, configuración ni contratos de API para evaluar el impacto,
- para cada componente marcado como impactado, traza la cadena real de dependencias o imports que lo conecta con el cambio (archivo que importa, función que invoca, contrato que consume) — no lo marques por similitud de nombre o por intuición arquitectónica,
- si no puedes verificar la cadena de dependencia de un componente crítico (seguridad, datos, producción, semver) por falta de visibilidad (código no accesible, contrato no versionado, documentación ausente), clasifícalo como riesgo alto no confirmado y señala explícitamente la brecha de visibilidad — nunca lo omitas de la matriz ni lo des por seguro sin evidencia,
- no cierres la matriz de impacto con severidades "bajo" en componentes que no pudiste inspeccionar directamente.

Salida:
- matriz de impacto (incluyendo workspaces y paquetes del monorepo),
- severidad,
- componente/workspace afectado,
- tipo de impacto (directo/indirecto, ruptura de retrocompatibilidad),
- riesgo,
- recomendación de mitigación.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de impacto cruzado y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: arquitectura, contratos API, esquema de BD
- objetivo puntual de salida: matriz de impacto cruzado con severidad por componente
- nivel de profundidad: alto
```

---

## Salida esperada

| Componente | Tipo de impacto | Severidad | Riesgo | Recomendación |
|---|---|---|---|---|
| CI/CD | Directo — `deploy.yml` invoca `build.py` en cada push a `main`; si `build.py` cambia su firma de validación, el step `python build.py` puede fallar el pipeline | Alto | El workflow no tiene un paso de rollback automático si `build.py` termina en error a mitad de la generación del índice | Agregar un paso de verificación (`pytest tests/test_build.py`) antes de generar `index.html` en el pipeline |
| documentación | Indirecto — cada prompt modificado en `ai_sdlc_pro_prompts/*.md` requiere actualizar su par `.en.md`; verificado por import/lectura cruzada en `tests/test_i18n.py` | Medio | Riesgo de que el build publique un par ES/EN desincronizado si el test de paridad no se ejecuta en CI | Confirmar que `test_i18n.py` corre en `deploy.yml` antes del build, no solo en local |
| frontend | | | | |
| backend | | | | |
| base de datos | | | | |
| integraciones | | | | |
| infraestructura | | | | |
| seguridad | | | | |
| monitoreo | | | | |
