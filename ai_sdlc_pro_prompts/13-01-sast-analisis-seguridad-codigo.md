# 13.1 — SAST: Análisis estático de seguridad de código

## Descripción

Prompt para realizar un análisis estático de seguridad del código fuente (SAST — Static Application Security Testing): detecta vulnerabilidades OWASP Top 10, patrones inseguros, manejo incorrecto de datos sensibles, problemas de autenticación/autorización y deuda de seguridad antes de que lleguen a producción.

**Cuándo usarlo:** antes de abrir un PR, después de implementar un cambio con implicaciones de seguridad, o como revisión periódica del código base. Complementa (no reemplaza) a herramientas automáticas de SAST.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Si existe un resultado de `13-04` (Threat Modeling), adjúntalo como contexto de superficies de ataque conocidas.

---

## Prompt completo

```text
Objetivo:
Realiza un análisis estático de seguridad (SAST) del código indicado, identificando
vulnerabilidades, patrones inseguros y deuda de seguridad según OWASP Top 10 y
buenas prácticas de desarrollo seguro.

Pasos:

1. RECONOCIMIENTO DEL CÓDIGO
   - Identifica el lenguaje, framework y versión.
   - Mapea los puntos de entrada de datos: endpoints HTTP, formularios, argumentos
     de CLI, colas de mensajes, imports de archivos, variables de entorno.
   - Identifica las salidas: respuestas HTTP, logs, archivos generados, BD, APIs externas.
   - Detecta el modelo de autenticación y autorización en uso.

2. ANÁLISIS POR CATEGORÍA OWASP TOP 10 (2021)
   Para cada categoría, reporta: ¿aplica al código?, hallazgos encontrados, severidad.

   A01 — Broken Access Control
   - Verificación de permisos en cada endpoint/función sensible
   - Exposición de IDs directos (IDOR)
   - Bypass de autorización por manipulación de parámetros

   A02 — Cryptographic Failures
   - Datos sensibles en texto plano (contraseñas, tokens, PII)
   - Algoritmos débiles o deprecados (MD5, SHA1, DES, ECB)
   - Certificados, claves hardcodeadas o en código fuente

   A03 — Injection
   - SQL Injection (queries concatenadas, sin parametrizar)
   - Command Injection (llamadas a OS con input de usuario)
   - LDAP, XPath, NoSQL Injection
   - Template Injection (SSTI)

   A04 — Insecure Design
   - Lógica de negocio explotable
   - Ausencia de rate limiting en operaciones críticas
   - Flujos sin validación de estado

   A05 — Security Misconfiguration
   - Headers HTTP de seguridad ausentes (CSP, HSTS, X-Frame-Options, etc.)
   - Modo debug habilitado o stack traces expuestos
   - CORS permisivo (*) en APIs privadas
   - Configuración de errores verbosa

   A06 — Vulnerable and Outdated Components
   - Dependencias con CVEs conocidos (remitir a 13-02 para análisis completo)
   - Versiones de runtime o framework desactualizadas

   A07 — Identification and Authentication Failures
   - Ausencia de límite de intentos de login / protección contra fuerza bruta
   - Tokens de sesión predecibles o sin expiración
   - Recuperación de contraseña insegura

   A08 — Software and Data Integrity Failures
   - Deserialización insegura de datos externos
   - Ausencia de verificación de integridad en actualizaciones o pipelines
   - Dependencias sin lock files o pinning de versión

   A09 — Security Logging and Monitoring Failures
   - Ausencia de logging de eventos de seguridad (logins fallidos, cambios de permisos)
   - Datos sensibles en logs
   - Sin alertas sobre patrones anómalos

   A10 — Server-Side Request Forgery (SSRF)
   - Llamadas a URLs construidas con input del usuario
   - Ausencia de validación de esquema y host en URLs externas

3. ANÁLISIS ADICIONAL
   - Secrets hardcodeados: claves API, contraseñas, tokens en código o comentarios
   - Manejo de errores: ¿se exponen detalles internos al cliente?
   - Validación de inputs: ¿se valida tipo, longitud y formato en la capa correcta?
   - Race conditions en operaciones críticas (pagos, stock, permisos)
   - Dependencias de terceros cargadas desde CDN sin integridad (SRI)

4. HERRAMIENTAS RECOMENDADAS
   Según el lenguaje detectado, indica los comandos exactos para ejecutar SAST
   automático como complemento a este análisis:
   - Python: bandit, semgrep, pylint-django (si aplica)
   - JavaScript/TypeScript: eslint-plugin-security, semgrep, njsscan
   - Java: SpotBugs + FindSecBugs, SonarQube
   - PHP: PHPCS Security Audit, Psalm
   - Go: gosec, staticcheck
   - Ruby: brakeman
   - Genérico: semgrep con ruleset p/owasp-top-ten

5. CLASIFICACIÓN DE HALLAZGOS
   Usa la escala CVSS v3.1 para severidad:
   - CRÍTICO (CVSS 9.0-10.0): explotable remotamente, sin autenticación, impacto total
   - ALTO (CVSS 7.0-8.9): explotable con condiciones mínimas
   - MEDIO (CVSS 4.0-6.9): explotable con condiciones específicas
   - BAJO (CVSS 0.1-3.9): impacto limitado o difícil explotación
   - INFORMATIVO: best practice, no es vulnerabilidad

Entrega:
- tabla de hallazgos con severidad, categoría OWASP, componente, descripción y remediación,
- lista de herramientas SAST recomendadas con comandos de ejecución,
- resumen ejecutivo: nivel de riesgo global del código analizado,
- plan de remediación priorizado por severidad.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de SAST y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA A ANALIZAR]
- archivos o módulos a revisar: [RUTAS — o "todo el repositorio"]
- lenguaje y framework: [AUTO-DETECTAR]
- modelo de autenticación: [JWT / session / OAuth2 / API key / otro]
- datos sensibles manejados: [PII / financieros / credenciales / ninguno]
- documentos a revisar: threat model si existe (13-04), arquitectura, contratos API
- objetivo puntual de salida: reporte SAST completo con plan de remediación por severidad
- nivel de profundidad: alto
```

---

## Salida esperada

### Resumen ejecutivo

| Dimensión | Resultado |
|---|---|
| Nivel de riesgo global | [CRÍTICO / ALTO / MEDIO / BAJO] |
| Hallazgos críticos | N |
| Hallazgos altos | N |
| Hallazgos medios | N |
| Hallazgos bajos | N |
| Informativos | N |

### Tabla de hallazgos

| ID | Categoría OWASP | Severidad | Componente / Línea | Descripción | Remediación | CVSS estimado |
|---|---|---|---|---|---|---|
| SAST-001 | A03 — Injection | CRÍTICO | `api/views.py:42` | Query SQL concatenada con input de usuario | Usar ORM o consultas parametrizadas | 9.8 |
| SAST-002 | A02 — Crypto Failures | ALTO | `utils/auth.py:18` | Contraseña hasheada con MD5 | Migrar a bcrypt / Argon2 | 7.5 |

### Plan de remediación

| Prioridad | Hallazgo | Esfuerzo | Responsable | Fecha límite sugerida |
|---|---|---|---|---|
| 1 | SAST-001 — SQL Injection | Bajo | Dev backend | Inmediato |
| 2 | SAST-002 — MD5 passwords | Medio | Dev + DBA | Sprint actual |
