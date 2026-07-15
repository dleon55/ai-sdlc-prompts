# 17.2 — Checklist de offboarding técnico

## Descripción

Prompt para generar el checklist de offboarding técnico cuando un integrante deja el equipo o la organización: qué accesos hay que revocar (repositorios, cuentas cloud, gestor de secretos, SSO, pipelines de CI/CD), qué conocimiento hay que transferir antes de que la persona se vaya (documentar lo que solo esa persona sabía, reasignar ownership de servicios, repositorios y rotaciones de on-call), y qué credenciales huérfanas hay que verificar (tokens personales, llaves SSH, service accounts creados a su nombre). El prompt no revoca nada por sí mismo: produce el checklist para que lo ejecute un humano con permisos de administración (IAM, SSO, gestor de secretos), con foco explícito en el riesgo de seguridad que representa un acceso olvidado.

**Cuándo usarlo:** en cuanto se confirma la fecha de salida de un integrante del equipo (renuncia, despido, fin de contrato, cambio de equipo con pérdida de accesos), idealmente con antelación suficiente para planificar la transferencia de conocimiento antes del último día. Es la contraparte simétrica de `17-01-onboarding-tecnico`: mientras ese prompt gestiona la incorporación y el otorgamiento inicial de accesos, este gestiona la salida y la revocación completa de los mismos. No sustituye la ejecución real de la revocación (que requiere permisos de administración sobre cada sistema) ni un proceso de RR.HH.: es la capa técnica que asegura que ningún acceso, credencial o conocimiento crítico quede sin cubrir tras la salida.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | seguridad |
| Riesgo esperado | alto — un offboarding técnico incompleto deja accesos activos, tokens vigentes o service accounts huérfanos a nombre de alguien que ya no debería tenerlos, lo cual es una vía directa de fuga de datos o acceso no autorizado; el riesgo es alto aunque el prompt en sí solo genera el checklist, porque el costo de omitir un ítem lo paga la organización, no el prompt |
| Entradas requeridas | rol de la persona que deja el equipo y accesos/sistemas conocidos a los que tenía acceso, servicios/repositorios/rotaciones de on-call de los que es owner o mantenedor, fecha de salida confirmada, lista de sistemas de la organización que gestionan accesos (repos, cloud, gestor de secretos, SSO, CI/CD) |
| Herramientas permitidas | lectura de inventarios de accesos, listas de repositorios y ownership, documentación existente y registros de on-call; la salida es un checklist de texto — no ejecuta revocaciones, no elimina llaves ni deshabilita cuentas en ningún sistema |
| Autonomía permitida | A1 — Proponer (genera el checklist de revocación, transferencia y verificación); nunca A2/A3 — la revocación real de accesos requiere ejecución humana con permisos de administración sobre cada sistema (IAM, SSO, gestor de secretos, CI/CD), y debe completarse antes o el mismo día de la fecha de salida |
| Criterios de detención | detener y escalar si no se conoce la lista completa de accesos o sistemas a los que la persona tenía acceso — señalarlo explícitamente como riesgo residual en vez de asumir una lista completa; detener si no hay fecha de salida confirmada y usar ese hueco como bloqueante para fijar plazos concretos en el checklist |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada ítem del checklist indica el sistema o acceso específico afectado, el responsable de ejecutarlo (rol o persona, no "el equipo"), el plazo (antes/en/después de la fecha de salida) y si depende de otro ítem previo (ej: reasignar ownership antes de revocar el acceso del owner saliente) |
| Siguiente prompt recomendado | `17-01-onboarding-tecnico` — su contraparte simétrica, para la persona que asuma el ownership o la rotación de on-call reasignada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como responsable de seguridad de accesos y operaciones. Genera el checklist completo de offboarding técnico para la persona que deja el equipo, cubriendo revocación de accesos, transferencia de conocimiento y ownership, y verificación de credenciales huérfanas. No ejecutes ninguna revocación: produce el checklist para que lo ejecute un humano con permisos de administración sobre cada sistema.

Entradas:
- persona que deja el equipo (rol/función): [ROL O FUNCIÓN]
- accesos y sistemas conocidos a los que tenía acceso: [REPOSITORIOS / CUENTAS CLOUD / GESTOR DE SECRETOS / SSO / CI-CD / OTRO — o "lista incompleta, requiere levantamiento" si aplica]
- servicios, repositorios o rotaciones de on-call de los que es owner o mantenedor: [LISTA CONOCIDA]
- fecha de salida confirmada: [FECHA]
- sistemas de la organización que gestionan accesos: [PROVEEDOR DE REPOS, PROVEEDOR CLOUD, GESTOR DE SECRETOS, PROVEEDOR SSO, HERRAMIENTA CI/CD]

