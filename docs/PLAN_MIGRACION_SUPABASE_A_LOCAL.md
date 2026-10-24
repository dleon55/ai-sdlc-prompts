# Plan de migración: salir de Supabase hacia un backend propio

> **Estado: plan, sin código todavía.** Este documento responde a la
> decisión explícita del propietario del proyecto de no depender de
> Supabase (ver issue #241, origen del análisis: token de CI caducado para
> desplegar la Edge Function `paddle-webhook`). Alcance confirmado: migrar
> **todo** — autenticación, base de datos y el webhook de Paddle —, no solo
> la pieza que falló en CI. No se escribe ni se ejecuta ningún cambio de
> código hasta que este plan se apruebe.

---

## 1. Por qué esto es más grande que "cambiar de base de datos"

Hoy **no existe ningún backend propio**. El sitio es estático
(`index.html` generado por `build.py`, servido por nginx en una VM de
GCP) y el navegador habla **directamente** con Supabase desde JavaScript:

```
Navegador ── (supabase-js, cargado desde cdn.jsdelivr.net) ──▶ Supabase
                                                                 ├─ GoTrue (auth, OAuth con GitHub)
                                                                 ├─ PostgREST (tablas + RPC, protegidas por RLS)
                                                                 └─ Edge Function paddle-webhook (Deno)
```

La única barrera de seguridad hoy es la **Row Level Security (RLS)** de
Postgres — el `anon key` que vive en el HTML público no protege nada por
sí mismo. Quitar Supabase no es reemplazar un driver de base de datos: es
**construir un backend que hoy no existe**, porque alguien tiene que
hacer lo que GoTrue y PostgREST+RLS hacen gratis hoy:

- Hablar con GitHub para el login (OAuth) y emitir una sesión propia.
- Decidir, en cada petición, si ese usuario puede leer/escribir esa fila
  (lo que hoy hace una política RLS).
- Recibir el webhook de Paddle, verificar su firma y aplicar el evento.
- Quedar corriendo 24/7 para responder peticiones (nginx hoy solo sirve
  archivos estáticos, no ejecuta código en cada request).

## 2. Inventario completo de lo que hace Supabase hoy

### 2.1 Autenticación (GoTrue)
- Único proveedor: **GitHub OAuth** (no hay email/password). Ver
  `docs/auth-setup.md`.
- Supabase registra la OAuth App de GitHub, gestiona el `state`/PKCE del
  flujo OAuth, y emite el JWT de sesión que el cliente guarda.

### 2.2 Base de datos (Postgres + PostgREST + RLS)

| Tabla | Filas por | Quién escribe | Protección |
|---|---|---|---|
| `auth.users` | — | GoTrue | gestionada por Supabase, no por nuestro SQL |
| `projects` | usuario | cliente (CRUD directo) | RLS: `auth.uid() = user_id` |
| `project_prompt_state` | proyecto+prompt | cliente (CRUD directo) | RLS indirecta vía `projects.user_id` |
| `user_trial` | usuario | solo funciones `security definer` | RLS: cliente solo lee, nunca escribe |
| `anon_usage` | IP | solo `check_anon_usage()` | RLS: sin políticas de cliente |
| `feedback` | usuario | cliente (solo insert) + lectura propia | RLS: insert/select propios, sin update/delete |
| `subscriptions` | usuario | solo la Edge Function (service role) | RLS: cliente solo lee |
| `paddle_webhook_events` | evento Paddle | solo la Edge Function | RLS: sin políticas de cliente |
| `prompt_copy_stats` | prompt | solo `track_prompt_copy()` | RLS: sin políticas de cliente |

Funciones RPC (`security definer`, ejecutadas por el cliente vía
`supabase.rpc(...)`): `check_trial_status()`, `check_anon_usage()`,
`submit_feedback_and_renew()`, `track_prompt_copy()`,
`founding_spots_left()`, y la función interna
`apply_paddle_subscription_event()` (solo la llama la Edge Function, con
service role). Trigger `on_auth_user_created_trial` crea la fila de
prueba al registrarse.

**No se usa Realtime** de Supabase en ningún lugar del código revisado —
confirmar esto explícitamente no está en el alcance de este documento;
quien apruebe el plan debería confirmarlo o se revisa en la Fase 1.

### 2.3 Edge Function `paddle-webhook` (Deno)
- Verifica la firma HMAC-SHA256 de Paddle (`Paddle-Signature`) sobre el
  cuerpo crudo del request, con ventana de 300 s contra replay.
- Aplica el evento vía `apply_paddle_subscription_event()` (idempotente,
  ordenado por `occurred_at`).
