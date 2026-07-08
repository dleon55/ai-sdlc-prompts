# 4.1 — Diseño funcional y técnico de solución

## Descripción

Prompt para diseñar la solución completa antes de implementar: objetivo, alcance, supuestos, restricciones, cambios por componente, riesgos, dependencias, estrategia de validación y rollback.

**Cuándo usarlo:** una vez completado el análisis funcional, técnico y de impacto, antes de planificar o ejecutar cualquier cambio.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — el diseño resultante guía directamente la implementación; un diseño incompleto en riesgos o estrategia de rollback puede llevar a una implementación insegura o sin plan de reversión, aunque este prompt no ejecuta cambios |
| Entradas requeridas | análisis funcional, técnico y de impacto cruzado ya completados (`02-01`, `02-02`, `02-03`), arquitectura y contratos existentes |
| Herramientas permitidas | lectura de código, arquitectura y documentación — sin ejecución ni cambios; el resultado es un documento de diseño, no código |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no existe una estrategia de rollback viable para un componente crítico, declararlo como riesgo abierto en el diseño en vez de omitirlo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada cambio propuesto por componente debe estar vinculado a un riesgo y su mitigación, y a los hallazgos del análisis previo citado |
| Siguiente prompt recomendado | `05-01-plan-implementacion` |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña una solución completa, funcional y técnica, para el requerimiento o incidente analizado.

Pasos:
1. Define el objetivo de la solución: qué problema resuelve, para quién y qué resultado observable confirma que quedó resuelto — sin un objetivo verificable no hay forma de validar el diseño después.
2. Define el alcance: qué queda dentro y qué queda explícitamente fuera, para evitar que la implementación se expanda sin control o deje huecos sin cubrir.
3. Documenta los supuestos sobre los que se apoya el diseño (datos disponibles, comportamiento de terceros, infraestructura existente); si algún supuesto resulta falso, el diseño debe declararse inválido en vez de ajustarse silenciosamente durante la implementación.
4. Documenta las restricciones técnicas, de negocio, de tiempo o de compatibilidad que limitan las opciones de diseño.
5. Lista los casos de uso impactados y cómo cambia su comportamiento, citando los hallazgos del análisis funcional (`02-01`) que los sustentan.
6. Lista las reglas de negocio nuevas o modificadas, citando el análisis técnico y de impacto cruzado (`02-02`/`02-03`) correspondiente.
7. Detalla los cambios requeridos por componente: qué cambia, por qué ese componente es el punto correcto de intervención y qué contratos existentes (APIs, esquemas, formatos de archivo) se ven afectados.
8. Identifica los riesgos del diseño y, para cada uno, una mitigación concreta — prioriza los riesgos sobre componentes críticos o sin estrategia de rollback clara antes que riesgos menores o cosméticos.
9. Lista las dependencias entre componentes y con sistemas externos, señalando cuáles bloquean el orden de implementación.
10. Define la estrategia de validación: cómo se comprobará, con evidencia concreta, que la solución cumple el objetivo antes de darla por lista.
11. Define la estrategia de rollback por cada componente crítico; si no existe una estrategia viable, decláralo como riesgo abierto en el diseño en vez de omitirlo.

Restricciones:
- este prompt produce únicamente un documento de diseño: no propongas comandos a ejecutar ni modifiques código, configuración o infraestructura,
- cada cambio propuesto por componente debe quedar vinculado explícitamente a un riesgo, su mitigación y al hallazgo del análisis previo (02-01/02-02/02-03) que lo justifica — no incluyas cambios sin esa trazabilidad,
- si no existe una estrategia de rollback viable para un componente crítico, decláralo como riesgo abierto en vez de inventar una o de omitirlo,
- si el análisis funcional, técnico o de impacto cruzado previo no está disponible o está incompleto, detente y solicítalo antes de diseñar — no rellenes esos vacíos con suposiciones,
- si una decisión de diseño contradice la arquitectura o los contratos existentes, señálalo explícitamente como una desviación a validar, no la presentes como un hecho consumado.

Formato de salida:
1. Resumen de diseño
2. Diseño funcional
3. Diseño técnico
4. Componentes afectados
5. Riesgos y mitigaciones
6. Recomendación de implementación
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de solución y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: análisis previo, arquitectura, contratos
- objetivo puntual de salida: diseño completo con riesgos y estrategia de rollback
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen de diseño | Descripción ejecutiva de la solución |
| Diseño funcional | Cambios en flujos, reglas y casos de uso |
| Diseño técnico | Componentes, contratos, cambios por módulo |
| Componentes afectados | Lista precisa con tipo de cambio |
| Riesgos y mitigaciones | Riesgos identificados con plan de mitigación |
| Recomendación | Orden y prioridad de implementación |

### Ejemplo aplicado: validación automática de paridad ES/EN en el build

**Componentes afectados**

| Componente | Tipo de cambio | Descripción |
|---|---|---|
| `build.py` | Modificación | Agregar un paso `check_i18n_parity()` que compare la estructura de encabezados (`##`) de cada `.md` con su par `.en.md` antes de generar `index.html` |
| `tests/test_i18n.py` | Modificación | Sumar casos de prueba para el nuevo validador de paridad de secciones |

**Riesgos y mitigaciones**

| Riesgo | Mitigación |
|---|---|
| Falsos positivos por diferencias menores de formato (espacios, saltos de línea) entre el `.md` y su `.en.md` | Normalizar espacios en blanco antes de comparar la estructura de encabezados |
| El validador bloquea el build en PRs legítimos que traducen un archivo de forma incremental | Permitir una excepción explícita y documentada mientras el PR esté marcado como traducción en curso |