Pasos:

1. INVENTARIO DE ACCESOS CONOCIDOS
   A partir de las entradas, lista todos los sistemas y accesos conocidos de la persona, agrupados por categoría: repositorios de código, cuentas y roles cloud, gestor de secretos, SSO/identidad, pipelines de CI/CD, herramientas internas (paneles admin, dashboards, colas de mensajería, bases de datos).
   - si la lista de accesos es incompleta o proviene solo de memoria del equipo (no de un inventario centralizado), márcalo explícitamente como "riesgo residual — lista no verificada contra un inventario de accesos" en vez de asumir que está completa.

2. CHECKLIST DE REVOCACIÓN DE ACCESOS
   Para cada acceso identificado en el paso 1, genera un ítem de checklist accionable: sistema/acceso específico, acción a tomar (revocar rol, deshabilitar cuenta, remover de organización/equipo, rotar credencial compartida si la conocía), responsable sugerido (quien tiene permisos de administración sobre ese sistema) y plazo (antes de la fecha de salida, el mismo día, o inmediatamente después si el acceso es necesario hasta el último día).

3. TRANSFERENCIA DE OWNERSHIP
   Para cada servicio, repositorio o rotación de on-call del que la persona es owner o mantenedor, genera un ítem de checklist: qué se transfiere, a quién (persona o equipo receptor, a definir por el responsable si no está identificado), y el plazo para completar la transferencia antes de que se revoque el acceso del owner saliente. Señala explícitamente el orden de dependencia: la transferencia de ownership debe completarse ANTES de revocar el acceso correspondiente, nunca después.

4. TRANSFERENCIA DE CONOCIMIENTO NO DOCUMENTADO
   Identifica y lista qué conocimiento crítico podría existir solo en la cabeza de esta persona (decisiones de diseño no documentadas, procedimientos manuales, contactos externos clave, contraseñas o accesos no gestionados centralmente, contexto histórico de incidentes o decisiones). Para cada ítem, propone una acción concreta de captura (sesión de traspaso documentada, entrada en el wiki/runbook, grabación de walkthrough) con responsable y plazo antes de la fecha de salida.

5. VERIFICACIÓN DE CREDENCIALES HUÉRFANAS
   Genera un checklist de verificación específico para credenciales que puedan sobrevivir a la salida de la persona si no se revisan activamente: tokens de acceso personal (PATs) emitidos a su nombre, llaves SSH asociadas a su cuenta o desplegadas en servidores, service accounts o API keys creadas "a su nombre" o bajo su identidad para automatizaciones, sesiones activas de SSO no cerradas, credenciales compartidas que solo ella conocía. Para cada categoría, indica cómo verificar que no quede ninguna huérfana (auditoría de tokens activos, búsqueda de llaves SSH en `authorized_keys` de servidores relevantes, revisión de service accounts sin dueño claro).

6. ORDEN Y DEPENDENCIAS DEL CHECKLIST
   Ordena el checklist completo respetando dependencias: primero transferencia de ownership y captura de conocimiento (mientras la persona sigue disponible para consultarla), luego revocación de accesos (en o después de la fecha de salida), y por último verificación de credenciales huérfanas (después de la revocación, como control de cierre).

7. RESUMEN EJECUTIVO Y RIESGOS RESIDUALES
   Resume cuántos ítems quedan pendientes por categoría (revocación, transferencia, verificación), cuáles son bloqueantes antes de la fecha de salida, y señala explícitamente cualquier riesgo residual: accesos no inventariados, ownership sin receptor asignado, o sistemas de la organización que no tienen un proceso de revocación centralizado.

