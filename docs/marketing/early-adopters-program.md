# Programa early adopters (issue #14)

> Sprint 4, `docs/STRATEGY.md`. El issue original (abril 2026) pedía
> "$99 MXN/mes de por vida" para los primeros 50 Pro — desactualizado: el
> sitio vigente tiene su propio precio introductorio, publicado en
> `/precios` (**$9 USD/mes al 2026-08-09**, ancla de lista $19 — la página
> deriva el monto de `PADDLE_PRICE_AMOUNT_USD`, así que `/precios` es
> siempre la fuente de verdad; verificar ahí antes de publicar cualquier
> copy). En vez de inventar otro número, este programa reutiliza el precio
> real vigente y le da la urgencia que pedía el issue original: **los
> primeros 50 aseguran el precio de hoy de por vida**, incluso después de
> que suba para nuevos usuarios cuando termine el piloto. Mismo espíritu
> del issue (urgencia + trato fundador), precio consistente con lo que el
> sitio promete.

## Propuesta del programa

**Nombre:** Programa Fundador / Founding Member Program

**Mecánica:**
- Los primeros 50 usuarios en activar una suscripción Pro (al precio
  introductorio vigente de `/precios`) quedan marcados como "fundadores".
- Cuando el piloto termine y el precio introductorio suba para usuarios
  nuevos, los 50 fundadores **mantienen el precio con el que entraron, de
  por vida**, mientras la suscripción siga activa sin interrupción.
- No hay una promesa de descuento adicional sobre el precio actual — la
  promesa es **congelar** el precio de hoy, no bajarlo más. Esto es honesto
  con el hecho de que el introductorio ya es agresivo frente al ancla de
  lista.

## ✅ Mecanismo técnico — decidido 2026-08-09

El "precio congelado" **no requiere implementación en el flujo de cobro**:
es el comportamiento por defecto de Paddle Billing. Cambiar un precio (o
crear uno nuevo) solo afecta a las suscripciones **nuevas** — las activas
siguen cobrándose al monto con el que se crearon, indefinidamente, salvo
migración explícita suscripción por suscripción vía API. Las dos opciones
que este documento planteaba originalmente (segundo price manual / webhook
con price por flag) resolvían un problema que Paddle ya resuelve solo.

El mecanismo operativo completo es:

1. **Hoy**: nada que cambiar en Paddle. Toda suscripción al precio vigente
   queda congelada por defecto.
2. **Cuando termine el piloto y el precio suba**: crear un price **nuevo**
   en Paddle para el mismo producto (no editar el actual — así el price ID
   introductorio queda como marcador limpio de la cohorte), actualizar la variable
   `PADDLE_PRICE_ID` en GitHub Actions y redeployar. Los checkouts nuevos
   cobran el precio nuevo; nadie existente cambia.
3. **Cumplir la promesa Fundador** = nunca migrar esas suscripciones.
4. **Suscriptores 51+ que entren antes de la subida** (decisión de producto,
   opción "a"): también conservan su precio por el mismo default de Paddle. La
   garantía *pública* es solo para los primeros 50; el resto recibe más de
   lo prometido, nadie recibe menos. No se migrará activamente a nadie.

Lo que sí se implementó (porque faltaba de verdad) es el **tracking de la
cohorte y el contador real**:

- `subscriptions.created_at` (migración
  `supabase/migrations/20260809_founding_members.sql`): orden de llegada,
  fijado al primer insert, nunca pisado por el upsert del webhook. Los
  primeros 50 por `created_at` son la cohorte fundadora.
- RPC `founding_spots_left()`: expone solo el agregado `{left, total}` para
  el banner de `/precios` — dato real, jamás filas de usuarios. Un lugar se
  consume al crearse la suscripción y no se libera al cancelar.
- Banner Fundador en `/precios` (`build.py`): oculto por defecto,
  fail-closed — solo aparece si el RPC devuelve lugares disponibles reales
  y el checkout de Paddle está configurado.

## Copy de campaña

> El monto citado abajo ($9 USD/mes) es el vigente al 2026-08-09 — el banner
> real de `/precios` lo deriva automáticamente de la configuración, pero
> este copy estático no: **verificar contra `/precios` antes de publicar**.

**Banner / anuncio corto (ES):**
```
🎖️ Programa Fundador — quedan [N] de 50 lugares
Activa tu Pro hoy a $9 USD/mes y consérvalo de por vida, incluso cuando el
precio suba para nuevos usuarios. Sin trucos: es el mismo precio de hoy,
congelado para siempre mientras tu suscripción siga activa.
```

**Banner / anuncio corto (EN):**
```
🎖️ Founding Member Program — [N] of 50 spots left
Activate Pro today at $9 USD/month and keep it for life, even after the
price goes up for new users. No catch: it's today's price, locked in
forever while your subscription stays active.
```

**Post de LinkedIn para lanzar el programa (ES):**
```
Los primeros 50 usuarios Pro de AI-SDLC Pro se quedan con $9 USD/mes de por
vida — aunque el precio suba después para quien se una más tarde.

No es un descuento temporal. Es congelar el precio de hoy para quien confía
primero.

Después de esos 50, el precio Pro sigue siendo el que esté vigente en el
piloto — sin sorpresas, sin letra chica.

Prueba el catálogo completo gratis (112 prompts, sin cuenta) y decide si
quieres ser de los primeros 50: https://prompts.lionsystems.com.mx

#IA #StartupBuilding #SoftwareEngineering
```

## Checklist de ejecución

- [x] Decidir el mecanismo técnico de precio congelado — **decidido
      2026-08-09** (ver sección "Mecanismo técnico" arriba): grandfathering
      por defecto de Paddle + price nuevo al subir + nunca migrar
      fundadores.
- [x] Tracking de "fundador" en Supabase — `subscriptions.created_at` +
      RPC `founding_spots_left()`
      (`supabase/migrations/20260809_founding_members.sql`).
- [x] Banner en `/precios` (`build.py`) — oculto hasta que el contador
      real devuelva lugares disponibles y el checkout esté configurado.
- [ ] **Ejecutar la migración** `20260809_founding_members.sql` en el SQL
      Editor de Supabase (instalación existente — un solo paso manual).
- [ ] Publicar el post de lanzamiento en LinkedIn (manual, cuenta del
      propietario).
