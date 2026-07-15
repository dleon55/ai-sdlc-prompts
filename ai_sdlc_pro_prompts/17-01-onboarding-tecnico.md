# 17.1 — Checklist de onboarding técnico

## Descripción

Prompt para generar un checklist concreto y accionable de onboarding técnico para un nuevo integrante del equipo de ingeniería: accesos a provisionar (repositorios, cloud, herramientas de CI/CD, gestor de secretos), herramientas a instalar/configurar en el entorno local, y documentación/contexto a revisar durante su primera semana. El checklist se adapta al rol y al stack tecnológico del equipo, distingue entre lo bloqueante para el día 1 y lo esperable durante la semana 1, y asigna un responsable a cada ítem. No otorga accesos ni crea cuentas: genera el checklist para que un humano con permisos (lead técnico, IT, administrador de IAM) lo ejecute.

**Cuándo usarlo:** al incorporar un nuevo integrante al equipo de ingeniería, antes o durante su primer día. Complementa a `17-02-offboarding-tecnico` como su contraparte simétrica: este prompt genera el checklist de qué otorgar y configurar al ingresar; `17-02-offboarding-tecnico` genera el checklist de qué revocar y desactivar al salir.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación/planificación |
| Riesgo esperado | medio — un checklist de accesos incompleto retrasa la productividad del nuevo integrante; un checklist excesivo (accesos de más, permisos elevados sin justificación) tiene implicaciones de seguridad, aunque el prompt en sí no otorga ningún acceso real |
| Entradas requeridas | rol y seniority del nuevo integrante, stack tecnológico y herramientas del equipo (repos, proveedor cloud, herramientas de CI/CD, gestor de secretos), nivel de acceso requerido por el rol, fecha de inicio, mentor/buddy asignado si existe, documentación interna disponible (wiki, runbooks, guías de arquitectura) |
| Herramientas permitidas | lectura de documentación interna existente sobre el stack, procesos y estructura de accesos del equipo; la salida es un checklist de texto — no crea cuentas, no otorga permisos IAM, no configura herramientas; la ejecución del aprovisionamiento de accesos queda delegada a quien tiene permisos IAM, no a este prompt |
| Autonomía permitida | A0 — Analizar (relevar rol, stack y accesos existentes del equipo); A1 — Proponer (el checklist de accesos, herramientas y documentación a revisar); nunca A2/A3 — este prompt no crea cuentas, no otorga permisos ni ejecuta cambios en sistemas de identidad o acceso |
| Criterios de detención | detener y pedir clarificación si no se especifica el rol o el stack del equipo — no fabricar un checklist genérico sin contexto; escalar a quien tenga permisos IAM antes de que se otorgue cualquier acceso listado; si falta información sobre el gestor de secretos o la política de acceso mínimo del equipo, señalarlo explícitamente en vez de asumirla |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada ítem del checklist indica el sistema o herramienta específica, el responsable/dueño que debe otorgarlo o configurarlo, y si es bloqueante para el día 1 o esperable durante la semana 1 |
| Siguiente prompt recomendado | `17-02-offboarding-tecnico` como su contraparte simétrica, para tener ambos flujos documentados de forma consistente |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Lead Técnico responsable de onboarding. Genera un checklist concreto y accionable de onboarding técnico para el nuevo integrante descrito, adaptado a su rol y al stack del equipo, cubriendo accesos a provisionar, herramientas a instalar/configurar y documentación a revisar en su primera semana. No otorgues ningún acceso ni ejecutes ninguna configuración: el checklist resultante debe ser ejecutado por una persona con los permisos correspondientes (lead técnico, IT, administrador de IAM).

