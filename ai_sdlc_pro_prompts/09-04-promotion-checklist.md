# 9.4 — Promotion checklist: integración y despliegue entre ambientes

## Descripción

Prompt para planificar y documentar la promoción de cambios entre ambientes (dev → qa → staging → prod): verificaciones previas, pasos de despliegue, validaciones post-despliegue, criterios de go/no-go y plan de rollback. Incluye consideraciones para entornos con agentes IA operando.

**Cuándo usarlo:** antes de cualquier despliegue a un ambiente superior, especialmente antes de ir a producción. También útil para definir el proceso estándar de promotion del proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera el checklist completo de promotion para el despliegue de este cambio entre ambientes.

Inputs requeridos:
- repositorio: [NOMBRE O URL]
- cambio a desplegar: [REFERENCIA AL ISSUE O PR]
- rama fuente: [RAMA CON LOS CAMBIOS]
- ambiente origen: [DEV / QA / STAGING]
- ambiente destino: [QA / STAGING / PROD]
- stack de despliegue: [Docker / Kubernetes / VM / GCP / AWS / otro]
- hay migraciones de base de datos: [SÍ / NO]
- hay cambios de infraestructura: [SÍ / NO]
- hay cambios en variables de entorno: [SÍ / NO]

Entrega:

## 1. VERIFICACIONES PREVIAS AL DESPLIEGUE (pre-flight)
### Código y calidad
- [ ] El PR está aprobado por al menos [N] revisores
- [ ] CI/CD pasa en verde: lint, build, tests, coverage
- [ ] No hay secrets ni credenciales expuestas en el diff
- [ ] Revisión de seguridad básica completada (OWASP Top 10 aplicable)
- [ ] Deuda técnica nueva documentada en backlog
- [ ] CHANGELOG.md actualizado con el cambio

### Base de datos (si aplica)
- [ ] Migraciones revisadas y probadas en el ambiente origen
- [ ] Backup del ambiente destino realizado ANTES del despliegue
- [ ] Las migraciones son reversibles o se tiene rollback de datos
- [ ] Scripts de migración probados con dataset representativo

### Variables de entorno (si aplica)
- [ ] Nuevas variables documentadas en .env.example
- [ ] Variables configuradas en el ambiente destino ANTES del despliegue
- [ ] Secretos gestionados en el gestor de secretos (Vault / GitHub Secrets)

### Infraestructura (si aplica)
- [ ] Cambios de infraestructura revisados por el responsable
- [ ] Recursos necesarios disponibles (CPU, memoria, almacenamiento)
- [ ] Configuración de red y firewall validada

### Para agentes IA (si participaron en el cambio)
- [ ] Validación humana del output del agente completada
- [ ] El PR solo toca los archivos del alcance autorizado
- [ ] No hay instrucciones del agente en comentarios del código

## 2. CRITERIOS GO / NO-GO
Define explícitamente qué condiciones DEBEN cumplirse para continuar:

### ✅ GO — Continuar si:
- todos los checks del punto 1 están marcados
- pruebas de humo del ambiente origen pasan
- la ventana de mantenimiento está activa (si aplica)
- hay responsable de rollback disponible durante el despliegue

### 🔴 NO-GO — Detener si:
- algún check crítico del punto 1 falla
- el ambiente destino tiene incidentes activos
- no hay responsable disponible para rollback
- es viernes por la tarde o víspera de fecha importante (regla de higiene operativa)

## 3. PASOS DE DESPLIEGUE
Secuencia exacta y ordenada de comandos o acciones para este cambio.
Por cada paso indica:
- descripción de la acción
- comando o procedimiento exacto
- resultado esperado
- cómo verificar que el paso fue exitoso
- acción de rollback de ese paso si falla

## 4. VALIDACIONES POST-DESPLIEGUE (smoke test mínimo)
- [ ] Aplicación responde HTTP 200 en la URL del ambiente destino
- [ ] Flujos críticos funcionan: [LISTA ESPECÍFICA PARA ESTE CAMBIO]
- [ ] Logs no muestran errores nuevos en los primeros 5 minutos
- [ ] Métricas de performance dentro de los umbrales normales
- [ ] No hay alertas activas en el sistema de monitoreo

## 5. VENTANA DE OBSERVACIÓN
- Tiempo de observación recomendado post-despliegue: [X horas]
- Criterios para cerrar el cambio como exitoso:
  - cero incidentes en la ventana de observación
  - métricas estables
  - validación del solicitante del cambio

## 6. PLAN DE ROLLBACK
- Cuándo ejecutar rollback: [condiciones concretas]
- Pasos de rollback ordenados (inverso al despliegue):
  1. [Paso 1]
  2. [Paso 2]
  ...
- Tiempo estimado de rollback: [X minutos]
- Responsable del rollback: [ROL]
- Notificación post-rollback: [a quién y por qué canal]

## 7. COMUNICACIÓN
- Notificar ANTES del despliegue a: [LISTA]
- Notificar al COMPLETAR a: [LISTA]
- Canal de comunicación de incidentes: [CANAL]
- Decisión de rollback la toma: [ROL / PERSONA]
```

---

## Uso con fórmula estándar

```text
Usa el prompt de promotion checklist y adáptalo a:
- repositorio: [NOMBRE O URL]
- cambio: [REFERENCIA AL ISSUE O PR]
- rama fuente: [RAMA]
- ambiente origen → destino: [ORIGEN → DESTINO]
- stack de despliegue: [STACK]
- migraciones de BD: [SÍ / NO]
- cambios de infraestructura: [SÍ / NO]
- documentos a revisar: CHANGELOG, PR diff, runbooks/, arquitectura
- objetivo puntual de salida: checklist completo go/no-go + pasos de despliegue + plan de rollback
- nivel de profundidad: alto
```

---

## Salida esperada

### Resumen del cambio a desplegar

| Campo | Valor |
|---|---|
| Issue / PR | #[N] |
| Rama | [RAMA] |
| Ambiente destino | [AMBIENTE] |
| Tipo de cambio | feat / fix / refactor / ops |
| Migraciones BD | Sí / No |
| Cambios infra | Sí / No |
| Estimación ventana | [X] minutos de downtime esperado |
| Responsable | [NOMBRE] |
| Rollback disponible | Sí / No |

### Semáforo de go/no-go

| Área | Estado | Observación |
|---|---|---|
| CI/CD verde | 🟢 / 🔴 | |
| Backup BD | 🟢 / 🔴 | |
| Revisores aprobaron | 🟢 / 🔴 | |
| Ambiente destino estable | 🟢 / 🔴 | |
| Responsable rollback presente | 🟢 / 🔴 | |
| **Decisión** | **GO / NO-GO** | |
