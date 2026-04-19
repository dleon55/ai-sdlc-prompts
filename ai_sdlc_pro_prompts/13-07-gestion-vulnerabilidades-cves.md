# 13.7 — Análisis de vulnerabilidades y gestión de CVEs

## Descripción

Prompt para realizar el triaje, clasificación, priorización y gestión del ciclo de vida completo de las vulnerabilidades detectadas por cualquier herramienta de seguridad (SAST, SCA, DAST, pentesting, escáneres). Convierte hallazgos crudos en un backlog de seguridad accionable con SLAs de remediación.

**Cuándo usarlo:** después de ejecutar cualquier herramienta de análisis de seguridad (`13-01` SAST, `13-02` SCA, `13-05` DAST, `13-06` pentesting), al recibir alertas de nuevos CVEs que afectan las dependencias del proyecto, o como revisión periódica del estado de seguridad.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta los resultados de las herramientas de seguridad ejecutadas: reportes de `13-01`, `13-02`, `13-05`, `13-06` o salidas de escáneres automáticos.

---

## Prompt completo

```text
Objetivo:
Realiza el triaje, clasificación, priorización y gestión de vulnerabilidades detectadas,
convirtiendo los hallazgos de seguridad en un backlog accionable con SLAs de remediación,
propietario asignado y criterios de cierre verificables.

Pasos:

1. CONSOLIDACIÓN DE HALLAZGOS
   Consolida todas las vulnerabilidades reportadas desde las diferentes fuentes:
   - herramienta o fuente de origen (SAST, SCA, DAST, pentesting, escáner, manual)
   - ID original del hallazgo en la herramienta fuente
   - componente, archivo, línea o dependencia afectada
   - descripción técnica del problema
   - elimina duplicados: si la misma vulnerabilidad aparece en múltiples fuentes,
     consolida en un único ítem referenciando todas las fuentes

2. TRIAJE Y VALIDACIÓN
   Para cada hallazgo, determina si es un verdadero positivo:
   - ¿Es el código vulnerable realmente ejecutable en el contexto del proyecto?
   - ¿Existe algún control compensatorio que mitigue el riesgo?
   - ¿Es un falso positivo de la herramienta? (documentar el razonamiento)
   - ¿Es una vulnerabilidad conocida y aceptada previamente?
   
   Clasifica el resultado del triaje:
   - VERDADERO POSITIVO: requiere remediación
   - FALSO POSITIVO: documentar y suprimir en la herramienta
   - ACEPTADO CON RIESGO: registrar decisión con aprobación y fecha de revisión
   - FUERA DE ALCANCE: documentar por qué no aplica

3. PUNTUACIÓN Y SEVERIDAD
   Para cada verdadero positivo, calcula o valida la severidad usando CVSS v3.1:

   Vector base:
   - Vector de ataque (AV): Red / Adyacente / Local / Físico
   - Complejidad de ataque (AC): Bajo / Alto
   - Privilegios requeridos (PR): Ninguno / Bajo / Alto
   - Interacción de usuario (UI): Ninguna / Requerida
   - Alcance (S): Sin cambio / Cambiado
   - Impacto en Confidencialidad (C): Alto / Bajo / Ninguno
   - Impacto en Integridad (I): Alto / Bajo / Ninguno
   - Impacto en Disponibilidad (A): Alto / Bajo / Ninguno

   Ajuste contextual (Environmental Score):
   - ¿Cuál es el impacto real en el negocio si se explota esta vulnerabilidad?
   - ¿Los datos expuestos son públicos, internos o altamente confidenciales?
   - ¿El sistema afectado es crítico para la operación del negocio?

   Escala de severidad ajustada:
   - CRÍTICO (CVSS ≥ 9.0): amenaza inmediata — SLA 24 horas
   - ALTO (CVSS 7.0-8.9): riesgo significativo — SLA 7 días
   - MEDIO (CVSS 4.0-6.9): riesgo moderado — SLA 30 días
   - BAJO (CVSS 0.1-3.9): riesgo limitado — SLA 90 días
   - INFORMATIVO: sin SLA — evaluar en próxima revisión de deuda técnica

4. ANÁLISIS DE EXPLOTABILIDAD
   Para los hallazgos críticos y altos, evalúa:
   - ¿Existe exploit público conocido? (Exploit-DB, Metasploit, PoC en GitHub)
   - ¿Está siendo explotado activamente (KEV — CISA Known Exploited Vulnerabilities)?
   - ¿Requiere autenticación para ser explotado?
   - ¿Es necesario acceso a red interna o puede explotarse desde internet?
   - EPSS score si disponible (Exploit Prediction Scoring System)

   Si existe exploit público activo → escalar SLA a inmediato, independiente del CVSS.

5. PLAN DE REMEDIACIÓN
   Para cada vulnerabilidad, define:
   
   a) Remediación preferida (fix permanente):
      - qué cambio exacto se debe hacer (actualizar dependencia, cambiar código, configurar)
      - archivos o componentes afectados
      - esfuerzo estimado: [< 1h / medio día / 1 día / > 1 día]
      - riesgo de regresión del fix: [bajo / medio / alto]

   b) Mitigación temporal (si el fix tarda):
      - control compensatorio que reduce el riesgo mientras se implementa el fix
      - ejemplos: WAF rule, feature flag, validación adicional en capa superior, patch temporal

   c) Verificación del fix:
      - cómo verificar que la vulnerabilidad fue correctamente remediada
      - prueba o comando específico para confirmar el cierre

6. BACKLOG DE SEGURIDAD
   Genera el backlog de issues de seguridad listo para crear en GitHub Issues / Jira:
   - título: [SEVERIDAD] [CVE-ID o SAST-ID] — Descripción breve del problema
   - etiquetas: security, [severidad], [categoría OWASP si aplica]
   - descripción: vector, impacto, componente afectado, pasos de remediación
   - criterios de aceptación: qué debe cumplirse para cerrar el issue
   - fecha límite según SLA

7. MÉTRICAS Y REPORTING
   Genera las métricas del estado de seguridad del proyecto:
   - Mean Time to Detect (MTTD): tiempo promedio entre introducción y detección
   - Mean Time to Remediate (MTTR): tiempo promedio de remediación por severidad
   - Deuda de seguridad total: suma de vulnerabilidades abiertas ponderadas por severidad
   - Tendencia: ¿el número de vulnerabilidades sube, baja o se mantiene?
   - Cumplimiento de SLAs: % de vulnerabilidades cerradas dentro del SLA definido

Entrega:
- tabla consolidada de vulnerabilidades con triaje y severidad CVSS,
- backlog de seguridad en formato de issues listo para crear,
- plan de remediación priorizado con SLAs y propietarios,
- métricas del estado de seguridad del proyecto,
- dashboard resumen para reporte ejecutivo.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de gestión de vulnerabilidades y CVEs y adáptalo a:
- repositorio: [NOMBRE O URL]
- fuentes de hallazgos: [SAST 13-01 / SCA 13-02 / DAST / pentesting / alerta Dependabot]
- resultados adjuntos: [ADJUNTA LOS REPORTES DE LAS HERRAMIENTAS]
- ambiente objetivo: [DEV / QA / STAGING / PROD]
- criticidad del sistema: [CRÍTICA / ALTA / MEDIA — según impacto al negocio]
- SLAs definidos: [USAR ESTÁNDAR / PERSONALIZAR: crítico=Xh, alto=Xd, medio=Xd]
- documentos a revisar: registros de vulnerabilidades previas, CHANGELOG de seguridad
- objetivo puntual de salida: backlog de seguridad priorizado + métricas de estado
- nivel de profundidad: alto
```

---

## Salida esperada

### Tabla de vulnerabilidades consolidada

| ID | Fuente | Componente | Descripción | CVSS | Severidad | Triaje | Fix disponible | SLA | Propietario |
|---|---|---|---|---|---|---|---|---|---|
| VUL-001 | SAST-001 | `api/views.py:42` | SQL Injection en búsqueda | 9.8 | CRÍTICO | Verdadero positivo | Sí — parametrizar query | 24h | Backend dev |
| VUL-002 | SCA | `requests==2.25.0` | CVE-2023-32681 SSRF | 6.1 | MEDIO | Verdadero positivo | Sí — actualizar a 2.32.3 | 30 días | DevOps |

### Dashboard de seguridad

| Métrica | Valor |
|---|---|
| Total vulnerabilidades | N |
| Críticas abiertas | N |
| Altas abiertas | N |
| % dentro de SLA | N% |
| MTTR críticas | Xh |
| Deuda de seguridad | Score |