Entradas:
- rol y seniority del nuevo integrante: [ej: Backend Engineer Semi-Senior / SRE / Data Engineer]
- stack tecnológico del equipo: [LENGUAJES, FRAMEWORKS, BASES DE DATOS]
- repositorios relevantes: [LISTA DE REPOS O "definir con el lead del equipo"]
- proveedor(es) cloud: [AWS / GCP / AZURE / OTRO]
- herramientas de CI/CD: [ej: GitHub Actions, Jenkins, CircleCI, GitLab CI]
- gestor de secretos: [ej: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, 1Password — o "no definido"]
- nivel de acceso requerido por el rol: [MÍNIMO INDISPENSABLE / ELEVADO CON JUSTIFICACIÓN]
- fecha de inicio: [FECHA]
- mentor/buddy asignado: [NOMBRE O "por asignar"]
- documentación interna disponible: [WIKI, RUNBOOKS, GUÍAS DE ARQUITECTURA — o "no disponible"]

Pasos:

1. RELEVAMIENTO DE ROL Y STACK
   Confirma el rol, seniority y las herramientas específicas que ese rol necesita tocar dado el stack del equipo. Si falta información crítica (rol o stack no especificado), detente y pide la clarificación en vez de generar un checklist genérico.

2. ACCESOS A REPOSITORIOS
   Lista los repositorios a los que el nuevo integrante necesita acceso, el nivel de permiso requerido (lectura, escritura, administración de rama protegida) según su rol, y quién es el responsable de otorgarlo (ej: administrador de la organización en GitHub/GitLab).

3. ACCESOS CLOUD
   Lista las cuentas y roles IAM necesarios en el/los proveedor(es) cloud indicados, aplicando el principio de mínimo privilegio por defecto. Señala explícitamente cualquier acceso elevado (admin, permisos de producción) y exige que quede justificado por el rol antes de otorgarse.

4. ACCESOS A HERRAMIENTAS DE CI/CD
   Lista los accesos necesarios en las herramientas de CI/CD del equipo (ver pipelines, disparar builds, administrar secretos de pipeline) diferenciando permisos de solo lectura de los que permiten modificar o disparar despliegues.

5. ACCESO AL GESTOR DE SECRETOS
   Lista qué secretos o namespaces del gestor de secretos necesita el rol, con qué nivel de acceso (lectura de secretos específicos vs administración), y quién aprueba el otorgamiento. Si el equipo no tiene gestor de secretos formalizado, señálalo como un riesgo a resolver antes de continuar con accesos ad-hoc.

6. HERRAMIENTAS DE COMUNICACIÓN Y GESTIÓN
   Lista accesos a herramientas de comunicación y gestión del equipo (chat, gestor de tickets/proyectos, documentación colaborativa) necesarios para operar desde el día 1.

7. HERRAMIENTAS Y ENTORNO LOCAL
   Lista lo que el nuevo integrante debe instalar/configurar en su entorno local: IDE y extensiones recomendadas, gestor de paquetes y versión del lenguaje/runtime, linters/formatters del equipo, contenedores/orquestación local si aplica, cliente VPN si el equipo lo requiere, generación y registro de llave SSH/GPG.

8. DOCUMENTACIÓN Y CONTEXTO A REVISAR EN LA PRIMERA SEMANA
   Lista la documentación interna que debe revisar antes de contribuir código de forma autónoma: visión general de arquitectura, guía de estilo/convenciones de código, proceso de code review y despliegue del equipo, política de on-call/incidentes si aplica, glosario de dominio del producto. Si algún documento no existe, señálalo como gap a resolver en vez de omitirlo silenciosamente.

9. CLASIFICACIÓN POR PRIORIDAD Y RESPONSABLE
   Para cada ítem del checklist (accesos, herramientas, documentación), indica: (a) si es bloqueante para el día 1 o esperable durante la semana 1, y (b) quién es el responsable/dueño de otorgarlo, instalarlo o compartirlo.

10. RESUMEN EJECUTIVO
    Resume cuántos accesos bloqueantes de día 1 existen, quiénes son los responsables clave a coordinar antes de la fecha de inicio, y cualquier gap de documentación o de gestor de secretos detectado.

