# 2.7 — Matriz de trazabilidad de requerimientos del proyecto completo

## Descripción

Prompt para mantener una **matriz de trazabilidad agregada y viva** de todos los requerimientos de un proyecto: qué necesidad de negocio dio origen a cada requerimiento, y si ya tiene diseño, implementación y prueba vinculados. Complementa `08-02-cumplimiento-requerimiento`, que valida el cumplimiento de **un** issue puntual, no una vista agregada de todo el proyecto.

**Cuándo usarlo:** periódicamente durante la ejecución de un proyecto con múltiples requerimientos ya analizados (`02-05`), para detectar requerimientos huérfanos (sin diseño, código o prueba) o código sin requerimiento formal que lo respalde, antes de que el proyecto se dé por cerrado.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — una matriz desactualizada o incompleta da una falsa sensación de cobertura completa cuando en realidad hay requerimientos sin diseño/implementación/prueba, o funcionalidad construida sin respaldo formal; el prompt no ejecuta ni modifica nada por sí mismo |
| Entradas requeridas | lista de requerimientos de negocio del proyecto (o issues ya analizados con `02-05`), diseños asociados, PRs/implementaciones relacionadas, resultados de prueba disponibles |
| Herramientas permitidas | lectura de issues, diseños, código y resultados de prueba existentes — sin ejecutar pruebas nuevas ni modificar nada |
| Autonomía permitida | A0 — Analizar (agregar trazabilidad ya evidenciable); A1 — Proponer (marcar huecos y priorizarlos) |
| Criterios de detención | si un requerimiento no puede vincularse a ninguna evidencia de diseño, código o prueba, no lo marques como "cubierto" — repórtalo explícitamente como huérfano |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada requerimiento del proyecto aparece exactamente una vez en la matriz con su estado de cobertura citado en cada etapa (requerimiento → diseño → implementación → prueba) |
| Siguiente prompt recomendado | `08-02-cumplimiento-requerimiento` para profundizar en un requerimiento específico marcado como incompleto o huérfano |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Construye y mantén la matriz de trazabilidad agregada de todos los requerimientos del proyecto: vínculo entre cada requerimiento y su diseño, implementación y prueba, identificando huérfanos en cualquier etapa.

Entradas:
- requerimientos de negocio del proyecto: [PEGAR LISTA O REFERENCIA A 02-05]
- diseños asociados: [PEGAR O REFERENCIA]
- implementaciones/PRs relacionados: [PEGAR O REFERENCIA]
- resultados de prueba disponibles: [PEGAR O REFERENCIA, O "no disponibles aún"]

Actividades:
1. INVENTARIO DE REQUERIMIENTOS
   Lista todos los requerimientos de negocio conocidos del proyecto, con su identificador y una descripción breve.

2. VINCULACIÓN A DISEÑO
   Para cada requerimiento, verifica si existe un diseño (`04-01` u otro artefacto de diseño) que lo cubra explícitamente. Cita la referencia concreta, no asumas cobertura por similitud.

3. VINCULACIÓN A IMPLEMENTACIÓN
   Para cada requerimiento, verifica si existe código o un PR que lo implemente. Cita la referencia concreta (commit, PR, archivo).

4. VINCULACIÓN A PRUEBA
   Para cada requerimiento, verifica si existe evidencia de prueba real — la ausencia de prueba es una brecha aunque el código "se vea correcto".

5. IDENTIFICACIÓN DE HUÉRFANOS
   Señala explícitamente cada requerimiento que carece de vínculo en alguna etapa (diseño, implementación o prueba) — distingue "aún no implementado" (esperado en un proyecto en curso) de "huérfano sin trazabilidad" (una brecha real que requiere atención).

6. IDENTIFICACIÓN DE CÓDIGO HUÉRFANO
   Señala funcionalidad implementada que no tiene ningún requerimiento formal vinculado — es una señal de scope creep o de un requerimiento que nunca se documentó formalmente, y debe reportarse, no omitirse.

Restricciones:
- nunca marques un requerimiento como "cubierto" en una etapa sin una referencia concreta citada (diseño, PR, o resultado de prueba específico) — la cobertura sin evidencia se reporta como no verificable,
- distingue siempre "no implementado todavía" (normal en un proyecto en curso, con fecha esperada si se conoce) de "huérfano sin trazabilidad" (brecha real que requiere una acción),
- no ignores ni omitas código o funcionalidad que no tiene requerimiento formal vinculado — repórtalo explícitamente en vez de asumir que está bien documentado en otro lugar,
- si la lista de requerimientos de negocio del proyecto está incompleta o no existe, detente y solicítala antes de construir la matriz sobre supuestos.

Salida:
0. Bloque JSON de metadatos (claves: status, requirement_count, orphan_requirements_count, orphan_code_count, confidence_score [0.0 a 1.0]).
1. Matriz de trazabilidad completa: Requerimiento | Diseño | Implementación | Prueba | Estado
2. Requerimientos huérfanos (sin cobertura completa), con la etapa donde se rompe la trazabilidad.
3. Código o funcionalidad sin requerimiento formal vinculado.
4. Recomendaciones priorizadas para cerrar los huecos detectados.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de matriz de trazabilidad de requerimientos y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- requerimientos de negocio: [PEGAR LISTA O REFERENCIA A 02-05]
- documentos a revisar: diseños, PRs/implementaciones, resultados de prueba
- objetivo puntual de salida: matriz de trazabilidad completa con huérfanos identificados
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de cobertura |
| Matriz de trazabilidad (1) | Todos los requerimientos con su estado en cada etapa, con referencias citadas |
| Requerimientos huérfanos (2) | Lista con la etapa exacta donde se rompe la trazabilidad |
| Código huérfano (3) | Funcionalidad implementada sin requerimiento formal vinculado |
| Recomendaciones (4) | Acciones priorizadas para cerrar los huecos |

### Ejemplo (fragmento)

```json
{
  "status": "matriz_con_huerfanos",
  "requirement_count": 24,
  "orphan_requirements_count": 3,
  "orphan_code_count": 1,
  "confidence_score": 0.74
}
```

| Requerimiento | Diseño | Implementación | Prueba | Estado |
|---|---|---|---|---|
| RN-014 Exportar reporte filtrado a CSV | `04-01` sección 3.2 | PR #482 | Sin evidencia de prueba con filtro aplicado | Huérfano en prueba |
| RN-015 Notificación por email al cerrar ticket | No hay diseño formal encontrado | PR #501 (implementado) | Test unitario `test_email_on_close` | Huérfano en diseño — implementado sin diseño formal previo |

| Sección | Ejemplo de contenido |
|---|---|
| Código huérfano (3) | Endpoint `POST /reports/schedule` (envío programado de reportes) implementado en PR #495, sin ningún requerimiento de negocio vinculado en el backlog — posible scope creep o requerimiento verbal nunca documentado; requiere retro-documentar el requerimiento o justificar su remoción |
