# 14.1 — Auditoría de dependencias y workspaces en monorepos

## Descripción

Prompt para mapear, auditar y documentar las fronteras arquitectónicas, la red de dependencias locales y los acoplamientos entre subproyectos o workspaces en una arquitectura monorepo.

**Cuándo usarlo:** al inicio de un cambio técnico mayor o refactorización que afecte a bibliotecas compartidas (`packages/`, `shared/`) dentro de un monorrepositorio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — mapea el grafo de dependencias de solo lectura, no modifica código ni configuración de los workspaces |
| Entradas requeridas | workspace/subproyecto origen a analizar, archivos de configuración del monorepo (package.json, pnpm-workspace.yaml, go.work, lerna.json, turbo.json, tsconfig.json) |
| Herramientas permitidas | lectura de archivos de configuración y código fuente de los workspaces — sin ejecución de build ni instalación de dependencias |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si los archivos de configuración del monorepo no son accesibles o son ambiguos, declarar el grafo como incompleto en vez de asumir relaciones de dependencia no verificadas |
| Salida esperada | ver `Salida:` dentro de `## Prompt completo` |
| Evidencia mínima | cada dependencia local reportada (directa, transitiva o circular) referencia el archivo de configuración donde se declara |
| Siguiente prompt recomendado | `05-01-plan-implementacion` para planear el refactor de aislamiento; `04-04-adr-decisiones-arquitectura` para documentar la decisión si implica un cambio de frontera arquitectónica |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Mapea la red de dependencias del monorepo e identifica posibles violaciones de arquitectura (ciclos, importaciones no permitidas, dependencias fantasmas) tras el cambio sugerido.

Entradas:
- repositorio: [NOMBRE O URL]
- workspace/subproyecto origen: [WORKSPACE/SUBPROYECTO]
- archivos de configuración (package.json, go.work, lerna.json, turbo.json, tsconfig.json): [LEER O PEGAR DETALLES]

Actividades:
1. Analiza el grafo de dependencias internas y externas del subproyecto/workspace indicado.
2. Identifica:
   - dependencias locales compartidas (e.g. @repo/shared, common-utils),
   - dependencias de runtime externas vs dependencias de desarrollo,
   - posibles importaciones circulares (paquete A importa B y B importa A).
3. Evalúa si el cambio propuesto introduce acoplamiento innecesario.
4. Diseña una matriz de relaciones de importación.

Salida:
1. Mapeo del Grafo de Dependencias (workspaces involucrados)
2. Análisis de Ciclos y Conflictos Potenciales
3. Evaluación de impacto en la velocidad del Build (Turbo/Lerna caching)
4. Recomendación de aislamiento o refactor
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de dependencias en monorepos y adáptalo a:
- repositorio: [NOMBRE O URL]
- workspace/subproyecto: [DIRECTORIO/PAQUETE]
- estandar/compliance: [NINGUNO]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA]
- ambiente: DEV
- componentes: package.json, workspaces, common/
- documentos a revisar: pnpm-workspace.yaml, package.json
- objetivo puntual de salida: grafo de dependencias con matriz de impacto local
- nivel de profundidad: alto
```
