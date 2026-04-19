# 13.4 — Modelado de amenazas (Threat Modeling)

## Descripción

Prompt para realizar el modelado de amenazas de un sistema, componente o feature antes o durante su diseño. Identifica superficies de ataque, actores maliciosos, vectores de amenaza y controles de mitigación usando la metodología STRIDE. Genera el insumo de seguridad para los prompts `13-01` (SAST) y `13-03` (Secure SDLC review).

**Cuándo usarlo:** en la fase de diseño de nuevas funcionalidades con impacto en seguridad, al diseñar integraciones con sistemas externos, al cambiar el modelo de autenticación o autorización, o al incorporar manejo de datos sensibles.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el diseño de solución (`04-01`) o casos de uso (`04-03`) si están disponibles.
> Adjunta diagramas de arquitectura o flujo existentes (`04-02`).

---

## Prompt completo

```text
Objetivo:
Realiza el modelado de amenazas del sistema o componente indicado usando la
metodología STRIDE, identifica las superficies de ataque, los actores maliciosos,
los vectores de amenaza y los controles de mitigación requeridos.

Pasos:

1. DESCRIPCIÓN DEL SISTEMA
   Describe el sistema o componente a analizar:
   - propósito del sistema
   - actores legítimos (usuarios, sistemas, servicios externos)
   - datos que procesa, almacena o transmite
   - límites de confianza (trust boundaries): dónde cambia el nivel de confianza
     entre componentes (ej: internet → load balancer, cliente → API, API → BD)
   - tecnologías involucradas: lenguaje, framework, base de datos, colas, APIs externas

2. DIAGRAMA DE FLUJO DE DATOS (DFD nivel 0 y nivel 1)
   Genera en texto estructurado (para convertir a diagrama) los componentes y flujos:
   - entidades externas (usuarios, sistemas externos)
   - procesos (servicios, funciones, módulos)
   - almacenes de datos (BD, caché, archivos, sesiones)
   - flujos de datos entre componentes (indicar si son confiables o no confiables)
   - límites de confianza (representar con línea punteada)

3. IDENTIFICACIÓN DE AMENAZAS — METODOLOGÍA STRIDE
   Para cada componente y flujo significativo, evalúa las 6 categorías STRIDE:

   S — Spoofing (Suplantación de identidad)
   ¿Puede un atacante hacerse pasar por un usuario u componente legítimo?
   - Ejemplos: credenciales robadas, JWT falsificados, ARP spoofing, DNS spoofing
   - Controles típicos: autenticación fuerte (MFA), certificados TLS mutuos, firmas digitales

   T — Tampering (Manipulación)
   ¿Puede un atacante modificar datos en tránsito o en reposo sin detección?
   - Ejemplos: SQL injection, modificación de parámetros de URL, man-in-the-middle
   - Controles típicos: HTTPS, firma de mensajes (HMAC), validación de integridad, ORM

   R — Repudiation (Repudio)
   ¿Puede un actor negar haber realizado una acción?
   - Ejemplos: ausencia de logs de auditoría, logs manipulables, sin firma de transacciones
   - Controles típicos: logging de auditoría inmutable, firma de transacciones, timestamps

   I — Information Disclosure (Divulgación de información)
   ¿Puede un atacante acceder a datos a los que no tiene derecho?
   - Ejemplos: IDOR, errores con stack trace, archivos de configuración expuestos,
     datos en logs, directorios listables
   - Controles típicos: control de acceso, encoding de salida, manejo de errores seguro,
     principio de menor privilegio

   D — Denial of Service (Denegación de servicio)
   ¿Puede un atacante degradar o interrumpir el servicio?
   - Ejemplos: flood de requests, queries costosas sin límite, uploads ilimitados,
     recursión infinita, lock de base de datos
   - Controles típicos: rate limiting, timeouts, paginación, validación de tamaño de input,
     circuit breaker

   E — Elevation of Privilege (Escalada de privilegios)
   ¿Puede un atacante obtener más privilegios de los asignados?
   - Ejemplos: IDOR con acceso a recursos de otros usuarios, bypassear verificación de rol,
     command injection que ejecuta como root, JWT con rol manipulable
   - Controles típicos: autorización en backend (nunca solo en cliente), tokens firmados,
     verificación de pertenencia de recursos, sandbox

4. ÁRBOL DE AMENAZAS (Attack Trees) — top 3 escenarios de mayor riesgo
   Para los 3 escenarios más críticos identificados:
   - nombre del escenario de ataque
   - objetivo del atacante
   - precondiciones necesarias
   - pasos del ataque (árbol de decisiones)
   - probabilidad estimada: [ALTA / MEDIA / BAJA]
   - impacto estimado: [CRÍTICO / ALTO / MEDIO / BAJO]

5. CLASIFICACIÓN DE AMENAZAS POR RIESGO
   Prioriza todas las amenazas identificadas con:
   - ID de amenaza
   - categoría STRIDE
   - componente afectado
   - descripción del vector
   - probabilidad (1-3)
   - impacto (1-3)
   - riesgo = probabilidad × impacto (1-9)
   - control de mitigación propuesto
   - estado: [SIN MITIGAR / MITIGADO / ACEPTADO]

6. SUPERFICIE DE ATAQUE
   Documenta la superficie de ataque total del sistema:
   - endpoints HTTP/API expuestos (internos y externos)
   - interfaces de usuario (web, mobile, CLI)
   - colas de mensajes o eventos
   - importación/exportación de archivos
   - integraciones con terceros (webhooks, OAuth, APIs)
   - interfaces de administración
   - scripts de mantenimiento o batch jobs

7. RECOMENDACIONES DE ARQUITECTURA DE SEGURIDAD
   Lista los controles de seguridad a implementar o validar antes del desarrollo,
   agrupados por capa:
   - Capa de red: WAF, firewall, segmentación, TLS
   - Capa de aplicación: autenticación, autorización, validación, rate limiting
   - Capa de datos: cifrado en reposo, cifrado en tránsito, acceso mínimo a BD
   - Capa de operaciones: logging de seguridad, alertas, rotación de secretos

Entrega:
- DFD textual del sistema con límites de confianza marcados,
- tabla completa de amenazas STRIDE con riesgo y mitigación,
- top 3 árboles de amenaza con pasos de ataque,
- mapa de superficie de ataque,
- lista de controles de seguridad requeridos por capa,
- este documento sirve como input obligatorio para 13-01 (SAST) y 13-03 (Secure SDLC).
```

