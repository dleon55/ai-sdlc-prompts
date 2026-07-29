# 0-D.3 — Plan de trabajo del proyecto: cronograma, EDT y asignación de recursos

## Descripción

Prompt para elaborar el **plan de trabajo de todo el proyecto**: estructura de desglose del trabajo (EDT/WBS), estimación por fase o entregable, dependencias, cronograma con ruta crítica y asignación de recursos. Es el plan a nivel de proyecto completo — distinto de `05-01-plan-implementacion`, que planifica la ejecución de un cambio o feature ya diseñado dentro de un componente existente.

**Cuándo usarlo:** después de aprobar el Project Charter (`00-D-01`) y, si ya existe, el stack/arquitectura inicial (`00-D-02`) — antes de iniciar la ejecución del proyecto, para tener un cronograma y una asignación de recursos que el equipo o patrocinador pueda aprobar.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | alto — el cronograma y la asignación de recursos resultantes condicionan compromisos de fecha ante el patrocinador y la carga de trabajo del equipo; una estimación optimista o una sobreasignación de recursos no detectada se descubre típicamente tarde, cuando ya es costosa de corregir |
| Entradas requeridas | Project Charter aprobado (`00-D-01`), alcance y entregables principales, equipo disponible (roles, capacidad, calendario), fecha límite o ventana objetivo si existe, dependencias externas conocidas (otros equipos, proveedores, aprobaciones) |
| Herramientas permitidas | ninguna de ejecución — el prompt produce un documento de planeación (EDT, cronograma, tabla de asignación); no crea issues, milestones ni eventos de calendario reales |
| Autonomía permitida | A1 — Proponer (cronograma y asignación de recursos quedan marcados como propuesta hasta aprobación del patrocinador o equipo) |
| Criterios de detención | si la fecha límite declarada no es alcanzable con el equipo y alcance dados, no ajustar las estimaciones para que "encajen" — reportarlo explícitamente como conflicto con las opciones de trade-off; si falta información de capacidad del equipo, detener y solicitarla antes de asignar recursos |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada entregable de la EDT tiene estimación con método declarado, cada dependencia entre entregables está listada, la ruta crítica está identificada explícitamente, y cualquier sobreasignación de un recurso queda señalada con la fila y el recurso afectado |
| Siguiente prompt recomendado | `05-02-riesgos-implementacion` para profundizar en riesgos de ejecución del cronograma; `05-01-plan-implementacion` cuando cada entregable de la EDT entre a su fase de diseño/implementación individual |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Elabora el plan de trabajo completo del proyecto: estructura de desglose del trabajo (EDT/WBS), estimación, dependencias, cronograma con ruta crítica y asignación de recursos.

Entradas:
- Project Charter aprobado: [PEGAR O REFERENCIA A 00-D-01]
- alcance y entregables principales: [LISTA O DESCRIPCIÓN]
- equipo disponible: [ROLES, CAPACIDAD POR PERSONA (horas/semana), CALENDARIO/AUSENCIAS CONOCIDAS]
- fecha límite o ventana objetivo: [FECHA O "no declarada aún"]
- dependencias externas conocidas: [OTROS EQUIPOS, PROVEEDORES, APROBACIONES REQUERIDAS, O "ninguna declarada"]

Actividades:
1. ESTRUCTURA DE DESGLOSE DEL TRABAJO (EDT/WBS)
   Descompón el alcance en entregables y, dentro de cada entregable, en paquetes de trabajo lo bastante pequeños para estimar con confianza (regla general: ningún paquete debe exceder ~2 semanas de esfuerzo; si lo excede, descompónlo más). Cada paquete de trabajo debe tener un responsable único identificable (rol, no necesariamente persona nombrada).

2. ESTIMACIÓN
   Para cada paquete de trabajo, estima el esfuerzo con un método declarado explícitamente (analogía con trabajo similar previo, juicio experto, descomposición PERT de tres puntos, u otro) — nunca presentes una cifra sin indicar de dónde sale. Declara el nivel de confianza de cada estimación (alto/medio/bajo) según la información disponible al momento de estimar.

3. DEPENDENCIAS
   Identifica dependencias entre paquetes de trabajo (secuenciales, de recursos compartidos, externas) y clasifícalas por tipo. Señala explícitamente las dependencias externas (fuera del control directo del equipo) porque son las de mayor riesgo para el cronograma.

