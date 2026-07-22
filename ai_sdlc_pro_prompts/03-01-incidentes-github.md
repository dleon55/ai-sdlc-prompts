# 3.1 — Revisión de incidentes reportados por tester contra GitHub Issues

## Descripción

Prompt para normalizar incidentes de testing, compararlos contra issues existentes en GitHub, detectar duplicados, incompletos o mal documentados, y redactar los que no existen con el estándar del proyecto.

**Cuándo usarlo:** al recibir un reporte de ciclo de QA, antes de gestionar cualquier defecto en GitHub.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — clasificar mal un incidente como duplicado o "ya existe" puede ocultar un defecto real sin reportar |
| Entradas requeridas | reporte de incidentes de QA normalizado, acceso de lectura a issues abiertos y cerrados en GitHub |
| Herramientas permitidas | lectura/búsqueda de issues en GitHub — sin crear, cerrar, comentar ni modificar issues |
| Autonomía permitida | A1 — Proponer (redacta issues y acciones, no las ejecuta) |
| Criterios de detención | el propio prompt restringe explícitamente su alcance a análisis y redacción; nunca ejecutar acciones de mutación en GitHub |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada incidente clasificado debe referenciar el issue de GitHub equivalente (o su ausencia confirmada) |
| Siguiente prompt recomendado | `03-02-causa-raiz` si un incidente confirmado requiere investigación de causa raíz |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza los incidentes reportados por testing y compáralos con los issues existentes en GitHub para determinar si ya existen, si están bien documentados y cuál es su estatus actual.

Actividades:
1. Normaliza cada incidente:
   - título,
   - descripción,
   - pasos para reproducir,
   - resultado actual,
   - resultado esperado,
   - severidad,
   - ambiente,
   - módulo.
2. Busca equivalentes en GitHub.
3. Clasifica cada incidente en:
   - existe y está correcto,
   - existe pero está incompleto,
   - existe pero está mal documentado,
   - es un duplicado de otro incidente ya reportado,
   - no existe.
4. Propón acción:
   - comentar,
   - actualizar,
   - reabrir,
   - crear,
   - relacionar,
   - marcar duplicado.
5. Si no existe, redacta el issue completo con el estándar del proyecto.

Restricciones:
Este prompt es de solo análisis y redacción. No ejecutes comandos que creen, cierren, comenten o modifiquen issues en GitHub; entrega únicamente las acciones propuestas y el contenido redactado para revisión humana.

Salida:
1. Resumen ejecutivo
2. Matriz QA vs GitHub
3. Issues a crear
4. Issues a actualizar
5. Issues con problemas de trazabilidad
6. Recomendaciones de mejora al proceso QA → GH
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión de incidentes y adáptalo a:
- repositorio: [NOMBRE O URL]
- reporte de QA: [PEGAR LISTA DE INCIDENTES]
- rama: [RAMA EN PRUEBAS]
- ambiente: [QA / STAGING]
- módulos probados: [MÓDULOS]
- documentos a revisar: issues abiertos y cerrados en GitHub, estándar de documentación de issues
- objetivo puntual de salida: matriz QA vs GitHub + issues redactados para crear/actualizar
- nivel de profundidad: alto
```

---

## Salida esperada

### Resumen ejecutivo

| Métrica | Valor |
|---|---|
| Total incidentes reportados | 14 |
| Existen y están correctos | 6 |
| Existen pero incompletos | 3 |
| No existen | 4 |
| Duplicados | 1 |

### Matriz QA vs GitHub

| Incidente | Severidad | Issue GH | Estado actual | Acción propuesta |
|---|---|---|---|---|
| INC-014 — build.py no valida par ES/EN antes de publicar | alta | ninguno encontrado | No existe | Crear |
| INC-015 — timeout intermitente en test_build_unit | media | #138 | Existe, incompleto (falta ambiente y pasos) | Comentar solicitando datos faltantes |
| INC-016 — mismo síntoma que INC-014 reportado por otro tester | alta | (mismo que INC-014, aún sin issue) | Duplicado de INC-014 | Marcar duplicado, no crear issue nuevo |

### Issues a crear

| Incidente | Título propuesto | Severidad | Labels |
|---|---|---|---|
| INC-014 | fix: build.py no valida par ES/EN antes de publicar | alta | bug, agente-ia |

### Issues a actualizar / con problemas de trazabilidad

| Issue GH | Problema detectado | Acción propuesta |
|---|---|---|
| #138 | Falta ambiente y pasos de reproducción exactos | Comentar solicitando los campos faltantes antes de cerrar |

### Recomendaciones de mejora al proceso QA → GH

- Ejemplo: estandarizar que todo reporte de QA incluya el ambiente y la versión antes de normalizarlo, para evitar el ciclo de "comentar solicitando datos faltantes" en cada ronda.
