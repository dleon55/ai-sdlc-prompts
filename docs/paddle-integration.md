# Configuración de la integración de pagos (Paddle Billing)

Este feature se apoya en el registro de usuarios y el trial-gate ya
configurados (ver [`docs/auth-setup.md`](auth-setup.md) y
[`docs/trial-gate-setup.md`](trial-gate-setup.md)) — complétalos primero si
no lo has hecho.

Un usuario logueado con GitHub puede suscribirse desde `/precios.html` al
precio vigente (el monto viaja en `PADDLE_PRICE_AMOUNT_USD` junto al price id
de Paddle — nunca hardcodeado en el copy). Al pagar, `GET /api/trial/status`
reporta acceso ilimitado sin importar el estado de su prueba gratuita — el
gate revisa primero la tabla `subscriptions`, que solo escribe el backend
propio al recibir el webhook de Paddle
([`backend/src/routes/webhooks/paddle.ts`](../backend/src/routes/webhooks/paddle.ts)).
El checkout envía `customData: { user_id }` con el UUID del usuario en el
backend propio (tabla `users`).

## 1. Esquema

Todo el esquema vive en [`backend/src/schema.sql`](../backend/src/schema.sql)
y se aplica con `npm run migrate` (idempotente) — no hay paso manual de
SQL. Incluye la tabla `subscriptions` (con `created_at`, orden de llegada
de la cohorte del Programa Fundador), `paddle_webhook_events` (registro
idempotente por `event_id`) y la función SQL atómica
`apply_paddle_subscription_event`: reintentos concurrentes no aplican dos
veces un cobro y eventos atrasados no sustituyen un estado más reciente.

El banner "quedan N de 50" en `/precios` lo alimenta la ruta pública de
solo-conteo `GET /api/founding/spots-left`. Si no responde, el banner
simplemente no aparece (fail-closed) — nada más se rompe.

**Seguridad**: no existe ninguna ruta que permita al cliente escribir en
`subscriptions`; solo el webhook firmado la modifica. La autorización se
aplica en cada ruta del backend, nunca desde el navegador.

## 2. Despliegue del backend

El despliegue del backend sigue siendo **manual** (todavía no hay job de
CI): se copia el código (no requiere build) a la VM, se ejecuta
`npm ci --omit=dev` y `sudo systemctl restart ai-sdlc-api`. El servicio
escucha solo en `127.0.0.1:8787`; nginx lo publica en `/api/` con límite de
10 peticiones/s por IP (ráfaga 30).

## 3. URL del webhook

```
https://prompts.lionsystems.com.mx/api/webhooks/paddle
```

## 4. Configurar el webhook en Paddle

1. En tu dashboard de Paddle (Sandbox primero): **Developer Tools → Notifications** (o "Webhooks").
2. Crea un destino nuevo con la URL del paso 3.
3. Suscríbete al menos a: `subscription.created`, `subscription.updated`,
   `subscription.canceled`, `subscription.past_due` y `adjustment.created`
   (reembolsos y contracargos, ver §7).
4. Paddle te da un **Notification signing secret** (o "Webhook secret") — cópialo.
5. En la VM, agrega `PADDLE_WEBHOOK_SECRET=<el secreto que copiaste>` a
   `/opt/ai-sdlc-backend/app/backend/.env` (root, `600`) y reinicia con
   `sudo systemctl restart ai-sdlc-api`. Este NO va en GitHub ni en el repo.
6. Opcional: en el mismo `.env` agrega `ALERTAS_WEBHOOK_URL` (ver §8).
   Para desarrollo local, copia
   [`backend/.env.example`](../backend/.env.example) a `backend/.env`
   (ignorado por git).

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
disponible".

## 6. Verificación funcional (manual)

1. En Paddle, usa el botón de **"Send test event"** (o equivalente) sobre
   `subscription.created` sin conectar el checkout real todavía — confirma
   en los logs del backend (`journalctl -u ai-sdlc-api` en la VM) que la
   firma se verificó y no hubo error de DB.
2. Inicia sesión con GitHub en el sitio, ve a `/precios.html`, dale
   "Suscribirme" y completa el checkout de Paddle con una tarjeta de
   prueba (Sandbox).
3. Confirma con `psql` en la VM (`sudo -u postgres psql ai_sdlc_pro`) que
   aparece tu fila en `subscriptions` con `status = 'active'`.
4. Recarga la app — ya no debe pedirte registrarte ni mostrar el muro de
   prueba vencida.
5. Solo cuando todo lo anterior funcione en Sandbox, crea entidades separadas
   en la cuenta **productiva** de Paddle: token `live_`, precio live, destino
   webhook live y `PADDLE_WEBHOOK_SECRET` live en el `.env` del backend. Configura el
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
   (total o parcial). Paddle devuelve el importe reembolsado más el
   impuesto que le corresponde, y emite `adjustment.created` con
   `action = refund`.
