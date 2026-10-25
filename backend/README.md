# Backend de AI-SDLC Pro

API propia del sitio `prompts.lionsystems.com.mx`: login con GitHub, base de
datos PostgreSQL propia, prueba gratuita, feedback y webhook de Paddle. No
depende de ningún proveedor de backend externo.

No requiere paso de build: corre con el *type stripping* nativo de Node
(`--experimental-strip-types`, Node >= 22.6).

## Rutas

| Ruta | Sesión | Para qué |
|---|---|---|
| `GET /api/auth/login?volver=/ruta` | — | Inicia el login con GitHub; tras él, vuelve a `/ruta` (solo rutas del propio sitio) |
| `GET /api/auth/callback` | — | Vuelta de GitHub; crea la sesión (cookie `httpOnly`) |
| `GET /api/auth/session` | opcional | `{user}` o `{user:null}` |
| `POST /api/auth/logout` | — | Cierra la sesión |
| `GET /api/trial/status` · `POST /api/trial/feedback` | sí | Prueba gratuita y su renovación con feedback |
| `GET/POST/PUT /api/projects` · `DELETE /api/projects/:id` | sí | Proyectos del usuario |
| `GET/PUT /api/project-prompt-state` | sí | Progreso por proyecto y prompt |
| `POST /api/prompt-stats/track` | — | Contador de copias |
| `GET /api/founding/spots-left` | — | Plazas del programa Fundador |
| `POST /api/webhooks/paddle` | firma HMAC | Eventos de suscripción de Paddle |
| `GET /api/health` | — | Salud |

## Producción

- VM `34.51.112.6`, servicio systemd `ai-sdlc-api`, usuario `ai-sdlc-backend`,
  código en `/opt/ai-sdlc-backend/app/backend`, Node 22 dedicado en
  `/opt/ai-sdlc-backend/node` (el Node del sistema es otro y lo usa PM2).
- Escucha solo en `127.0.0.1:8787`; nginx publica `/api/` del mismo dominio.
- Base `ai_sdlc_pro` (rol `ai_sdlc_backend`) en el PostgreSQL nativo de la VM,
  con respaldo diario en `pg_backup.sh`.
- `.env` (root, 600) con `NODE_ENV=production`, `PUBLIC_BASE_URL` y
  `FRONTEND_URL` en HTTPS, la OAuth App de producción y el secreto de la
  notificación de Paddle. Ver `.env.example`.

## Levantarlo en local

1. Postgres: uno propio en `localhost:5432`, o `docker compose up -d`.
2. `cp .env.example .env` y completar como mínimo `DATABASE_URL` y
   `JWT_SIGNING_SECRET` (`node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`).
   Para el login hace falta una OAuth App de GitHub con callback
   `http://localhost:8787/api/auth/callback`.
3. `npm install`
4. `npm run migrate` — aplica `src/schema.sql` (idempotente).
5. `npm run dev`

## Pruebas

```bash
set -a; source .env; set +a
npm test
```

Las de lógica pura corren siempre; las de integración se saltan si no hay
`DATABASE_URL`. El CI del repositorio no ejecuta `backend/`: hay que correrlas
en local antes de abrir el PR.
