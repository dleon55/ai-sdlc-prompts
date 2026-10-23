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
   `subscription.canceled`, `subscription.past_due` y `adjustment.created`
   (reembolsos y contracargos, ver §7).
4. Paddle te da un **Notification signing secret** (o "Webhook secret") — cópialo.
5. En **Supabase → Edge Functions → paddle-webhook → Secrets** (o vía
   `supabase secrets set`), agrega: nombre `PADDLE_WEBHOOK_SECRET`, valor el
   secreto que copiaste. Este NO va en GitHub ni en el repo.
6. Opcional: en el mismo lugar agrega `ALERTAS_WEBHOOK_URL` (ver §8).
   Para `supabase functions serve` local, copia
   [`supabase/functions/.env.example`](../supabase/functions/.env.example)
   a `supabase/functions/.env` (ignorado por git).

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

## 7. Reembolsos y contracargos

AI-SDLC Pro no ejecuta reembolsos desde código: Paddle es el comerciante
registrado (Merchant of Record) y el reembolso se emite desde su dashboard.
La política pública es la de [`/reembolsos.html`](../reembolsos.html)
(14 días sin preguntas desde el primer cobro); el precio publicado es antes
de impuestos, Paddle aplica el IVA del país del comprador y emite el recibo,
y no se emite CFDI.

Runbook del operador, en este orden:

1. **Reembolsar**: Paddle → Transactions → la transacción → *Refund*
   (total o parcial). Paddle devuelve el importe completo, impuestos
   incluidos, y emite `adjustment.created` con `action = refund`.
2. **Degradar el acceso**: Paddle → Subscriptions → la suscripción →
   *Cancel* (inmediata). Reembolsar **no** cancela la suscripción por sí
   solo. La cancelación emite `subscription.canceled`, la Edge Function
   pone `subscriptions.status = 'canceled'` y `check_trial_status()` deja
   de reportar acceso Pro. Sin este paso el cliente conserva acceso pagado
   por un cobro ya devuelto.
3. **Verificar** en Table Editor → `subscriptions` que la fila quedó en
   `canceled`, y en `paddle_webhook_events` que existen los dos eventos con
   `processed_at` no nulo.

Qué hace la Edge Function con cada evento:

| Evento | Efecto |
|---|---|
| `adjustment.created` (reembolso, crédito o contracargo) | Lo registra en `paddle_webhook_events` como procesado **sin tocar** `subscriptions`, lo escribe en el log y manda la alerta `reembolso` (§8) con el id del ajuste, para que el operador confirme el paso 2. |
| `subscription.canceled` | Degrada el acceso (status `canceled`). Es el único camino por el que un reembolso quita el acceso. |
| Reembolso parcial | Igual que el total: solo registro y alerta; el acceso no cambia. |

Un reembolso o contracargo recibido por `adjustment.created` **nunca**
modifica `subscriptions` desde la función: la función SQL
`apply_paddle_subscription_event` solo cambia estado para eventos
`subscription.%`, así que un ajuste mal interpretado no puede quitar ni dar
acceso.

## 8. Alertas operativas (`ALERTAS_WEBHOOK_URL`)

La Edge Function avisa al operador cuando algo que afecta cobros falla o
merece revisión. Siempre escribe un log estructurado nivel `error`
(Supabase → Edge Functions → paddle-webhook → Logs). Si además existe el
secreto **`ALERTAS_WEBHOOK_URL`** en Supabase (Edge Functions →
paddle-webhook → Secrets, o `supabase secrets set ALERTAS_WEBHOOK_URL=…`),
manda un `POST` JSON a esa URL. Sirve una URL de Slack (incoming webhook),
Discord o cualquier receptor genérico: el cuerpo lleva `text` y `content`
con el resumen, más `producto`, `clave`, `detalle` y `fecha`.

| Clave | Cuándo |
|---|---|
| `webhook_error` | La función va a responder **500**: `apply_paddle_subscription_event` devolvió error o la llamada lanzó una excepción. Paddle reintentará, pero si el error es permanente (migración sin aplicar, evento sin `user_id`) el cliente pagó y no tiene acceso — hay que mirar. |
| `reembolso` | Llegó `adjustment.created` (§7). |

Reglas: la misma clave + `event_id` no se repite durante una hora (los
reintentos de Paddle no inundan el canal); el `detalle` nunca incluye el
cuerpo del webhook, la firma ni ningún secreto (se filtran por nombre de
clave); la URL del destino nunca se escribe en el log (es una credencial);
el `POST` se aborta a los 2.5 s para que un destino colgado no haga que
Paddle dé el webhook por fallido; y `alertar()` nunca lanza — una alerta que
tumba al webhook que la emite es peor que ninguna. Implementación en
[`supabase/functions/paddle-webhook/alertas.ts`](../supabase/functions/paddle-webhook/alertas.ts),
probada en Node con `node tests/js/test_alertas_runtime.js`.

Prueba manual: con `ALERTAS_WEBHOOK_URL` configurada, manda desde Paddle un
*Send test event* de `adjustment.created`; debe llegar un mensaje
`[ai-sdlc-pro] reembolso — …` al canal y una fila nueva en
`paddle_webhook_events`.

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
