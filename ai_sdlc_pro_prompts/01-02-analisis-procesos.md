# 1.2 — Localizar procesos, procedimientos y políticas del proyecto

## Descripción

Prompt de arranque para mapear todo el gobierno del proyecto: procesos, procedimientos, políticas, estándares, branching strategy, estrategia QA, CI/CD y reglas de ingeniería. Establece qué sí existe, qué está incompleto y qué no existe.

**Cuándo usarlo:** antes de cualquier trabajo de análisis o implementación, para entender el marco de gobierno del proyecto y evitar violar reglas ya definidas.

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
