# 13.3 — Revisión de desarrollo de software seguro (Secure SDLC)

## Descripción

Prompt para verificar que se han aplicado los controles de seguridad requeridos en cada fase del ciclo de desarrollo: desde el diseño hasta el despliegue. Actúa como checklist estructurado de Secure SDLC basado en OWASP SAMM, NIST SSDF y Microsoft SDL, adaptable a proyectos nuevos y cambios incrementales.

**Cuándo usarlo:** al cierre de cada sprint, antes de un release a producción, como revisión de madurez de seguridad del proyecto, o cuando se incorpora un nuevo equipo o agente al proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta resultados relevantes disponibles: `13-01` (SAST), `13-02` (SCA), `13-04` (Threat Modeling).

---

## Prompt completo

```text
Objetivo:
Verifica el nivel de madurez de seguridad del proyecto evaluando si se han aplicado
los controles requeridos en cada fase del ciclo de desarrollo de software seguro
(Secure SDLC), y genera un plan de mejora para las brechas encontradas.

Fases y controles a evaluar:

1. FASE DE REQUERIMIENTOS Y DISEÑO
   □ ¿Se realizó modelado de amenazas (threat modeling) antes de implementar?
   □ ¿Se definieron requerimientos de seguridad explícitos (no asumidos)?
   □ ¿Se identificaron datos sensibles y su clasificación (PII, financiero, confidencial)?
   □ ¿Se diseñó el modelo de autenticación y autorización antes de codificar?
   □ ¿Se consideraron los principios de diseño seguro?
     - Menor privilegio (least privilege)
     - Defense in depth
     - Fail securely
     - Separation of concerns
     - No security by obscurity
   □ ¿Se documentó la superficie de ataque del sistema?

2. FASE DE IMPLEMENTACIÓN
   □ ¿Se siguieron guías de codificación segura para el lenguaje/framework del proyecto?
   □ ¿Se valida y sanitiza todo input en la capa correcta (no solo en el cliente)?
   □ ¿Se usan consultas parametrizadas / ORM para acceso a base de datos?
   □ ¿Se aplica encoding de salida para prevenir XSS?
   □ ¿Se manejan errores sin exponer información interna al cliente?
   □ ¿Se usan cabeceras HTTP de seguridad? (CSP, HSTS, X-Content-Type-Options, etc.)
   □ ¿Los secretos se gestionan vía variables de entorno o vault, nunca en código?
   □ ¿Las contraseñas se almacenan con hashing adaptativo (bcrypt, Argon2, scrypt)?
   □ ¿Se aplica HTTPS en todos los endpoints, incluyendo internos?
   □ ¿Se limita el tamaño y tipo de archivos en upload endpoints?

3. FASE DE PRUEBAS DE SEGURIDAD
   □ ¿Se ejecutó SAST como parte del pipeline CI? (ver 13-01)
   □ ¿Se ejecutó SCA / análisis de dependencias? (ver 13-02)
   □ ¿Se realizaron pruebas de seguridad dinámicas (DAST) sobre el ambiente de QA?
   □ ¿Se ejecutaron pruebas de autenticación y autorización (roles, permisos, JWT)?
   □ ¿Se realizaron pruebas de inyección básicas (SQL, Command, SSTI)?
   □ ¿Se revisaron manualmente los endpoints más críticos?
   □ ¿El QA gate del CI falla si hay hallazgos de seguridad de severidad alta o crítica?

4. FASE DE REVISIÓN DE CÓDIGO (CODE REVIEW)
   □ ¿Existe un checklist de revisión de código con ítems de seguridad?
   □ ¿Al menos un revisor tiene conocimiento de seguridad de aplicaciones?
   □ ¿Se revisaron los cambios en autenticación, autorización y manejo de datos?
   □ ¿Se identificaron y documentaron supuestos de seguridad en el código?
   □ ¿Se revisaron los logs para confirmar que no incluyen datos sensibles?

5. FASE DE CI/CD Y DESPLIEGUE
   □ ¿El pipeline CI incluye lint de seguridad, SAST y SCA automático?
   □ ¿Las imágenes Docker están basadas en versiones oficiales y mínimas (distroless, alpine)?
   □ ¿Los contenedores corren como usuario no root?
   □ ¿Los secretos de producción se gestionan con un sistema dedicado? (Vault, AWS Secrets Manager, etc.)
   □ ¿Se aplica el principio de menor privilegio en los permisos del servicio?
   □ ¿Existe un proceso de rollback probado ante despliegues con problema de seguridad?
   □ ¿Los artefactos de build están firmados o verificados con checksum?

6. FASE DE OPERACIONES Y MONITOREO
   □ ¿Se registran eventos de seguridad en logs estructurados?
     (logins fallidos, cambios de permisos, acceso a datos sensibles)
   □ ¿Hay alertas configuradas para patrones anómalos?
   □ ¿Existe un proceso de respuesta a incidentes de seguridad? (ver 11-04)
   □ ¿Se realiza revisión periódica de accesos y permisos?
   □ ¿Se aplican parches de seguridad en tiempo razonable?
     (crítico: ≤24h, alto: ≤7 días, medio: ≤30 días)
   □ ¿Se realizan penetration tests o revisiones de seguridad periódicas? (ver 13-06)

7. MADUREZ POR DOMINIO (OWASP SAMM simplificado)
   Evalúa el nivel actual para cada dominio en escala 0-3:
   - Gobernanza (políticas, formación, cumplimiento)
   - Diseño (threat modeling, requisitos de seguridad)
   - Implementación (codificación segura, gestión de defectos)
   - Verificación (pruebas de seguridad, revisión de código)
   - Operaciones (gestión de incidentes, gestión de entornos)

Entrega:
- checklist completo con estado de cada control (✅ cumple / ⚠️ parcial / ❌ no cumple / N/A),
- nivel de madurez por fase (0-3),
- resumen de brechas críticas,
- plan de mejora priorizado con responsable y plazo sugerido,
- roadmap de madurez: qué alcanzar en el próximo sprint / trimestre / semestre.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de Secure SDLC review y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- fase del ciclo actual: [DISEÑO / IMPLEMENTACIÓN / QA / PRE-RELEASE / OPERACIÓN]
- resultados disponibles: [SAST 13-01 / SCA 13-02 / Threat Model 13-04 / ninguno]
- tipo de proyecto: [NUEVO / CAMBIO INCREMENTAL / MANTENIMIENTO]
- ambiente objetivo: [DEV / QA / STAGING / PROD]
- documentos a revisar: arquitectura, workflows CI/CD, políticas de seguridad del proyecto
- objetivo puntual de salida: checklist completo + plan de mejora con niveles de madurez
- nivel de profundidad: alto
```

---

## Salida esperada

### Checklist por fase

| Fase | Control | Estado | Evidencia / Nota |
|---|---|---|---|
| Diseño | Threat modeling realizado | ✅ / ⚠️ / ❌ | |
| Implementación | Secrets en vault, no en código | ✅ / ⚠️ / ❌ | |
| CI/CD | SAST en pipeline | ✅ / ⚠️ / ❌ | |

### Nivel de madurez por dominio (SAMM)

| Dominio | Nivel actual | Nivel objetivo | Brecha |
|---|---|---|---|
| Gobernanza | 1 / 3 | 2 / 3 | Falta política formal de seguridad |
| Diseño | 0 / 3 | 2 / 3 | No se realiza threat modeling |
| Implementación | 2 / 3 | 3 / 3 | Faltan guías de codificación formal |
| Verificación | 1 / 3 | 3 / 3 | SAST y DAST no integrados en CI |
| Operaciones | 2 / 3 | 3 / 3 | Sin alertas de seguridad en producción |

### Plan de mejora

| Prioridad | Brecha | Acción | Responsable | Plazo |
|---|---|---|---|---|
| 1 | SAST no en CI | Integrar bandit/semgrep en pipeline | DevOps | Sprint actual |
