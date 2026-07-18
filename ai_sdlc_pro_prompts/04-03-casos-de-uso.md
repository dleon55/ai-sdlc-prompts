# 4.3 — Diseño de casos de uso

## Descripción

Prompt para documentar formalmente los casos de uso del requerimiento o módulo analizado: actores, disparadores, flujos principal y alternos, reglas de negocio y criterios de aceptación.

**Cuándo usarlo:** durante la fase de diseño, para formalizar el comportamiento esperado del sistema antes de implementar.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | bajo — formaliza en documentación el comportamiento ya analizado, sin ejecutar cambios; el riesgo es que casos de uso incompletos (flujos alternos, criterios de aceptación) generen ambigüedad para la implementación y las pruebas posteriores |
| Entradas requeridas | análisis funcional previo (`02-01`), documentación existente de casos de uso, módulo o funcionalidad objetivo |
| Herramientas permitidas | lectura de documentación y código relacionado — sin ejecución ni cambios |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si faltan reglas de negocio, postcondiciones o criterios de aceptación verificables para un flujo, marcarlo como pendiente de validación funcional en vez de inventarlos |
| Salida esperada | ver `## Estructura de cada caso de uso` |
| Evidencia mínima | cada caso de uso debe incluir flujo principal, al menos un flujo alterno y criterios de aceptación verificables contra el análisis funcional citado |
| Siguiente prompt recomendado | `04-04-adr-decisiones-arquitectura` si hay decisiones de arquitectura pendientes derivadas de los casos de uso; `05-01-plan-implementacion` si el diseño ya está completo |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Documenta formalmente los casos de uso relacionados con el requerimiento o módulo analizado, a partir del análisis funcional previo (`02-01`).

Entradas:
- análisis funcional previo: [PEGAR O REFERENCIA A 02-01]
- documentación existente de casos de uso: [REFERENCIA O "ninguna"]
- módulo o funcionalidad objetivo: [MODULO]

Pasos:
1. Revisa el análisis funcional citado y la documentación existente de casos de uso para identificar qué comportamiento ya está definido y qué falta.
2. Para cada caso de uso, documenta: nombre, objetivo, actores, disparador, precondiciones, flujo principal, flujos alternos, postcondiciones, reglas de negocio, criterios de aceptación y componentes técnicos relacionados.
3. El flujo principal debe reflejar el camino feliz completo; los flujos alternos deben cubrir al menos las excepciones y variaciones ya mencionadas en el análisis funcional.
4. Verifica que cada criterio de aceptación sea verificable de forma objetiva (observable en el sistema), no una aspiración vaga.
5. Si para algún caso de uso faltan reglas de negocio, postcondiciones o criterios de aceptación verificables en el análisis funcional citado, no los inventes.

Restricciones:
- no completes un campo (postcondiciones, reglas de negocio, criterios de aceptación) inventando contenido plausible cuando el análisis funcional citado no lo especifica — márcalo explícitamente como "pendiente de validación funcional" en ese caso de uso,
- todo caso de uso debe incluir al menos un flujo alterno; si el análisis funcional no menciona ninguna excepción, señálalo como vacío a validar en vez de omitir la sección,
- no propongas cambios de arquitectura ni de implementación en este prompt — el objetivo es formalizar el comportamiento ya analizado, no diseñarlo o resolverlo,
- cita el análisis funcional o la documentación existente como fuente de cada regla de negocio o precondición no obvia; no las presentes como si fueran evidentes por sí mismas.

Salida:
- ver `## Estructura de cada caso de uso`
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de casos de uso y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- módulo: [MÓDULO O FUNCIONALIDAD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: análisis funcional, documentación existente de CU
- objetivo puntual de salida: casos de uso formales listos para revisión y validación
- nivel de profundidad: alto
```

---

## Estructura de cada caso de uso

| Campo | Contenido |
|---|---|
| Nombre | Nombre del caso de uso |
| Objetivo | Qué logra este caso de uso |
| Actores | Quién lo ejecuta o participa |
| Disparador | Qué evento o acción lo inicia |
| Precondiciones | Qué debe ser verdad antes de ejecutar |
| Flujo principal | Secuencia de pasos del camino feliz |
| Flujos alternos | Variaciones y excepciones |
| Postcondiciones | Estado del sistema al terminar |
| Reglas de negocio | Restricciones y validaciones aplicables |
| Criterios de aceptación | Cómo verificar que está correctamente implementado |
| Componentes técnicos | Módulos, servicios y tablas involucradas |
