# Configuración de la integración de pagos (Paddle Billing)

Este feature se apoya en el registro de usuarios y el trial-gate ya
configurados (ver [`docs/auth-setup.md`](auth-setup.md) y
[`docs/trial-gate-setup.md`](trial-gate-setup.md)) — complétalos primero si
no lo has hecho.

Un usuario logueado con GitHub puede suscribirse desde `/precios.html` al
precio vigente (el monto viaja en `PADDLE_PRICE_AMOUNT_USD` junto al price id
de Paddle — nunca hardcodeado en el copy). Al pagar, `check_trial_status()` reporta acceso ilimitado
sin importar el estado de su prueba gratuita — el gate revisa primero la
tabla `subscriptions`, que solo escribe una Supabase Edge Function al
recibir el webhook de Paddle.

## 1. Ejecutar el SQL

Para una instalación nueva, en el SQL Editor de Supabase, después de
`trial_gate.sql`, pega y ejecuta
[`supabase/subscriptions.sql`](../supabase/subscriptions.sql) completo —
crea la tabla `subscriptions` y reemplaza `check_trial_status()` con la
versión que revisa suscripción primero.

Para una instalación que ya ejecutó ese script, aplica solamente
[`supabase/migrations/20260730_paddle_webhook_idempotency.sql`](../supabase/migrations/20260730_paddle_webhook_idempotency.sql).
La migración también registra la fecha del último evento y encapsula el
procesamiento en una función SQL atómica: reintentos concurrentes no aplican
dos veces un cobro y eventos atrasados no sustituyen un estado más reciente.

Después, aplica
[`supabase/migrations/20260809_founding_members.sql`](../supabase/migrations/20260809_founding_members.sql)
(Programa Fundador): agrega `subscriptions.created_at` (orden de llegada de
la cohorte) y el RPC público de solo-conteo `founding_spots_left()` que
alimenta el banner "quedan N de 50" en `/precios`. Sin esta migración el
banner simplemente no aparece (fail-closed) — nada más se rompe.

**Verificación de seguridad**: en **Database → Tables → subscriptions**,
confirma que aparece con **RLS habilitado** y **una sola política**, de
tipo `SELECT`. Si ves `UPDATE`/`INSERT`/`ALL`, algo salió mal: cualquiera
podría auto-otorgarse acceso pagado desde la consola del navegador.

## 2. Generar un token de acceso personal de Supabase (para que CI despliegue la función)

1. Entra a [supabase.com/dashboard/account/tokens](https://supabase.com/dashboard/account/tokens).
2. Genera un token nuevo (dale un nombre como "GitHub Actions — ai-sdlc-prompts").
3. Cópialo — no se vuelve a mostrar completo después.
4. En GitHub: `Settings → Environments → production → Environment secrets`
   (el mismo lugar donde ya tienes `GCP_SSH_KEY`, etc.) → **New secret**:
   nombre `SUPABASE_ACCESS_TOKEN`, valor el token que copiaste.

## 3. Desplegar la Edge Function

Con el secreto ya configurado, el próximo push a `main` despliega
automáticamente `supabase/functions/paddle-webhook/` (job
`deploy-supabase-function` en `deploy.yml`) — no necesitas instalar nada de
Supabase CLI tú mismo.

La URL de la función, una vez desplegada, siempre es:

```
https://sqdzoreqfatpdainlhrm.supabase.co/functions/v1/paddle-webhook
```

## 4. Configurar el webhook en Paddle

1. En tu dashboard de Paddle (Sandbox primero): **Developer Tools → Notifications** (o "Webhooks").
2. Crea un destino nuevo con la URL del paso 3.
3. Suscríbete al menos a: `subscription.created`, `subscription.updated`,
   `subscription.canceled`, `subscription.past_due`.
4. Paddle te da un **Notification signing secret** (o "Webhook secret") — cópialo.
5. En **Supabase → Edge Functions → paddle-webhook → Secrets** (o vía
   `supabase secrets set`), agrega: nombre `PADDLE_WEBHOOK_SECRET`, valor el
   secreto que copiaste. Este NO va en GitHub ni en el repo.

## 5. Configurar el checkout por ambiente

1. En Paddle: **Developer Tools → Authentication → Client-side tokens**.
2. Genera uno para el ambiente correspondiente (Sandbox primero).
3. En GitHub: `Settings > Secrets and variables > Actions > Variables`, crea
   `PADDLE_ENVIRONMENT=sandbox`, `PADDLE_CLIENT_TOKEN=<token test_...>` y
   `PADDLE_PRICE_ID=<pri_...>` para pruebas. Son valores públicos de
   Paddle.js, no API keys ni secretos.
4. El build lee esas variables y valida que los tokens `test_` solo se usen
   con `sandbox`. Para producción usa un token `live_`, un precio live y
   `PADDLE_ENVIRONMENT=production`; si falta alguno, el build falla en lugar
   de publicar un checkout ambiguo.

Mientras ese valor siga en `PENDIENTE_CONFIGURAR`, el botón "Suscribirme"
no intenta abrir un checkout roto — solo avisa "el pago aún no está
disponible", igual que Supabase antes de tener sus claves reales.

## 6. Verificación funcional (manual)

1. En Paddle, usa el botón de **"Send test event"** (o equivalente) sobre
   `subscription.created` sin conectar el checkout real todavía — confirma
   en los logs de la Edge Function (Supabase → Edge Functions →
   paddle-webhook → Logs) que la firma se verificó y no hubo error de DB.
2. Inicia sesión con GitHub en el sitio, ve a `/precios.html`, dale
   "Suscribirme" y completa el checkout de Paddle con una tarjeta de
   prueba (Sandbox).
3. Confirma en **Table Editor → subscriptions** que aparece tu fila con
   `status = 'active'`.
4. Recarga la app — ya no debe pedirte registrarte ni mostrar el muro de
   prueba vencida.
5. Solo cuando todo lo anterior funcione en Sandbox, crea entidades separadas
   en la cuenta **productiva** de Paddle: token `live_`, precio live, destino
   webhook live y `PADDLE_WEBHOOK_SECRET` live en Supabase. Configura el
   dominio aprobado y el default payment link en Paddle antes del deploy.

## Notas de diseño

- **Por qué Edge Function y no un servidor nuevo**: este repo no tenía
  ningún backend propio -- todo pasaba por Supabase (RPC) o por el sitio
  estático. Agregar una Edge Function reutiliza la misma plataforma que ya
  confías con toda la lógica del trial-gate, en vez de sumar un proveedor
  más.
- **Por qué se verifica la firma antes de leer el payload**: sin esto,
  cualquiera podría mandar un POST falso a la URL de la función diciendo
  "ya pagué" y auto-otorgarse acceso ilimitado sin pagar.
- **`PADDLE_WEBHOOK_SECRET` vive solo en Supabase, nunca en GitHub ni en el
  repo** — no cambia en cada deploy, así que no tiene sentido como secreto
  de CI.
- **Protección de webhooks**: la función rechaza firmas vencidas y registra
  `event_id` para reconocer reintentos. La transacción SQL bloquea el evento
  y conserva `last_event_occurred_at` para resistir concurrencia y entregas
  fuera de orden. En instalaciones existentes, ejecuta la migración
  `20260730_paddle_webhook_idempotency.sql` antes de desplegar la función; sin
  ella el webhook responderá con error.
