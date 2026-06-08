# 14.1 — Auditoría de dependencias y workspaces en monorepos

## Descripción

Prompt para mapear, auditar y documentar las fronteras arquitectónicas, la red de dependencias locales y los acoplamientos entre subproyectos o workspaces en una arquitectura monorepo.

**Cuándo usarlo:** al inicio de un cambio técnico mayor o refactorización que afecte a bibliotecas compartidas (`packages/`, `shared/`) dentro de un monorrepositorio.

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