Restricciones:
- nunca ejecutes ni simules haber ejecutado una revocación de acceso, eliminación de credencial o cambio de ownership: este prompt solo produce el checklist, la ejecución queda a cargo de una persona con permisos de administración en cada sistema.
- nunca asumas que la lista de accesos de la persona está completa si no proviene de un inventario centralizado verificado: señala la incompletitud como riesgo residual explícito.
- nunca reordenes el checklist de forma que un acceso se revoque antes de que su ownership haya sido transferido a un receptor concreto, salvo que exista una razón de seguridad explícita para hacerlo así (ej: salida por causa disciplinaria).
- si la fecha de salida no está confirmada, dilo explícitamente y usa una fecha placeholder marcada como "PENDIENTE DE CONFIRMAR" en vez de inventar una.
- prioriza siempre los accesos de mayor sensibilidad (cloud con permisos de administración, gestor de secretos, SSO) sobre accesos de baja sensibilidad al ordenar el checklist, incluso si ambos comparten el mismo plazo nominal.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de offboarding técnico y adáptalo a:
- persona que deja el equipo (rol/función): [ROL]
- accesos y sistemas conocidos: [REPOSITORIOS / CLOUD / GESTOR DE SECRETOS / SSO / CI-CD]
- servicios/repositorios/on-call de los que es owner: [LISTA]
- fecha de salida confirmada: [FECHA]
- sistemas de la organización a considerar: [PROVEEDORES CONCRETOS]
- documentos a revisar: inventario de accesos, tabla de ownership de repos/servicios, calendario de on-call
- objetivo puntual de salida: checklist accionable de revocación, transferencia y verificación con responsable y plazo por ítem
- nivel de profundidad: alto
```

---

## Salida esperada

| Categoría | Ítem | Sistema/acceso específico | Responsable | Plazo | Depende de |
|---|---|---|---|---|---|
| Transferencia de ownership | Reasignar ownership del repositorio `payments-service` | GitHub — organización `acme` | Tech lead del equipo de pagos | antes de la fecha de salida | — |
| Transferencia de conocimiento | Documentar el procedimiento manual de reconciliación de pagos fallidos (solo lo conocía esta persona) | Runbook interno / wiki | La persona saliente + tech lead receptor | antes de la fecha de salida | — |
| Revocación de accesos | Remover de la organización y equipos de GitHub | GitHub — organización `acme` | Administrador de GitHub org | el mismo día de la fecha de salida | ownership de `payments-service` ya reasignado |
| Revocación de accesos | Revocar rol IAM y deshabilitar usuario | AWS — cuenta de producción | Administrador cloud/IAM | el mismo día de la fecha de salida | — |
| Revocación de accesos | Deshabilitar cuenta SSO y cerrar sesiones activas | Okta / proveedor SSO | Administrador de identidad | el mismo día de la fecha de salida | — |
| Revocación de accesos | Rotar secretos compartidos que la persona conocía | Gestor de secretos (Vault/1Password) | Administrador del gestor de secretos | en o antes de la fecha de salida | — |
| Verificación de credenciales huérfanas | Auditar y revocar tokens de acceso personal (PATs) emitidos a su nombre | GitHub / GitLab / CI-CD | Administrador de la plataforma correspondiente | inmediatamente después de la revocación de cuenta | cuenta ya deshabilitada |
| Verificación de credenciales huérfanas | Buscar y remover llaves SSH asociadas en servidores relevantes | Servidores de producción / bastion hosts | Equipo de infraestructura | inmediatamente después de la revocación de cuenta | — |
| Verificación de credenciales huérfanas | Identificar service accounts o API keys creadas "a su nombre" y reasignarlas o eliminarlas | Cloud / CI-CD / integraciones internas | Administrador cloud + tech lead receptor | dentro de la semana posterior a la salida | ownership reasignado |

> Nota: la tabla completa debe incluir una fila por cada acceso, ítem de transferencia y verificación identificados, respetando el orden de dependencia (transferencia de ownership y conocimiento primero, revocación después, verificación de credenciales huérfanas al final).

### Resumen ejecutivo

- **Persona y fecha de salida:** [ROL] — salida confirmada el [FECHA].
- **Ítems bloqueantes antes de la fecha de salida:** [N] — principalmente transferencia de ownership y captura de conocimiento no documentado.
- **Accesos de alta sensibilidad a revocar el mismo día:** [LISTA — ej: cloud con permisos admin, gestor de secretos, SSO].
- **Riesgos residuales:** [accesos no inventariados / lista de accesos no verificada contra un inventario centralizado / ownership sin receptor asignado / sistemas sin proceso de revocación centralizado].
- **Próxima verificación recomendada:** auditoría de credenciales huérfanas [N días] después de la fecha de salida, para confirmar que no queden tokens, llaves SSH o service accounts activos a su nombre.
