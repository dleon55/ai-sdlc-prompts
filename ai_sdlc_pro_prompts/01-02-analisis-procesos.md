# 1.2 — Localizar procesos, procedimientos y políticas del proyecto

## Descripción

Prompt de arranque para mapear todo el gobierno del proyecto: procesos, procedimientos, políticas, estándares, branching strategy, estrategia QA, CI/CD y reglas de ingeniería. Establece qué sí existe, qué está incompleto y qué no existe.

**Cuándo usarlo:** antes de cualquier trabajo de análisis o implementación, para entender el marco de gobierno del proyecto y evitar violar reglas ya definidas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — es una localización de solo lectura de documentos de gobierno; no ejecuta cambios, aunque omitir una política existente puede llevar a violarla en trabajo posterior |
| Entradas requeridas | acceso de lectura a README, docs/, wiki exportada, ADRs, archivos de contribución y workflows del repositorio |
| Herramientas permitidas | lectura de documentación, markdowns y archivos de configuración — sin ejecución ni cambios |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si no se encuentra evidencia documental de una categoría de gobierno (por ejemplo, seguridad o branching), declararla como "no existe" en vez de asumir una política implícita |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada fila de la matriz debe citar el archivo o ruta encontrada; las categorías marcadas como incompletas o inexistentes deben indicar qué se buscó y no se halló |
| Siguiente prompt recomendado | `01-01-arranque-comprension-repositorio` si aún no se hizo el inventario técnico; `02-01-analisis-issue` para iniciar el análisis funcional del trabajo concreto |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Quiero que identifiques dentro del repositorio todos los documentos, archivos o secciones que correspondan a procesos, procedimientos, políticas, estándares, lineamientos, guías de codificación, flujos de trabajo, definición de ramas, estrategia QA, estrategia CI/CD y reglas de ingeniería de software.

Actividades:
1. Busca en README, docs, wiki exportada, carpetas de documentación, markdowns, ADRs, archivos de contribución y workflows.
2. Clasifica lo encontrado por categoría:
   - procesos,
   - procedimientos,
   - políticas,
   - estándares,
   - arquitectura,
   - QA,
   - seguridad,
   - branching,
   - despliegue,
   - operación.
3. Indica qué sí existe, qué está incompleto y qué no existe.

Restricciones:
- basa cada hallazgo en evidencia observable (el archivo, la sección o el commit donde está documentado); no lo bases en supuestos sobre cómo "debería" trabajar un equipo,
- distingue explícitamente entre "no está documentado" y "no existe el proceso" — la ausencia de un documento no prueba que la práctica no se siga informalmente, así que decláralo como falta de documentación, no como ausencia del proceso,
- no ejecutes cambios ni crees documentación nueva; este prompt solo localiza y clasifica lo que ya existe,
- si una categoría de gobierno no tiene evidencia documental encontrada, márcala como "no existe" en la matriz en vez de asumir una política implícita.

Formato de salida:
- matriz por categoría,
- archivo/ruta encontrada,
- descripción,
- nivel de completitud,
- observaciones.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de localización de procesos y políticas y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA ACTUAL]
- documentos a revisar: README, docs/, .github/, workflows/
- objetivo puntual de salida: matriz de gobierno del proyecto con estado de completitud
- nivel de profundidad: medio
```

---

## Salida esperada

Matriz con las siguientes columnas:

| Categoría | Archivo/Ruta | Descripción | Completitud | Observaciones |
|---|---|---|---|---|
| procesos | `CONTRIBUTING.md` | Define el flujo de contribución: estructura ES/EN obligatoria, cómo correr `build.py` y validaciones previas al PR | Completo | Referencia el Contrato editorial pero no detalla el proceso de revisión humana post-agente |
| QA | `tests/test_build.py`, `tests/test_i18n.py` | Suite pytest que valida generación del índice, paridad ES/EN y estructura de cada prompt | Completo | No hay documento de estrategia QA aparte de los propios tests; falta explicitarla en texto |
| despliegue | `.github/workflows/deploy.yml` | Pipeline de GitHub Actions que construye y publica `index.html` | Incompleto | No documenta condiciones de rollback ni ambiente de staging previo a producción |
| procedimientos | | | | |
| políticas | | | | |
| estándares | | | | |
| arquitectura | | | | |
| seguridad | | | | |
| branching | | | | |
| operación | | | | |
