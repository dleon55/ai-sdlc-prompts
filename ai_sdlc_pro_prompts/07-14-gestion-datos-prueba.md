# 7.14 — Estrategia de gestión de datos de prueba en QA

## Descripción

Prompt para diseñar la estrategia transversal de datos de prueba en ambientes de QA/staging compartidos: generación de datasets sintéticos representativos o enmascarado de un snapshot de producción, volumen necesario para representatividad, mecanismo de aislamiento entre ejecuciones paralelas, y política de refresco/reset del ambiente. Distinto de los datos de prueba puntuales por escenario que ya cubren `07-01`/`07-02`/etc. — este prompt diseña la estrategia completa de datos del ambiente, no de un flujo individual.

**Cuándo usarlo:** al configurar un ambiente de QA/staging compartido nuevo, o cuando aparecen fallas de pruebas por datos inconsistentes/contaminados entre corridas o por colisión entre ejecuciones paralelas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — un enmascarado de datos productivos mal diseñado puede filtrar datos sensibles reales a un ambiente de menor seguridad; una estrategia de reset mal diseñada puede corromper el estado de otros equipos que comparten el ambiente |
| Entradas requeridas | ambiente(s) de prueba a cubrir, origen del dataset (sintético / snapshot de producción enmascarado / mixto), volumen de datos necesario para representatividad, cantidad de pipelines/agentes ejecutando en paralelo, política de compliance aplicable a los datos (PII, PCI u otra, si aplica) |
| Herramientas permitidas | lectura de esquemas, scripts de seed/fixture existentes y políticas de datos; el prompt diseña la estrategia y genera scripts de generación/enmascarado — la ejecución contra un ambiente compartido real requiere aprobación explícita, y nunca contra producción |
| Autonomía permitida | A1 — Proponer (estrategia y scripts); A2 — Ejecutar controlado solo en el ambiente de prueba aislado indicado, nunca contra producción ni contra un ambiente compartido sin aprobación explícita |
| Criterios de detención | detener si se pide partir de un snapshot de producción sin una política de enmascarado de PII/datos sensibles ya definida — no diseñar el enmascarado por cuenta propia sin esa política; detener si no se puede confirmar el volumen de datos necesario para que las pruebas sean representativas |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada campo sensible identificado en el dataset tiene una estrategia de enmascarado explícita (nunca "se deja igual" sin justificación); el mecanismo de aislamiento entre corridas paralelas se describe en términos concretos (namespacing, transacciones, contenedores efímeros) |
| Siguiente prompt recomendado | `07-01`/`07-02`/`07-03` para el diseño de pruebas específicas que consumen estos datos; `13-08-gestion-secretos-credenciales` si la estrategia requiere credenciales de acceso a producción para el snapshot inicial |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estrategia de gestión de datos de prueba para el/los ambiente(s) de QA indicados: generación o enmascarado del dataset base, mecanismo de aislamiento entre ejecuciones paralelas, y política de refresco/reset del entorno.

Entradas:
- ambiente(s) a cubrir: [QA / STAGING / AMBOS]
- origen del dataset base: [100% SINTÉTICO / SNAPSHOT DE PRODUCCIÓN ENMASCARADO / MIXTO]
- volumen de datos necesario: [ej. N REGISTROS POR ENTIDAD PRINCIPAL PARA REPRESENTATIVIDAD]
- pipelines/agentes ejecutando en paralelo: [NÚMERO O "desconocido"]
- política de compliance aplicable a los datos: [PII / PCI / NINGUNA CONOCIDA / OTRA]
- stack de base de datos: [STACK]

Pasos:
1. CLASIFICACIÓN DE CAMPOS SENSIBLES
   Si el dataset parte de un snapshot de producción, identifica todos los campos que contienen o pueden contener PII u otros datos sensibles según la política de compliance provista (nombres, emails, teléfonos, direcciones, datos de pago, identificadores gubernamentales). Si no se proveyó una política de compliance y se pide partir de producción, detente y solicítala antes de diseñar el enmascarado.

2. ESTRATEGIA DE ENMASCARADO O GENERACIÓN SINTÉTICA
   Para cada campo sensible, define la técnica de enmascarado (sustitución determinista, hashing, generación sintética preservando el formato) de forma que el dato deje de ser identificable pero mantenga la forma o distribución estadística necesaria para que las pruebas sigan siendo representativas (ej. mismo rango de fechas relativo, misma distribución de códigos postales).

