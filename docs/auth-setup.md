# Configuración de registro de usuarios (backend propio + GitHub)

El inicio de sesión con GitHub lo implementa el backend propio
([`backend/`](../backend/README.md)): Node 22 + Express, con la base
PostgreSQL `ai_sdlc_pro` en la VM de producción (GCP, región
northamerica-south1, Querétaro, México). El sitio estático solo habla con
`/api/*` en el mismo dominio; nginx publica el servicio `ai-sdlc-api`
(que escucha únicamente en `127.0.0.1:8787`) bajo `/api/`.

Los pasos de esta página requieren una cuenta humana con permisos de
administración (GitHub, acceso root a la VM), por eso quedan documentados
aquí en vez de automatizados.

**El uso anónimo no cambia**: sin cuenta, proyectos, variables y checklist
siguen viviendo en `localStorage` exactamente igual. Si el backend no
responde, el sitio sigue funcionando desde `localStorage` (fail-open).

## 1. Registrar la GitHub OAuth App

1. En GitHub: Settings → Developer settings → OAuth Apps → New OAuth App.
2. **Homepage URL**: `https://prompts.lionsystems.com.mx`.
3. **Authorization callback URL**:
   `https://prompts.lionsystems.com.mx/api/auth/callback` — es el backend,
   no una página del sitio, quien recibe el callback de GitHub.
4. Copiar el **Client ID** y generar un **Client Secret**.

Para desarrollo local, registrar una segunda OAuth App (GitHub admite una
sola callback por app) con callback
`http://localhost:8787/api/auth/callback`. Nunca mezclar las credenciales
de la app local con las de producción.

## 2. Variables de entorno del backend

Plantilla: [`backend/.env.example`](../backend/.env.example).

| Variable | Uso |
|---|---|
| `DATABASE_URL` | Conexión a `ai_sdlc_pro` con el rol `ai_sdlc_backend` |
| `GITHUB_OAUTH_CLIENT_ID` / `GITHUB_OAUTH_CLIENT_SECRET` | OAuth App del paso 1 |
| `JWT_SIGNING_SECRET` | Firma del JWT de sesión. Generar con `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"` |
| `PUBLIC_BASE_URL` | Origen público del backend, sin slash final; la callback es `${PUBLIC_BASE_URL}/api/auth/callback` |
| `FRONTEND_URL` | A dónde vuelve el usuario tras login/logout |
| `PORT` / `HOST` | `8787` / `127.0.0.1` (nginx es la única puerta pública) |
| `NODE_ENV` | `production` en la VM (activa la cookie `Secure`) |
| `PADDLE_WEBHOOK_SECRET`, `ALERTAS_WEBHOOK_URL` | Webhook de Paddle — ver [`paddle-integration.md`](paddle-integration.md) |

**Dónde viven los secretos**: solo en
`/opt/ai-sdlc-backend/app/backend/.env` en la VM (dueño `root`, permisos
`600`). Nunca en el repositorio ni en secretos de GitHub Actions. Tras
cambiar un valor: `sudo systemctl restart ai-sdlc-api`.

El esquema se aplica con `npm run migrate` (idempotente,
`backend/src/schema.sql`).

## 3. Flujo y sesión

- `GET /api/auth/login?volver=/ruta` — redirige a GitHub. `volver` solo
  acepta rutas relativas del mismo sitio; cualquier otra cosa vuelve a `/`.
- `GET /api/auth/callback` — valida el `state`, crea o actualiza el
  usuario en `users` y emite la sesión.
- `GET /api/auth/session` — siempre 200: `{"user": {"id", "githubLogin"}}`
  o `{"user": null}` sin sesión.
- `POST /api/auth/logout` — borra la cookie.

La sesión es un JWT firmado en la cookie `ai_sdlc_session`: `httpOnly`
(JavaScript no puede leerla), `SameSite=Lax` y `Secure` en producción.
No hay token en `localStorage`. La autorización se valida en cada ruta del
backend: cada consulta filtra por el `user_id` de la sesión.

## Verificación tras configurar

1. `systemctl status ai-sdlc-api` en la VM — activo; errores en
   `journalctl -u ai-sdlc-api`.
2. Sin sesión, `curl -s https://prompts.lionsystems.com.mx/api/auth/session`
   debe responder `{"user":null}` (no un 502 de nginx).
3. En el sitio, "Iniciar sesión" → redirige a GitHub → vuelve a la misma
   página con sesión. En las herramientas del navegador, la cookie
   `ai_sdlc_session` aparece con `HttpOnly`, `Secure` y `SameSite=Lax`, y
   `/api/auth/session` ya devuelve `user` con tu `githubLogin`.
4. Con sesión, crear un proyecto; cerrar sesión y volver a entrar (o
   desde otro navegador) → el proyecto debe seguir ahí.
