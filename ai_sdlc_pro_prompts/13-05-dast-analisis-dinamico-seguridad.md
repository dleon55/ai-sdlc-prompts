# 13.5 — DAST: Análisis dinámico de seguridad de aplicación

## Descripción

Prompt para diseñar y ejecutar un análisis dinámico de seguridad (DAST — Dynamic Application Security Testing) sobre la aplicación en ejecución: identifica vulnerabilidades explotables en tiempo real, valida la superficie de ataque expuesta, y prueba controles de seguridad de la capa de transporte, autenticación, sesiones y APIs.

**Cuándo usarlo:** cuando la aplicación pueda levantarse en un entorno aislado (local, staging, Docker), antes de promover a producción, o como parte del pipeline CI/CD en la fase de validación de seguridad. Complementa al análisis estático (`13-01` SAST) y al modelo de amenazas (`13-04`).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta resultados de `13-04` (Threat Modeling) para usar la superficie de ataque identificada como guía de pruebas.
> Adjunta resultados de `13-01` (SAST) si existen, para complementar con hallazgos dinámicos.

---

## Prompt completo

```text
Objetivo:
Realizar análisis dinámico de seguridad (DAST) sobre la aplicación en ejecución,
identificando vulnerabilidades explotables en tiempo real, validando la superficie de
ataque expuesta y probando los controles de seguridad de transporte, autenticación,
gestión de sesiones y APIs.

Pasos:

1. RECONOCIMIENTO DE SUPERFICIE DE ATAQUE DINÁMICA
   Con la aplicación en ejecución, mapear:
   - Todos los endpoints HTTP/HTTPS accesibles (rutas, métodos, parámetros)
   - APIs REST o GraphQL expuestas: endpoints, métodos aceptados, tipos de respuesta
   - Formularios web y campos de entrada (GET y POST)
   - Archivos estáticos y directorios accesibles públicamente
   - Cabeceras de respuesta HTTP y cookies
   - Mecanismos de autenticación expuestos (login, OAuth, tokens, API keys)
   - Flujos de redirección y gestión de sesión

2. ANÁLISIS DE CAPA DE TRANSPORTE
   Verificar la seguridad de la comunicación:
   
   a) TLS/SSL:
      - Versión de protocolo: ¿solo TLS 1.2+? ¿TLS 1.0/1.1 deshabilitado?
      - Algoritmos de cifrado: ¿suites débiles habilitadas? (RC4, DES, 3DES, NULL)
      - Certificado: validez, cadena de confianza, wildcard, SANs
      - HSTS: ¿cabecera Strict-Transport-Security presente con max-age ≥ 31536000?
      - HSTS includeSubDomains y preload activados
   
   b) Cabeceras de seguridad HTTP:
      - Content-Security-Policy (CSP): ¿presente? ¿restringe inline scripts y fuentes?
      - X-Frame-Options o frame-ancestors en CSP: protección contra clickjacking
      - X-Content-Type-Options: nosniff
      - Referrer-Policy: no expone URLs internas
      - Permissions-Policy: limita acceso a APIs del navegador
      - Cache-Control en respuestas con datos sensibles

3. PRUEBAS DE AUTENTICACIÓN Y SESIÓN
   
   a) Mecanismo de autenticación:
      - ¿Permite enumeración de usuarios? (respuestas distintas para usuario vs. contraseña incorrecta)
      - ¿Implementa límite de intentos o CAPTCHA?
      - ¿Transmite credenciales en texto plano o parámetros GET?
      - ¿Las API keys o tokens aparecen en URLs, logs o cabeceras sin protección?
   
   b) Gestión de sesiones:
      - ¿Las cookies de sesión tienen atributos HttpOnly, Secure, SameSite=Strict/Lax?
      - ¿El ID de sesión es suficientemente aleatorio? (mínimo 128 bits de entropía)
      - ¿Se regenera el ID de sesión tras el login exitoso?
      - ¿La sesión se invalida correctamente en logout?
      - ¿Verifica origen en peticiones de cambio de estado? (protección CSRF)

4. PRUEBAS DE INYECCIÓN (DINÁMICA)
   Ingresar payloads en todos los puntos de entrada para detectar:
   
   a) Inyección SQL (si aplica tecnología de BD):
      - Payloads básicos: `'`, `''`, `1' OR '1'='1`, `1; DROP TABLE`, `UNION SELECT NULL`
      - Comportamiento de error: ¿mensajes de BD expuestos en respuesta?
      - Blind SQL: comparar tiempos de respuesta con `1 AND SLEEP(3)`
   
   b) Cross-Site Scripting (XSS):
      - Reflected XSS: `<script>alert(1)</script>` en parámetros GET/POST
      - Stored XSS: enviar payload en campos que se persistan y luego se muestren
      - DOM-based XSS: verificar manejo de `document.location`, `innerHTML`, `eval()`
      - CSP bypass: ¿el payload es bloqueado o ejecutado a pesar de la CSP?
   
   c) Inyección de comandos OS:
      - `; ls`, `| id`, `&& whoami`, `$(id)` en campos de entrada procesados por el sistema
   
   d) SSRF (Server-Side Request Forgery):
      - URLs internas en campos URL: `http://localhost:8080/admin`, `http://169.254.169.254/`
      - Protocolos alternativos: `file:///etc/passwd`, `dict://`, `gopher://`
   
   e) XXE (XML External Entity) si la app procesa XML:
      - Payloads de entidad externa en documentos XML enviados al servidor