---

## Uso con fórmula estándar

```text
Usa el prompt de threat modeling y adáptalo a:
- repositorio: [NOMBRE O URL]
- sistema o feature a modelar: [DESCRIPCIÓN]
- actores legítimos: [USUARIOS, SISTEMAS EXTERNOS]
- datos sensibles involucrados: [PII / financieros / credenciales / ninguno]
- integraciones externas: [LISTA DE APIS O SERVICIOS EXTERNOS]
- modelo de autenticación: [JWT / session / OAuth2 / API key]
- documentos a revisar: diseño de solución (04-01), casos de uso (04-03),
  diagramas (04-02), arquitectura del repositorio
- objetivo puntual de salida: modelo de amenazas STRIDE + controles de mitigación
- nivel de profundidad: alto
```

---

## Salida esperada

### Diagrama de flujo de datos (textual)

```
[Usuario] → (Login) → [BD de usuarios]
[Usuario] → (API /prompts) → [Servicio de prompts] → [BD de prompts]
[Servicio de prompts] → (integración) → [API externa]
---- Límite de confianza: Internet / API ----
---- Límite de confianza: API / Base de datos ----
```

### Tabla de amenazas STRIDE

| ID | STRIDE | Componente | Vector de amenaza | Prob. | Impacto | Riesgo | Mitigación | Estado |
|---|---|---|---|---|---|---|---|---|
| T-001 | Spoofing | API /login | JWT falsificado con alg:none | 2 | 3 | 6 | Validar alg explícito, usar librería confiable | Sin mitigar |
| T-002 | Injection | BD | SQL concatenado en búsqueda | 3 | 3 | 9 | ORM / consultas parametrizadas | Sin mitigar |
| T-003 | Info Disclosure | API errores | Stack trace en respuesta 500 | 3 | 2 | 6 | Manejo de errores genérico en producción | Sin mitigar |