3. VOLUMEN Y REPRESENTATIVIDAD
   Define cuántos registros por entidad principal se necesitan para que las pruebas de performance/carga y los casos de borde (paginación, ordenamiento, agregaciones) sean representativos, y cómo generar los casos de borde específicos (valores nulos, límites de longitud, caracteres especiales) que un dataset real no necesariamente cubre.

4. AISLAMIENTO ENTRE EJECUCIONES PARALELAS
   Si múltiples pipelines o agentes ejecutan pruebas sobre el mismo ambiente compartido, diseña el mecanismo de aislamiento: namespacing de datos por ejecución (prefijos o sufijos únicos), transacciones que se revierten al final de cada corrida, o contenedores/bases de datos efímeras por ejecución. Señala explícitamente el riesgo de colisión si no se implementa ninguno de estos mecanismos.

5. POLÍTICA DE REFRESCO Y RESET
   Define cuándo y cómo se refresca el dataset base (periodicidad, disparador manual o automático) y el procedimiento de reset a un estado limpio conocido entre ejecuciones o al final del día, incluyendo qué hacer si el reset afecta a otros equipos que comparten el ambiente.

6. VALIDACIÓN DE INTEGRIDAD
   Define cómo verificar, antes de cada corrida, que el dataset está en el estado esperado (no corrompido por una corrida anterior fallida) y qué hacer si la validación falla.

Restricciones:
- nunca propongas usar datos reales de producción sin enmascarar en un ambiente de menor seguridad (QA/staging) — si el origen es un snapshot de producción, todo campo sensible debe tener una estrategia de enmascarado explícita antes de proponer el uso del dataset,
- si no hay política de compliance provista y el dataset parte de producción, detente y solicita la política en vez de decidir por tu cuenta qué campos enmascarar,
- no ejecutes el enmascarado ni la carga del dataset contra un ambiente compartido real sin aprobación explícita, y nunca contra producción,
- todo mecanismo de aislamiento entre ejecuciones paralelas debe describirse en términos concretos e implementables, nunca como "asegurar que no haya colisión" sin especificar cómo,
- si el volumen de datos necesario para representatividad no puede confirmarse, decláralo como pendiente en vez de asumir un número arbitrario.

Salida:
- estrategia de origen del dataset (sintético/enmascarado/mixto), con justificación
- tabla de campos sensibles y su técnica de enmascarado, si aplica
- volumen de datos recomendado por entidad y casos de borde a generar
- mecanismo de aislamiento entre ejecuciones paralelas
- política de refresco/reset del ambiente
- procedimiento de validación de integridad pre-corrida
```

---

## Uso con fórmula estándar

```text
Usa el prompt de gestión de datos de prueba en QA y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- ambiente(s): [QA / STAGING / AMBOS]
- origen del dataset: [SINTÉTICO / SNAPSHOT ENMASCARADO / MIXTO]
- volumen necesario: [N REGISTROS POR ENTIDAD]
- ejecuciones paralelas: [NÚMERO O "desconocido"]
- política de compliance: [PII / PCI / NINGUNA CONOCIDA]
- documentos a revisar: esquemas de BD, scripts de seed existentes, política de datos
- objetivo puntual de salida: estrategia completa de datos de prueba para el ambiente
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Origen del dataset | Sintético, enmascarado o mixto, con justificación |
| Campos sensibles | Tabla de campo → técnica de enmascarado aplicada |
| Volumen y casos de borde | Registros por entidad y casos de borde a generar |
| Aislamiento paralelo | Mecanismo concreto (namespacing, transacciones, contenedores efímeros) |
| Refresco/reset | Periodicidad, disparador y procedimiento de reset |
| Validación de integridad | Chequeo pre-corrida y acción si falla |

### Ejemplo (fragmento)

| Campo sensible | Técnica de enmascarado |
|---|---|
| `email` | Sustitución determinista: hash del email original mapeado a `user_{hash}@test.example` — mismo email original siempre produce el mismo valor enmascarado, preservando unicidad para pruebas de duplicados |
| `fecha_nacimiento` | Se conserva el año, se aleatoriza mes/día — preserva distribución de edades para pruebas de segmentación sin exponer la fecha real |
| `numero_tarjeta` | Reemplazado por números de prueba válidos del esquema de la pasarela de pago (nunca un PAN real, ni siquiera enmascarado) |

**Aislamiento entre ejecuciones paralelas:** cada pipeline de CI antepone un prefijo único (`run_{build_id}_`) a los registros que crea, y ejecuta su suite dentro de una transacción que se revierte al finalizar — evita que dos ejecuciones concurrentes vean o modifiquen los registros de la otra.
