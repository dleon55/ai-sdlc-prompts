# 11.2 — Hardening y seguridad operativa

## Descripción

Prompt para analizar el repositorio y la configuración operativa en busca de oportunidades de fortalecimiento de seguridad: hardening, manejo de secretos, permisos, exposición de servicios y riesgos de despliegue.

**Cuándo usarlo:** periódicamente como revisión de seguridad, antes de un despliegue a producción, o cuando se detectan hallazgos de seguridad en code review.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | seguridad |
| Riesgo esperado | alto — puede exponer configuración de infraestructura y secretos si se usa sin cuidado |
| Entradas requeridas | docker-compose, configuración nginx, `.env` (estructura, no valores), workflows, permisos de GitHub |
| Herramientas permitidas | lectura de configuración e infraestructura — nunca ejecutar cambios de configuración en el mismo paso |
| Autonomía permitida | A0 — Analizar (solo entrega hallazgos y plan de mitigación, no aplica cambios) |
| Criterios de detención | nunca incluir valores reales de secretos en la salida, aunque se detecten expuestos; referenciar solo ubicación y tipo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hallazgo debe indicar el archivo/componente exacto y la criticidad justificada |
| Siguiente prompt recomendado | `13-08-gestion-secretos-credenciales` si se detectan credenciales expuestas; `13-03-secure-sdlc-revision` para una revisión más amplia |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el repositorio y la configuración operativa para detectar oportunidades de fortalecimiento de seguridad, hardening, manejo de secretos, permisos, exposición de servicios y riesgos de despliegue.

Pasos:
1. Inventaria las fuentes de configuración operativa disponibles (docker-compose, nginx, `.env`, workflows de CI/CD, permisos de GitHub) y confirma cuáles son accesibles antes de continuar; si falta alguna, señálalo en vez de asumir que esa área está segura.
2. Revisa manejo de secretos: busca credenciales, tokens o claves hardcodeadas en código, configuración o historial de commits recientes. Reporta únicamente ubicación y tipo, nunca el valor real.
3. Revisa permisos: identifica cuentas de servicio, tokens de CI/CD o roles con privilegios más amplios de los que su función requiere (principio de mínimo privilegio).
4. Revisa exposición de servicios: puertos publicados innecesariamente, servicios sin autenticación, endpoints administrativos accesibles desde fuera de la red interna.
5. Revisa configuración insegura: flags de debug activos, CORS permisivo, headers de seguridad ausentes (CSP, HSTS, X-Frame-Options), TLS mal configurado o deshabilitado.
6. Revisa dependencias vulnerables: paquetes con CVEs conocidos o versiones desactualizadas de componentes críticos (framework web, librerías de autenticación/criptografía).
7. Revisa logging y auditoría: confirma que existan registros suficientes para detectar incidentes, sin que ese logging capture datos sensibles (PII, secretos) en texto plano.
8. Prioriza los hallazgos por explotabilidad e impacto: un secreto expuesto en un repositorio accesible es más urgente que un header de seguridad ausente en un endpoint interno de bajo riesgo.

Restricciones:
- nunca incluyas el valor real de un secreto, credencial o token en la salida, aunque lo detectes expuesto — referencia solo archivo, línea aproximada y tipo,
- esta es una auditoría de solo lectura: no apliques cambios de configuración, no rotes credenciales ni reinicies servicios como parte del mismo paso,
- si detectas una credencial que pudo haber sido comprometida, señala la necesidad de rotación inmediata y sigue el proceso de disclosure responsable del equipo — no la publiques ni la compartas fuera del canal de reporte designado,
- toda mitigación propuesta requiere revisión y aprobación humana antes de aplicarse; no ejecutes remediaciones automáticas ni scripts de corrección,
- si no tienes acceso a algún insumo requerido, señala la omisión explícitamente en la salida en vez de completar la matriz con supuestos.

Entrega:
- hallazgos,
- criticidad,
- mitigación,
- prioridad.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de hardening y seguridad y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- ambiente: [PROD / STAGING]
- componentes: [INFRAESTRUCTURA, SERVICIOS, CONFIGURACIONES]
- documentos a revisar: docker-compose, nginx, .env, workflows, permisos de GitHub
- objetivo puntual de salida: reporte de hallazgos de seguridad con plan de mitigación priorizado
- nivel de profundidad: alto
```

---

## Salida esperada

| Hallazgo | Categoría | Criticidad | Componente | Mitigación | Prioridad |
|---|---|---|---|---|---|
| Clave de API de terceros hardcodeada como valor por defecto (`STRIPE_KEY`) | secretos expuestos | crítica | `docker-compose.override.yml:14` | mover a un gestor de secretos (Vault / GitHub Actions secrets), rotar la clave expuesta y purgarla del historial de git | P0 |
| Token de CI/CD con permiso `repo` (acceso total) usado solo para publicar releases | permisos excesivos | alta | `.github/workflows/release.yml` | reemplazar por un GitHub App con permisos limitados a `contents:write` y `packages:write` | P1 |
| Puerto 5432 de PostgreSQL publicado directamente al host | servicios expuestos | alta | `docker-compose.yml`, servicio `db` | eliminar el mapeo de puerto público y exponerlo solo en la red interna de Docker | P1 |
| CORS configurado con `Access-Control-Allow-Origin: *` | configuración insegura | media | `nginx.conf` | restringir el origen a los dominios conocidos del frontend | P2 |
| Dependencia `lodash@4.17.15` con CVE conocido de prototype pollution | dependencias vulnerables | media | `package.json` | actualizar a `>=4.17.21` | P2 |
| El endpoint de login no registra intentos fallidos | logging insuficiente | baja | `auth/login` handler | agregar log estructurado de intentos fallidos sin registrar la contraseña ni otros datos sensibles | P3 |