Restricciones:
- este prompt genera el checklist; nunca crea cuentas, otorga permisos IAM, genera credenciales ni ejecuta comandos de aprovisionamiento (`aws iam`, `gcloud projects add-iam-policy-binding`, invitaciones de organización en el proveedor de Git, etc.) — esa ejecución queda siempre a cargo de una persona humana con los permisos correspondientes.
- aplica el principio de mínimo privilegio por defecto: no incluyas accesos administrativos o de producción salvo que el rol lo justifique explícitamente, y márcalos como tales para que reciban aprobación adicional.
- nunca incluyas contraseñas, tokens, claves API ni ninguna credencial real (ni de ejemplo con formato plausible) en el checklist.
- distingue siempre accesos/tareas bloqueantes para el día 1 de los esperables durante la semana 1; no trates todo el checklist como igualmente urgente.
- si falta información sobre el rol, el stack o el gestor de secretos del equipo, dilo explícitamente y pide la información en vez de inventar un checklist genérico o asumir herramientas que el equipo no usa.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de checklist de onboarding técnico y adáptalo a:
- repositorio/equipo: [NOMBRE O URL]
- rol y seniority del nuevo integrante: [ej: Backend Engineer Semi-Senior]
- stack tecnológico: [LENGUAJES, FRAMEWORKS, BASES DE DATOS]
- proveedor cloud: [AWS / GCP / AZURE]
- herramientas de CI/CD: [ej: GitHub Actions]
- gestor de secretos: [ej: AWS Secrets Manager o "no definido"]
- nivel de acceso requerido: [MÍNIMO INDISPENSABLE / ELEVADO CON JUSTIFICACIÓN]
- fecha de inicio: [FECHA]
- documentos a revisar: wiki interna, runbooks, guía de arquitectura
- objetivo puntual de salida: checklist de accesos, herramientas y documentación priorizado por día 1 / semana 1, con responsable por ítem
- nivel de profundidad: alto
```

---

## Salida esperada

| Categoría | Ítem | Nivel de acceso / detalle | Responsable | Prioridad |
|---|---|---|---|---|
| Repositorio | Acceso de lectura/escritura a `org/servicio-pagos` | escritura en ramas de feature, sin permiso de push directo a `main` | Admin de la organización en GitHub | Bloqueante día 1 |
| Cloud | Rol IAM `developer-readonly` en cuenta AWS de staging | solo lectura, sin acceso a producción | Lead técnico / administrador IAM | Bloqueante día 1 |
| CI/CD | Acceso de lectura a pipelines de GitHub Actions del repo | ver builds y logs, sin permiso para modificar workflows | Lead técnico | Bloqueante día 1 |
| Gestor de secretos | Acceso al namespace `pagos/staging` en Vault | lectura de secretos de staging únicamente | Responsable de seguridad / DevOps | Semana 1 |
| Comunicación | Alta en canal de Slack del equipo y tablero de Jira | acceso estándar de miembro | Manager directo | Bloqueante día 1 |
| Entorno local | Instalación de Docker, Node LTS del proyecto, linter del equipo | según guía de setup del repo | Nuevo integrante (con soporte del buddy) | Bloqueante día 1 |
| Documentación | Revisión de guía de arquitectura y proceso de code review | lectura y confirmación de comprensión con el buddy | Buddy asignado | Semana 1 |

> Nota: el checklist completo debe cubrir todas las categorías relevantes al rol y al stack indicados (repos, cloud, CI/CD, gestor de secretos, comunicación/gestión, entorno local, documentación), con una fila por ítem, evitando accesos elevados sin justificación explícita.

### Resumen ejecutivo

- **Accesos bloqueantes para el día 1:** [N] ítems — responsables clave a coordinar antes de la fecha de inicio: [LISTA].
- **Accesos/tareas esperables durante la semana 1:** [N] ítems.
- **Gaps detectados:** [documentación faltante, gestor de secretos no formalizado, u otro riesgo señalado durante el relevamiento].
- **Accesos elevados que requieren aprobación adicional:** [LISTA O "ninguno"].