2. **Degradar el acceso**: Paddle → Subscriptions → la suscripción →
   *Cancel* (inmediata). Reembolsar **no** cancela la suscripción por sí
   solo. La cancelación emite `subscription.canceled`, el webhook del
   backend pone `subscriptions.status = 'canceled'` y `GET /api/trial/status`
   deja de reportar acceso Pro. Sin este paso el cliente conserva acceso pagado
   por un cobro ya devuelto.
3. **Verificar** con `psql` en `subscriptions` que la fila quedó en
   `canceled`, y en `paddle_webhook_events` que existen los dos eventos con
   `processed_at` no nulo.

Qué hace el webhook del backend con cada evento:

| Evento | Efecto |
|---|---|
| `adjustment.created` (reembolso, crédito o contracargo) | Lo registra en `paddle_webhook_events` como procesado **sin tocar** `subscriptions`, lo escribe en el log y manda la alerta `reembolso` (§8) con el id del ajuste, para que el operador confirme el paso 2. |
| `subscription.canceled` | Degrada el acceso (status `canceled`). Es el único camino por el que un reembolso quita el acceso. |
| Reembolso parcial | Igual que el total: solo registro y alerta; el acceso no cambia. |

Un reembolso o contracargo recibido por `adjustment.created` **nunca**
modifica `subscriptions` desde el webhook: la función SQL
`apply_paddle_subscription_event` solo cambia estado para eventos
`subscription.%`, así que un ajuste mal interpretado no puede quitar ni dar
acceso.

## 8. Alertas operativas (`ALERTAS_WEBHOOK_URL`)

El webhook del backend avisa al operador cuando algo que afecta cobros
falla o merece revisión. Siempre escribe un log estructurado nivel `error`
(`journalctl -u ai-sdlc-api` en la VM). Si además existe
**`ALERTAS_WEBHOOK_URL`** en `/opt/ai-sdlc-backend/app/backend/.env`,
manda un `POST` JSON a esa URL. Sirve una URL de Slack (incoming webhook),
Discord o cualquier receptor genérico: el cuerpo lleva `text` y `content`
con el resumen, más `producto`, `clave`, `detalle` y `fecha`.

| Clave | Cuándo |
|---|---|
| `webhook_error` | El webhook va a responder **500** ("DB error"): `apply_paddle_subscription_event` devolvió error o la llamada lanzó una excepción. Paddle reintentará, pero si el error es permanente (esquema sin aplicar, evento sin `user_id`) el cliente pagó y no tiene acceso — hay que mirar. |
| `reembolso` | Llegó `adjustment.created` (§7). |

Reglas: la misma clave + `event_id` no se repite durante una hora (los
reintentos de Paddle no inundan el canal); el `detalle` nunca incluye el
cuerpo del webhook, la firma ni ningún secreto (se filtran por nombre de
clave); la URL del destino nunca se escribe en el log (es una credencial);
el `POST` se aborta a los 2.5 s para que un destino colgado no haga que
Paddle dé el webhook por fallido; y `alertar()` nunca lanza — una alerta que
tumba al webhook que la emite es peor que ninguna. Implementación en
[`backend/src/routes/webhooks/alertas.ts`](../backend/src/routes/webhooks/alertas.ts),
probada con `npm test` en `backend/`.

Prueba manual: con `ALERTAS_WEBHOOK_URL` configurada, manda desde Paddle un
*Send test event* de `adjustment.created`; debe llegar un mensaje
`[ai-sdlc-pro] reembolso — …` al canal y una fila nueva en
`paddle_webhook_events`.

## Notas de diseño

- **Por qué un backend propio**: el sitio dejó de depender de proveedores
  externos de auth y base de datos (issue #241). El webhook vive en el mismo servicio `ai-sdlc-api` que la
  autenticación y el trial-gate, junto a la base `ai_sdlc_pro` en la VM de
  producción — un solo proveedor (Google Cloud, en México) en vez de dos.
- **Por qué se verifica la firma antes de leer el payload**: sin esto,
  cualquiera podría mandar un POST falso a la URL del webhook diciendo
  "ya pagué" y auto-otorgarse acceso ilimitado sin pagar.
- **`PADDLE_WEBHOOK_SECRET` vive solo en el `.env` del backend en la VM,
  nunca en GitHub ni en el repo** — no cambia en cada deploy, así que no tiene sentido como secreto
  de CI.
- **Protección de webhooks**: la firma `Paddle-Signature` (`ts=…;h1=…`)
  es un HMAC sobre `${ts}:${rawBody}`; se rechazan firmas con más de 300 s
  de antigüedad y se registra `event_id` para reconocer reintentos. La
  transacción SQL bloquea el evento y conserva `last_event_occurred_at`
  para resistir concurrencia y entregas fuera de orden. Si el esquema no
  está aplicado (`npm run migrate`), el webhook responderá con error 500 y
  Paddle reintentará.
- **Respaldos**: `ai_sdlc_pro` entra en el `pg_backup.sh` diario de la VM
  (03:00, replicado a GCS).
