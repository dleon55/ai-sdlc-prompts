# Configuración del muro de registro + prueba Pro de 1 semana + feedback

Este feature se apoya en el registro de usuarios ya configurado (ver
[`docs/auth-setup.md`](auth-setup.md)) — si ese feature todavía muestra el
aviso de "no configurado", completa esos pasos primero.

El cliente está implementado en `build.py` (sección `MURO DE REGISTRO /
PRUEBA / FEEDBACK`) y la lógica de servidor en el backend propio
([`backend/src/routes/trial.ts`](../backend/src/routes/trial.ts), API en
`/api/*`, base PostgreSQL `ai_sdlc_pro`).

Si el backend no responde (servicio caído, `/api/` sin publicar en nginx,
error de base de datos), el diseño está pensado para ese caso:
**fail-open** — cualquier error de red o de ruta permite la acción en vez
de bloquearla, y el sitio sigue funcionando desde `localStorage`.

## Rediseño (issue #7, Opción B) — qué cambió y por qué

El repositorio de este proyecto es **público**: el texto completo de los
112 prompts ya es legible por cualquiera en GitHub o vía el servidor MCP,
sin autenticación. Gatear la **copia** de prompts (el diseño original de
este muro, "10 copias anónimas") solo agregaba fricción sin proteger nada
real — cualquier usuario técnico podía evadirlo leyendo el repo.

El muro ahora gatea la **plataforma**, no el texto:
- **Copiar cualquier prompt es siempre gratis e ilimitado**, con o sin
  sesión. `copyResolvedText()` ya no llama a ningún gate.
- **Gestionar más de 1 proyecto** (crear un 2do proyecto o duplicar uno
  existente) requiere sesión + prueba Pro activa o suscripción —
  `requestNewProject()`/`requestDuplicateProject()` llaman a
  `checkProFeatureGate()`.
- **Guardar personalización (`custom_additions`) o resultados de IA
  (`ai_output`)** con contenido no vacío requiere lo mismo —
  `saveGatedPromptField()` llama al mismo gate.
- El proyecto #1 (variables, checklist de progreso, modo guiado) sigue
  siendo gratis para siempre, sin sesión.

`GET /api/trial/status` (usuario con sesión; antes la RPC
`check_trial_status()`) no cambió de criterio: sigue decidiendo si
hay prueba activa o suscripción. Lo que cambió es **desde dónde se llama**
(antes: antes de copiar; ahora: antes de crear el 2do proyecto o guardar
personalización/IA).

El límite de "1 proyecto gratis" en modo anónimo se calcula del lado del
cliente (`loadProjects().length`), sin rastrear IPs, porque el conteo de
proyectos ya vive en `localStorage` de forma visible. Por eso el backend
propio no tiene tabla `anon_usage` ni nada equivalente.

## 1. Rutas y tablas del backend

El esquema vive en [`backend/src/schema.sql`](../backend/src/schema.sql) y
se aplica con `npm run migrate` (idempotente) — no hay paso manual de SQL.

| Ruta | Qué hace |
|---|---|
| `GET /api/trial/status` | Devuelve `{active, expires_at, no_trial_row, subscribed}`. Revisa primero `subscriptions`; si no hay suscripción activa, la fila de `user_trial`. |
| `POST /api/trial/feedback` | `{rating 1..5, comments}`: guarda la fila en `feedback` y renueva `user_trial.trial_expires_at` una semana desde el envío. |
| `POST /api/prompt-stats/track` | Público: incrementa el contador de `prompt_copy_stats` (indicador "prompts más copiados" para el administrador). Nunca bloquea la copia. |

Tablas: `user_trial` (se crea al registrarse el usuario en `users`, vía el
trigger `create_user_trial()`), `feedback` y `prompt_copy_stats`.

## 2. Verificar la regla de seguridad crítica

`user_trial` **nunca es editable por el cliente**: no existe ninguna ruta
que acepte una fecha de vencimiento. La única vía de extender
`trial_expires_at` es `POST /api/trial/feedback`, que exige sesión y
calcula la fecha en el servidor (`now() + interval '1 week'`). La
autorización se aplica en cada ruta del backend (el `user_id` sale siempre
de la cookie de sesión, nunca del cuerpo de la petición); las pruebas de
integración del backend (`backend/test/integration.test.ts`) lo cubren.

## 3. Verificación funcional (manual, no automatizable desde aquí)

1. Abre el sitio en una ventana de incógnito (sin sesión).
2. Copia varios prompts distintos, sin límite — deben copiar normal siempre
   (ya no hay gate de copia).
3. Con 1 proyecto ya creado, intenta crear un 2do proyecto (botón "+ Nuevo"
   o "duplicar") — debe aparecer el muro de registro en vez de crearlo.
4. Intenta escribir algo en "Adiciones personalizadas" o "Resultado de la
   IA" en el modal ⓘ de un prompt — debe aparecer el muro de registro al
   primer carácter no vacío, y el campo debe quedar vacío de nuevo.
5. Inicia sesión con GitHub. Crear un 2do proyecto y guardar
   personalización/IA deben funcionar sin límite mientras la prueba esté
   activa.
6. Para simular el vencimiento sin esperar 1 semana real, en la VM
   (`sudo -u postgres psql ai_sdlc_pro`):
   ```sql
   update user_trial set trial_expires_at = now() - interval '1 day'
   where user_id = (select id from users where github_login = 'tu-usuario-de-prueba');
   ```
7. Recarga el sitio (con la misma sesión) e intenta crear un 2do proyecto —
   debe aparecer el muro de feedback en vez de crearlo (copiar prompts
   sigue funcionando normal, sin verse afectado).
8. Envía el formulario (calificación + comentario) — debe cerrarse el
   modal y crear el 2do proyecto/guardar personalización debe volver a
   funcionar de inmediato.
9. Confirma con `psql` que la fila quedó registrada en `feedback`, y en
   `user_trial` que `trial_expires_at` avanzó ~1 semana desde el envío.
10. En `prompt_copy_stats`, confirma que aparece una fila
    por cada prompt copiado durante esta prueba, con `copy_count` correcto
    (esto sigue registrándose siempre, gratis o Pro, gate o no).

## Notas de diseño (por qué quedó así, no un olvido)

- **Copiar prompts nunca se gatea** — el repositorio es público, así que
  proteger el texto no tiene efecto real; el muro protege la plataforma
  (proyectos múltiples, personalización, resultados de IA), no el
  contenido. Ver `docs/STRATEGY.md`.
- **El límite de 1 proyecto gratis anónimo se evade abriendo varias
  ventanas de incógnito** (cada una con su propio `localStorage` vacío) —
  trade-off aceptado explícitamente: sin contenido real que proteger, el
  costo de hacerlo no vale la pena para la mayoría de usuarios, y los
  compradores objetivo (equipos, agencias) valoran la conveniencia de
  sincronizar entre dispositivos más que evadir un límite de conveniencia.
- **`user_trial` nunca es editable directo por el cliente** — la única vía
  de extender `trial_expires_at` es `POST /api/trial/feedback`, que calcula
  la fecha en el servidor.
- **Fail-open ante errores de red** — una caída transitoria del backend
  nunca bloquea a un usuario real.
- **El servidor MCP (`mcp-server/`) no está cubierto por este muro** — es
  un canal de distribución completamente separado, sin ninguna dependencia
  del backend; dado que copiar prompts ya es gratis en el sitio también,
  esto ya no representa una brecha del modelo de negocio.
