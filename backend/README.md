# Backend propio de AI-SDLC Pro (Fase 1)

Reemplaza auth, base de datos y el webhook de Paddle que hoy vive en
Supabase. Ver
[`docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md`](../docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md)
para el plan completo.

**Estado: Fase 1 (base), corriendo en paralelo a Supabase.** Nada en
producción usa todavía este backend -- el sitio real (`prompts.lionsystems.com.mx`)
sigue hablando con Supabase exactamente como hoy. Este directorio existe
para probar el backend nuevo contra datos de prueba antes de migrar nada
real (Fases 2-4 del plan).

No requiere paso de build: corre con el *type stripping* nativo de Node
(`--experimental-strip-types`, Node >= 22.6), igual que
`supabase/functions/paddle-webhook/alertas.ts` ya lo hace hoy en el resto
del repo (ver `tests/js/test_alertas_runtime.js`).

## Levantarlo en local

1. Postgres: o ya tienes uno corriendo en `localhost:5432`, o levantas el
   de este repo:
   ```bash
   docker compose up -d
   ```
2. `cp .env.example .env` y completar como mínimo `DATABASE_URL` y
   `JWT_SIGNING_SECRET` (generar uno con
   `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`).
   Para probar login real hace falta además una OAuth App de GitHub
   (`GITHUB_OAUTH_CLIENT_ID`/`_SECRET`) cuya **Authorization callback URL**
   sea `http://localhost:8787/api/auth/callback`; sin eso, todo lo demás
   (projects, trial-gate, webhook de Paddle) se puede probar igual
   fabricando una cookie de sesión a mano (ver `npm test` más abajo, que
   hace exactamente eso).
3. `npm install`
4. `npm run migrate` -- aplica `src/schema.sql` (idempotente).
5. `npm run dev`

## Pruebas

```bash
npm test
```

Las pruebas de lógica pura (firma HMAC del webhook, alertas operativas)
corren siempre, sin red ni base de datos. Las de integración
(`test/integration.test.ts`: autorización, trial-gate, idempotencia del
webhook) se saltan automáticamente si `DATABASE_URL` no está configurada
-- para que corran de verdad:

```bash
set -a; source .env; set +a
npm test
```

## Qué falta para que esto reemplace a Supabase de verdad

Ver §7 y §8 del plan. En resumen, lo que vive aquí es solo la Fase 1
(backend + esquema, verificado con datos de prueba); faltan, en orden:
migrar los datos reales conservando los mismos UUID de usuario, mover el
tráfico real del sitio a este backend, actualizar
`.github/workflows/deploy.yml` para desplegarlo, y solo al final tocar
nada relacionado con pagos reales.
