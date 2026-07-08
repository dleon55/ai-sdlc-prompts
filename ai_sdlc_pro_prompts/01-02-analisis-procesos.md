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
| procesos | | | | |
| procedimientos | | | | |
| políticas | | | | |
| estándares | | | | |
| arquitectura | | | | |
| QA | | | | |
| seguridad | | | | |
| branching | | | | |
| despliegue | | | | |
| operación | | | | |