5. PRUEBAS DE CONTROL DE ACCESO
   
   a) Control de acceso horizontal (IDOR):
      - ¿Acceder a recursos de otro usuario cambiando IDs en la URL o cuerpo? (p. ej. `/api/users/123` → `/api/users/124`)
      - ¿Modificar o eliminar recursos de otro usuario con la propia sesión?
   
   b) Control de acceso vertical (escalada de privilegios):
      - ¿Un usuario sin privilegios puede acceder a rutas de administración?
      - ¿Cambiar roles o permisos en el token JWT modifica el acceso?
      - ¿Endpoints de API admin accesibles sin autenticación?
   
   c) Métodos HTTP no autorizados:
      - ¿PUT, DELETE, PATCH permitidos en recursos que no deberían aceptarlos?
      - ¿OPTIONS revela métodos inesperados?

6. PRUEBAS DE EXPOSICIÓN DE INFORMACIÓN
   Verificar que la aplicación no exponga:
   - Stack traces o mensajes de error detallados en respuestas (nombres de frameworks, versiones, rutas internas)
   - Datos sensibles en respuestas JSON que no son necesarios para el cliente
   - Archivos de configuración accesibles: `.env`, `config.json`, `database.yml`, `.git/config`
   - Directorios listables o archivos residuales (`.bak`, `.old`, `~`, `.swp`)
   - Tokens, claves o credenciales en comentarios HTML o JavaScript

7. DOCUMENTACIÓN Y CLASIFICACIÓN DE HALLAZGOS
   Para cada vulnerabilidad encontrada:
   - ID único: DAST-XXX
   - Categoría OWASP (A01-A10)
   - Método de reproducción exacto: URL, método HTTP, payload, cabeceras
   - Respuesta del servidor que confirma la vulnerabilidad
   - Impacto potencial si se explota
   - Severidad CVSS v3.1 (vector completo)
   - Remediación recomendada
   - Estado: confirmado / requiere verificación manual / falso positivo

Herramientas recomendadas (usar en entorno aislado, nunca en producción sin autorización):
- OWASP ZAP (Zed Attack Proxy): escaneo automatizado + pruebas manuales
- Burp Suite Community/Pro: interceptación y modificación de tráfico
- Nikto: escaneo de servidor web y configuraciones inseguras
- Nuclei: plantillas de vulnerabilidades conocidas (CVEs)
- testssl.sh o ssllabs: análisis de configuración TLS
- sqlmap: detección automatizada de SQLi (SOLO en entornos propios con autorización)

Entregables:
- mapa de superficie de ataque dinámica (endpoints, formularios, APIs),
- tabla de hallazgos DAST (ID, OWASP, severidad, payload reproducible, remediación),
- resumen ejecutivo de controles de seguridad: cuáles pasan y cuáles fallan,
- comparativa con hallazgos SAST para identificar vulnerabilidades no detectadas estáticamente,
- plan de remediación priorizado por CVSS.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de DAST y adáptalo a:
- repositorio: [NOMBRE O URL]
- entorno de pruebas: [URL BASE donde corre la aplicación — staging / Docker local]
- stack tecnológico: [frontend / backend / BD / autenticación]
- tipo de aplicación: [web tradicional / SPA / API REST / API GraphQL]
- mecanismo de autenticación: [sesiones / JWT / OAuth2 / API key]
- áreas de mayor riesgo según threat model: [ADJUNTAR RESULTADO 13-04 si existe]
- herramientas disponibles: [ZAP / Burp Suite / Nikto / ninguna — solo manual]
- documentos a revisar: código fuente, modelo de amenazas 13-04, resultados SAST 13-01
- objetivo de salida específico: tabla de hallazgos DAST + mapa de superficie de ataque
- nivel de profundidad: alto
```

---

## Resultado esperado

### Mapa de superficie de ataque dinámica

| Endpoint | Método | Autenticación requerida | Parámetros entrada | Notas |
|---|---|---|---|---|
| `/api/users` | GET | Sí — JWT | `page`, `limit` | Verificar IDOR |
| `/api/search` | GET | No | `q` | Candidato a XSS reflected |
| `/login` | POST | No | `username`, `password` | Verificar enumeración de usuarios |

### Tabla de hallazgos DAST

| ID | OWASP | Severidad | Endpoint | Payload / Método | Impacto | Remediación | CVSS |
|---|---|---|---|---|---|---|---|
| DAST-001 | A03 — Inyección | CRÍTICO | `/api/search?q=` | `<script>alert(1)</script>` | XSS reflected — robo de sesión | Escapar output, reforzar CSP | 8.1 |
| DAST-002 | A05 — Misc. Config | MEDIO | Cabecera respuesta | (ausente) | Falta X-Frame-Options — clickjacking posible | Agregar `X-Frame-Options: DENY` | 5.3 |

### Resumen de controles de seguridad

| Control | Estado | Observación |
|---|---|---|
| TLS 1.3 activo | ✅ Pasa | Protocolo correcto |
| HSTS habilitado | ⚠️ Parcial | Falta `includeSubDomains` |
| Content-Security-Policy | ❌ Falla | Política ausente — XSS sin mitigación |
| Cookies seguras (HttpOnly + Secure) | ✅ Pasa | Atributos correctos |
| Límite de intentos en login | ❌ Falla | Sin rate limiting — fuerza bruta posible |
