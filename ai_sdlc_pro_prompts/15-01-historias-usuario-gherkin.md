# 15.1 — Historias de usuario y criterios de aceptación Gherkin

## Descripción

Prompt para analistas de negocio y product owners. Convierte requerimientos y solicitudes abstractas en historias de usuario estructuradas e incorpora criterios de aceptación con formato Gherkin (Dado / Cuando / Entonces).

**Cuándo usarlo:** al definir requerimientos de negocio detallados, antes del diseño técnico o arquitectura.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — genera documentación de requerimientos, no modifica código; una historia o criterio de aceptación mal definido puede propagar errores al diseño técnico y a las pruebas aguas abajo |
| Entradas requeridas | requerimiento o solicitud de negocio a convertir, módulo o proceso afectado, estándar de compliance aplicable si existe (ISO 29110 / MOPROSOFT) |
| Herramientas permitidas | ninguna ejecución ni acceso a sistemas — solo redacción de historias de usuario y criterios Gherkin a partir de la información provista |
| Autonomía permitida | A1 — Proponer las historias de usuario y criterios de aceptación como artefacto de documentación |
| Criterios de detención | no inventar reglas de negocio, roles o flujos que no estén implícitos en la solicitud original; si el requerimiento es ambiguo, señalar los supuestos usados en vez de asumir silenciosamente |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada historia de usuario tiene al menos un criterio de aceptación en formato Gherkin para el flujo feliz y uno para un flujo alterno o de error |
| Siguiente prompt recomendado | `04-01-diseno-solucion` para el diseño técnico basado en estas historias; `15-02-casos-prueba-manuales` para derivar los casos de prueba correspondientes |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como un Business Analyst & Product Owner Senior. Convierte la descripción funcional o requerimiento de negocio adjunto en historias de usuario detalladas con sus respectivos criterios de aceptación estructurados en formato Gherkin.

Entradas:
- requerimiento o solicitud de negocio: [PEGAR]
- módulo o proceso afectado: [MODULO]
- estándar/compliance: [NINGUNO / ISO 29110 / MOPROSOFT]

Actividades:
1. Analiza la solicitud de negocio e identifica los objetivos principales.
2. Identifica:
   - los roles de usuario (actores) involucrados,
   - la necesidad funcional (el "qué"),
   - el valor de negocio (el "para qué").
3. Escribe las historias de usuario bajo el estándar clásico: "Como [Rol], quiero [Acción], para [Beneficio]".
4. Escribe criterios de aceptación detallados en formato Gherkin:
   - escenario: descripción del caso,
   - Dado [Contexto o precondición],
   - Cuando [Acción o evento disparador],
   - Entonces [Resultado esperado o comportamiento del sistema].
5. Especifica las reglas de negocio críticas, flujos alternos e indicaciones especiales de experiencia de usuario (UX).

Restricciones:
- no inventes criterios de aceptación, reglas de negocio ni roles que el requerimiento original no mencione explícita o implícitamente; si falta información para completar un escenario, decláralo como supuesto en vez de rellenarlo por tu cuenta,
- señala explícitamente cualquier enunciado ambiguo tipo "debería" o "el sistema debe permitir" que no especifique un comportamiento verificable, y propone la aclaración concreta necesaria en vez de interpretarlo a tu criterio,
- cada escenario Gherkin debe ser independiente y autocontenido: no asumas estado compartido implícito entre escenarios (por ejemplo, que el escenario 2 dependa de datos dejados por el escenario 1) — cada "Dado" debe establecer su propio contexto completo,
- si una historia requiere validar más de una regla de negocio, sepáralas en escenarios Gherkin distintos en vez de mezclarlas en un solo "Cuando/Entonces".

Salida:
1. Historias de usuario (formato estándar)
2. Criterios de aceptación (formato Gherkin para flujos feliz, alternos e inválidos)
3. Reglas de negocio e implicaciones funcionales
4. Consideraciones de diseño UI/UX (accesibilidad, validación visual)
```

---

## Uso con fórmula estándar

```text
Usa el prompt de historias de usuario y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [PEGAR REQUERIMIENTO FUNCIONAL]
- rama: main
- ambiente: DEV
- componentes: modulo de registro
- documentos a revisar: reglas de negocio, mockups
- objetivo puntual de salida: historias de usuario detalladas con criterios de aceptación Gherkin
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Historia de usuario | "Como [Usuario], quiero [Funcionalidad], para [Valor]" |
| Criterios Gherkin | Dado / Cuando / Entonces de escenarios exitosos y fallidos |
| Reglas de negocio | Restricciones de validación, límites de negocio y políticas |
| Consideraciones UI/UX | Requisitos visuales, accesibilidad y comportamiento de componentes |

### Ejemplo aplicado: inicio de sesión de un cliente registrado

**Historia de usuario:** "Como cliente registrado, quiero iniciar sesión con mi correo y contraseña, para acceder a mi cuenta y continuar mi compra."

| Escenario | Dado | Cuando | Entonces |
|---|---|---|---|
| Inicio de sesión exitoso | el usuario está registrado y cuenta con credenciales válidas | ingresa su correo y contraseña correctos y presiona "Iniciar sesión" | el sistema lo redirige a su panel de cuenta y muestra un mensaje de bienvenida |
| Contraseña incorrecta | el usuario está registrado | ingresa su correo correcto pero una contraseña incorrecta y presiona "Iniciar sesión" | el sistema muestra "Correo o contraseña incorrectos" y permanece en la pantalla de login sin cerrar la sesión de nadie más |

**Supuesto declarado:** el requerimiento original no especifica un límite de intentos fallidos antes de bloquear la cuenta; se señala como pendiente de confirmación con el stakeholder en vez de asumir un valor.
