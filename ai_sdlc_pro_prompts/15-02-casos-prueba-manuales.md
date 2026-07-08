# 15.2 — Diseño de casos de prueba manuales y funcionales

## Descripción

Prompt para testers y QAs funcionales. Permite diseñar casos de prueba manuales detallados (paso a paso, datos de prueba, resultados esperados) a partir de historias de usuario o especificaciones funcionales sin requerir conocimientos de programación.

**Cuándo usarlo:** al planificar la fase de pruebas de una funcionalidad, antes de iniciar pruebas exploratorias o manuales.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — genera una matriz de casos de prueba como documentación, no ejecuta pruebas ni modifica código; un caso de borde omitido puede dejar un escenario sin cobertura de QA |
| Entradas requeridas | historia de usuario o requerimiento a validar, criterios de aceptación o reglas de negocio si existen (idealmente de `15-01`) |
| Herramientas permitidas | ninguna ejecución ni acceso a sistemas — solo redacción de la matriz de casos de prueba a partir de la información provista |
| Autonomía permitida | A1 — Proponer la suite de casos de prueba manuales como artefacto listo para ejecución por QA |
| Criterios de detención | no inventar reglas de negocio o comportamientos del sistema no descritos en el requerimiento; si faltan criterios de aceptación, señalarlo y limitar la cobertura a lo verificable con la información disponible |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada caso de prueba incluye ID, precondición, pasos de ejecución, datos de prueba y resultado esperado verificable; la suite cubre camino feliz, alterno, negativo y al menos un caso de borde |
| Siguiente prompt recomendado | `07-05-automatizacion-antigravity` para automatizar los casos críticos de la suite; `07-03-pruebas-e2e` si se requiere diseño de pruebas end-to-end formales |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un QA Tester Funcional. Genera una suite de casos de prueba manuales detallados para validar funcionalmente el requerimiento o la historia de usuario adjunta.

Entradas:
- historia de usuario o requerimiento: [PEGAR]
- criterios de aceptación o reglas de negocio: [PEGAR SI APLICA]

Actividades:
1. Analiza los flujos de usuario descritos en la funcionalidad.
2. Identifica los escenarios principales de prueba:
   - camino feliz (happy path),
   - escenarios alternos,
   - caminos de validación o error (negativos),
   - casos de borde (valores límite, campos vacíos, etc.).
3. Describe detalladamente cada caso de prueba en una estructura tabular.
4. Por cada caso de prueba especifica:
   - ID del caso de prueba,
   - título corto descriptivo,
   - precondición (estado previo del sistema),
   - pasos de ejecución (acciones secuenciales),
   - datos de prueba sugeridos (entradas específicas),
   - resultado esperado (comportamiento correcto observable).

Salida:
Presenta una tabla estructurada con los siguientes campos por cada caso de prueba:
| ID | Título | Precondición | Pasos de Ejecución | Datos de Entrada | Resultado Esperado |
```

---

## Uso con fórmula estándar

```text
Usa el prompt de casos de prueba manuales y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA FUNCIONAL]
- rama: main
- ambiente: QA
- componentes: módulo de checkout
- documentos a revisar: historias de usuario, reglas de negocio
- objetivo puntual de salida: matriz completa de casos de prueba manuales paso a paso
- nivel de profundidad: alto
```

---

## Salida esperada

Una tabla clara con casos de prueba numerados cubriendo flujos exitosos y de error:

| ID | Título | Precondición | Pasos de Ejecución | Datos de Entrada | Resultado Esperado |
|---|---|---|---|---|---|
| TC-01 | Login Exitoso | Usuario registrado existe | 1. Ir a login<br>2. Ingresar credenciales<br>3. Click en entrar | User: admin<br>Pass: admin123 | Redirección a Home y banner de bienvenida visible |
| TC-02 | Login con contraseña inválida | Usuario registrado existe | 1. Ir a login<br>2. Ingresar contraseña incorrecta<br>3. Click en entrar | User: admin<br>Pass: wrongpass | Mensaje de error "Contraseña incorrecta" y permanece en login |