4. CRONOGRAMA Y RUTA CRÍTICA
   A partir de las estimaciones y dependencias, construye el cronograma y calcula la ruta crítica (la secuencia de paquetes de trabajo que determina la duración mínima del proyecto). Señala explícitamente cuánta holgura (slack) tiene cada paquete fuera de la ruta crítica.

5. ASIGNACIÓN DE RECURSOS
   Asigna cada paquete de trabajo a un rol o persona según la capacidad declarada. Detecta y señala explícitamente cualquier sobreasignación (un recurso comprometido más allá de su capacidad declarada en una misma ventana de tiempo) — no la resuelvas por tu cuenta reasignando o recortando alcance sin indicarlo como una decisión pendiente.

6. VALIDACIÓN CONTRA FECHA LÍMITE
   Si existe una fecha límite u objetivo declarado, compárala contra la fecha resultante del cronograma. Si el cronograma no alcanza la fecha, no comprimas las estimaciones para forzar que encaje — presenta las opciones reales de trade-off (reducir alcance, sumar recursos, extender fecha, aceptar el riesgo de comprimir sin margen) para que el patrocinador decida.

Restricciones:
- nunca ajustes una estimación a la baja únicamente para que el cronograma alcance una fecha límite declarada — si hay una brecha, repórtala explícitamente con las opciones de trade-off, no la ocultes comprimiendo números,
- todo paquete de trabajo debe declarar el método de estimación usado y su nivel de confianza — una estimación sin método declarado se reporta como "estimación no verificable", no como cifra definitiva,
- no asignes un recurso por encima de su capacidad declarada sin señalarlo explícitamente como sobreasignación — nunca lo dejes implícito en la tabla de asignación,
- si falta información de capacidad del equipo o de alcance para poder planear con confianza, detente y solicita la información faltante en vez de asumir una capacidad o un alcance no declarados.

Salida:
0. Bloque JSON de metadatos (claves: status, work_package_count, critical_path_duration_days, overallocated_resources_count, confidence_score [0.0 a 1.0]).
1. EDT/WBS: Entregable | Paquete de trabajo | Responsable (rol) | Estimación | Método de estimación | Confianza
2. Dependencias: Paquete de trabajo | Depende de | Tipo de dependencia | Riesgo si se retrasa
3. Cronograma con ruta crítica: Paquete de trabajo | Inicio | Fin | ¿En ruta crítica? | Holgura
4. Asignación de recursos: Recurso (rol/persona) | Paquetes asignados | Carga total vs. capacidad | ¿Sobreasignado?
5. Validación contra fecha límite: fecha resultante del cronograma, brecha contra la fecha objetivo (si existe), opciones de trade-off si hay brecha.
6. Supuestos y vacíos de información pendientes de confirmar antes de aprobar el plan.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan de trabajo del proyecto y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- Project Charter: [REFERENCIA A 00-D-01]
- alcance y entregables principales: [LISTA]
- equipo disponible: [ROLES Y CAPACIDAD]
- documentos a revisar: Project Charter, arquitectura inicial (00-D-02) si existe
- objetivo puntual de salida: EDT, cronograma con ruta crítica y asignación de recursos
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del plan |
| EDT/WBS (1) | Tabla completa de entregables y paquetes de trabajo con estimación y método |
| Dependencias (2) | Todas las dependencias relevantes, con las externas señaladas explícitamente |
| Cronograma y ruta crítica (3) | Fechas por paquete, ruta crítica identificada, holgura de cada paquete fuera de ella |
| Asignación de recursos (4) | Carga por recurso vs. capacidad, con sobreasignaciones señaladas |
| Validación contra fecha límite (5) | Comparación explícita contra la fecha objetivo, con opciones de trade-off si hay brecha |
| Supuestos y vacíos (6) | Información pendiente de confirmar antes de aprobar el plan |

### Ejemplo (fragmento)

```json
{
  "status": "planeado_con_brecha",
  "work_package_count": 14,
  "critical_path_duration_days": 42,
  "overallocated_resources_count": 1,
  "confidence_score": 0.68
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Asignación de recursos (4) | Dev backend (1 persona, 30h/semana) \| 5 paquetes asignados en semanas 3-6 \| 38h/semana promedio vs. 30h/semana de capacidad \| Sí — sobreasignado en semana 4 |
| Validación contra fecha límite (5) | Fecha objetivo declarada: 15 de septiembre. Fecha resultante del cronograma: 29 de septiembre (brecha de 2 semanas). Opciones: (a) sumar un segundo dev backend desde la semana 3, (b) recortar el entregable de reportes avanzados a una fase 2, (c) aceptar la fecha del 29 de septiembre |