- Envía alertas operativas (`supabase/functions/paddle-webhook/alertas.ts`)
  por log + webhook opcional (Slack/Discord) en fallos y reembolsos.
- **Dato a favor nuestro**: `alertas.ts` ya está escrito sin tocar
  `Deno.*` directamente (recibe `fetch`/reloj/log por inyección,
  justamente para poder probarlo con Node) — se reutiliza casi sin
  cambios en el nuevo backend.

### 2.4 Secretos y configuración actuales relacionados
- `SUPABASE_URL` / `SUPABASE_ANON_KEY` — hardcoded en `build.py`, públicos
  por diseño (línea 2508-2509, 5950-5951).
- `PADDLE_WEBHOOK_SECRET`, `ALERTAS_WEBHOOK_URL` — viven solo en Supabase
  (Edge Function secrets), nunca en GitHub.
- `SUPABASE_ACCESS_TOKEN` — secreto de GitHub Actions, usado solo para que
  CI pueda desplegar la Edge Function (este es el que caducó, issue #241).
- CSP en `nginx_prompts.conf`: `connect-src` incluye
  `https://sqdzoreqfatpdainlhrm.supabase.co` explícitamente.

## 3. Arquitectura propuesta

```
Navegador ──▶ nginx (prompts.lionsystems.com.mx)
                ├─ /            → archivos estáticos (igual que hoy)
                └─ /api/*       → reverse proxy ──▶ backend propio (Node, systemd)
                                                        └─ Postgres local (misma VM o contenedor Docker)
```

Cambios de fondo respecto a hoy:

1. **Un backend nuevo, persistente, con estado** (hoy no existe — nginx
   solo sirve archivos). Alguien tiene que mantenerlo vivo, reiniciarlo si
   se cae, y desplegarlo sin downtime.
2. **Postgres propio** en vez de Supabase-managed: backups, parches de
   seguridad y alta disponibilidad pasan a ser responsabilidad del
   proyecto, no de un proveedor.
3. **RLS se convierte en código de aplicación**: cada endpoint del backend
   debe replicar exactamente la regla de la política equivalente (ver
   tabla §2.2) — un error aquí es un agujero de seguridad real, no una
   advertencia de linter.
4. **OAuth con GitHub implementado a mano**: el backend pasa a manejar el
   `state`/PKCE, el intercambio del código por un token, y a emitir su
   propia sesión (JWT firmado, cookie `httpOnly`+`secure`+`SameSite=Lax`).
5. **El webhook de Paddle pasa a un endpoint propio** (`POST /api/webhooks/paddle`),
   casi una traducción directa de `supabase/functions/paddle-webhook/index.ts`
   de Deno a Node, cambiando el cliente `supabase-js` por consultas SQL
   directas a Postgres.
6. **CSP se simplifica**: `connect-src` ya no necesita el dominio de
   Supabase si el backend vive en el mismo origen vía `/api/*`.

### 3.1 Elección de runtime para el backend: Node (recomendado)

Motivo: la Edge Function ya está en TypeScript/Deno — migrarla a Node es
casi una traducción de imports, no una reescritura de lógica. El repo ya
tiene tooling Node instalado (`mcp-server/`), y el ecosistema de Node para
JWT (`jose`), OAuth y clientes de Postgres (`pg`) es maduro. La alternativa
(Python/FastAPI) es viable pero obligaría a reescribir `alertas.ts` y el
webhook desde cero en otro lenguaje, sin ganar nada a cambio.

### 3.2 Dónde vive Postgres

Pediste revisar primero si ya hay una instalación local en la VM de GCP.
**No puedo verificarlo desde esta sesión** — el acceso SSH a esa VM
(`GCP_SSH_KEY`) es un secreto de GitHub Actions al que este agente no
tiene acceso. Antes de decidir, corre esto en la VM (o pide que lo
corra quien tenga acceso):

```bash
# ¿Hay un Postgres nativo ya corriendo?
systemctl status postgresql 2>&1 | head -5
which psql
psql --version 2>&1

# ¿Hay Docker disponible, por si hay que instalar Postgres en contenedor?
docker --version 2>&1
docker ps 2>&1
```

- **Si ya hay un Postgres nativo activo**: se reutiliza, se crea una base
  de datos y un rol dedicados para este proyecto (sin compartir
  credenciales con lo que ya exista ahí).
- **Si no hay nada**: Postgres en Docker (`docker run` con un volumen
  nombrado para persistencia, o un `docker-compose.yml` versionado en el
  repo junto al backend) — más simple de instalar, actualizar y respaldar
  (`docker exec pg_dump`) que compilar/paquetear Postgres nativo a mano.

## 4. Migración de datos — la parte de mayor riesgo real

Esto no es un ambiente de pruebas: hay **usuarios reales con sesión
iniciada y, sobre todo, suscripciones de pago activas en Paddle**. Un
error aquí puede dejar a un cliente que ya pagó sin acceso, o viceversa.

### 4.1 Identidad: conservar los mismos UUID, no reasignarlos

Paddle ya guarda, para cada suscripción activa, el `custom_data.user_id`
que se le mandó en el checkout — es el UUID de `auth.users` de Supabase.
Si al migrar se le asignan UUID nuevos a los usuarios, **los webhooks
futuros de Paddle para suscripciones que ya existen no van a encontrar a
nadie** (`apply_paddle_subscription_event` fallaría exactamente en el caso
que ya está documentado y manejado en `supabase/subscriptions.sql` líneas
120-148 — evento sin fila local y sin `user_id` para crear una nueva).

Por eso: exportar `auth.users` (al menos `id`, el `provider_id`/`login` de
GitHub, email, fecha de creación) y recrear una tabla `users` propia
**con los mismos UUID**, antes de migrar cualquier tabla que tenga una
`foreign key` hacia `auth.users(id)` (`projects`, `user_trial`, `feedback`,
`subscriptions`).

### 4.2 Pasos de la migración de datos

1. Exportar desde Supabase (Settings → Database → Connection string da
   acceso directo a Postgres, no solo a la API): `pg_dump` de
   `auth.users` (columnas necesarias) y de las 8 tablas propias listadas
   en §2.2.
2. Crear el esquema nuevo en el Postgres propio: mismas tablas, mismas
   `foreign key`, pero **sin RLS** (reemplazada por autorización en el
   backend) y **sin las funciones `security definer`** (reemplazadas por
   lógica del backend, no por funciones SQL invocables desde el cliente).
3. Importar los datos, respetando el orden de las FK (`users` →
   `projects`/`user_trial`/`feedback`/`subscriptions` → `project_prompt_state`).
4. Verificar conteos de filas por tabla, origen vs. destino, uno a uno.
5. Verificar con una muestra manual: tomar 3-5 usuarios con suscripción
   `active` real y confirmar que su fila migrada tiene el mismo
   `paddle_subscription_id` y el mismo UUID de usuario.

### 4.3 Ventana de corte (cutover)

Mientras el backend nuevo no esté verificado en paralelo (ver Fase 1 más
abajo), Supabase sigue siendo la fuente de verdad. El corte real
(apuntar el sitio al backend nuevo) necesita una ventana corta de
"solo lectura" en el sitio actual para que no se pierda ninguna
escritura entre el export y el primer request que ya use el backend
nuevo — su duración exacta depende de qué tan rápido corra el `pg_dump`/
`pg_restore` real, algo que solo se sabe al ejecutarlo.

## 5. CI/CD — qué cambia en `.github/workflows/deploy.yml`

- Se **elimina** el job `deploy-supabase-function` (y con él, la
  dependencia del secreto `SUPABASE_ACCESS_TOKEN` que causó el issue #241).
- Se **agrega** un job `deploy-backend` (nombre tentativo) que: construye
  el backend (`npm ci && npm run build`), lo transfiere a la VM (mismo
  patrón `scp`/SSH que ya usa `deploy-gcp` con `GCP_SSH_KEY`), aplica
  migraciones SQL pendientes contra Postgres, y reinicia el servicio
  (`systemctl restart ai-sdlc-api`, requiere crear la unit de systemd una
  vez, a mano, en la VM).
- Se agrega un smoke test del backend nuevo (`GET /api/health`), en el
  mismo paso donde hoy `deploy-gcp` ya hace smoke tests del sitio estático.
- Secretos nuevos a crear en GitHub (Environment `production`, mismo
  lugar que `GCP_SSH_KEY` hoy): `GITHUB_OAUTH_CLIENT_ID`,
  `GITHUB_OAUTH_CLIENT_SECRET`, `JWT_SIGNING_SECRET`,
  `PADDLE_WEBHOOK_SECRET` (se muda de "secreto de Supabase" a "secreto de
  GitHub Actions, inyectado al `.env` del backend en el deploy"),
  `DATABASE_URL` (o sus partes sueltas si se prefiere no versionar la
  cadena completa como un solo secreto).
- Secretos que **se eliminan** una vez completada la migración:
  `SUPABASE_ACCESS_TOKEN`.

## 6. Seguridad — riesgos nuevos que no existen hoy

Esto es lo más importante de leer antes de aprobar el plan: hoy, el 100%
de la superficie de autenticación y RLS está operada y auditada por
Supabase como proveedor especializado. Al traer esto "a casa", estos
riesgos pasan a ser responsabilidad del proyecto:

1. **OAuth implementado a mano**: `state`/PKCE mal validado = CSRF en el
   login; cookie de sesión mal configurada = robo de sesión. Esto es
   exactamente el tipo de código que, bien hecho, GoTrue ya resolvía por
   nosotros.
2. **RLS reescrita como `if` en cada endpoint**: cada tabla de §2.2 tiene
   una política que hoy es la única barrera contra que un usuario lea o
   edite los datos de otro. Portarla mal (olvidar un filtro `WHERE
   user_id = ...` en un solo endpoint) es una fuga de datos real, no un
   error cosmético.
3. **Postgres expuesto a la red**: si el puerto 5432 queda abierto al
   público en vez de solo a `localhost`/la red interna de la VM, cualquiera
   en internet puede intentar conectarse directamente a la base de pagos.
4. **Un solo punto de falla nuevo**: hoy, si la VM de GCP se cae, el sitio
   estático igual puede servirse desde GitHub Pages (staging) y
   Auth/DB/pagos siguen vivos en Supabase, en otra infraestructura. Con
   todo en la misma VM, una caída de esa VM tumba sitio + login + pagos a
   la vez.
5. **Mantenimiento continuo nuevo**: parches de seguridad de Postgres,
   rotación de `JWT_SIGNING_SECRET`, backups verificados (no solo
   programados) — trabajo operativo recurrente que hoy hace Supabase.

Ninguno de estos es motivo para no hacerlo — son el precio real de la
independencia que se pidió. Se listan para que la decisión de aprobar
este plan sea informada, no para disuadir.

## 7. Fases propuestas (de menor a mayor riesgo)

| Fase | Contenido | Riesgo si algo sale mal |
|---|---|---|
| **1. Base** | Backend nuevo + Postgres propio corriendo en paralelo a Supabase, sin que el sitio real los use todavía. Probar OAuth con GitHub y las rutas CRUD contra datos de prueba. | Ninguno — nada en producción depende de esto aún. |
| **2. Datos sin dinero** | Migrar `users`, `projects`, `project_prompt_state`, `prompt_copy_stats`. Apuntar el sitio al backend nuevo para estas rutas. | Molestia (un usuario pierde proyectos guardados) si la migración de datos falla — recuperable desde el export de Supabase. |
| **3. Trial gate + pagos** | Migrar `user_trial`, `anon_usage`, `feedback`, `subscriptions`, `paddle_webhook_events`; mover el webhook de Paddle al endpoint nuevo; reconfigurar la URL de notificación en el dashboard de Paddle. | El más alto: un error deja a un cliente que pagó sin acceso, o dinero sin registrar. Por eso va al final, con Fases 1-2 ya verificadas. |
| **4. Apagado** | Borrar el proyecto de Supabase (o dejarlo solo como respaldo de lectura un tiempo), quitar `SUPABASE_ACCESS_TOKEN`, actualizar CSP y toda la documentación (`docs/auth-setup.md`, `docs/paddle-integration.md`, `docs/trial-gate-setup.md`, `docs/ARQUITECTURA_PROCESOS.md`). | Bajo, si las fases anteriores ya están verificadas en producción por un tiempo razonable. |

## 8. Pendientes que solo el propietario puede resolver

- [ ] Correr en la VM de GCP el chequeo de §3.2 (Postgres nativo vs.
      Docker) — este agente no tiene acceso SSH a esa máquina.
- [ ] Confirmar que GitHub seguirá siendo el único proveedor de login (no
      se agrega email/password en este rediseño).
- [ ] Decidir la ventana de corte aceptable para la Fase 3 (días/horario
      de menor tráfico de pagos).
- [ ] Aprobar explícitamente el orden de fases de §7, o pedir cambios,
      antes de que se escriba el primer archivo de código del backend.

## 9. Fuera de alcance (no-objetivos)

- No se agregan features nuevas durante la migración — paridad exacta de
  comportamiento con lo que hace Supabase hoy.
- No se evalúan otros proveedores administrados (eso seguiría dependiendo
  de un tercero, que es justo lo que se quiere evitar).
- No se usa Realtime de Supabase hoy según el código revisado, así que no
  se migra ninguna funcionalidad de ese tipo — si en Fase 1 aparece algún
  uso no detectado aquí, se documenta como hallazgo nuevo.
