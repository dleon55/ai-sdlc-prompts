# Programa early adopters (issue #14)

> Sprint 4, `docs/STRATEGY.md`. El issue original (abril 2026) pedía
> "$99 MXN/mes de por vida" para los primeros 50 Pro — desactualizado: el
> sitio vigente ya tiene un precio introductorio distinto ($1 USD/mes,
> `precios.html`/`terminos.html`). En vez de inventar un tercer número,
> este programa reutiliza el precio real que ya existe y le da la urgencia
> que pedía el issue original: **los primeros 50 aseguran $1 USD/mes de por
> vida**, incluso después de que el precio suba para nuevos usuarios cuando
> termine el piloto. Mismo espíritu del issue (urgencia + trato fundador),
> precio consistente con lo que el sitio ya promete hoy.

## Propuesta del programa

**Nombre:** Programa Fundador / Founding Member Program

**Mecánica:**
- Los primeros 50 usuarios en activar una suscripción Pro ($1 USD/mes)
  quedan marcados como "fundadores".
- Cuando el piloto termine y el precio introductorio suba para usuarios
  nuevos, los 50 fundadores **mantienen $1 USD/mes de por vida** mientras
  la suscripción siga activa sin interrupción.
- No hay una promesa de descuento adicional sobre el precio actual — la
  promesa es **congelar** el precio de hoy, no bajarlo más. Esto es honesto
  con el hecho de que $1 USD/mes ya es un precio introductorio agresivo.

## ⚠️ Limitación técnica real — no implementado todavía

Este documento define el programa a nivel de **producto/mensaje**, no
implementa el mecanismo técnico de "congelar" el precio por usuario. Hoy
`build.py`/Paddle usan un único `PADDLE_PRICE_ID` global (ver
`docs/trial-gate-setup.md` y la config de Paddle en `build.py` línea
~22-39) — no existe todavía un concepto de "precio distinto por cohorte de
usuario" en el checkout real.

Antes de anunciar este programa públicamente hace falta una decisión de
ingeniería (fuera del alcance de este documento, requiere acceso a la
cuenta de Paddle):
- **Opción simple**: Paddle permite crear un segundo `price` para el mismo
  producto y asignarlo manualmente a las primeras 50 suscripciones — no
  requiere cambios de esquema, sí requiere seguimiento manual de quién es
  fundador (ej. una tabla `founding_members` en Supabase, similar a
  `user_trial`).
- **Opción robusta**: automatizar el conteo (trigger en Supabase que marca
  `is_founding_member = true` en la suscripción #1-50) y que el webhook de
  Paddle aplique el price ID correcto según ese flag.

No implemento ninguna de las dos automáticamente en este PR porque cambia
el flujo de cobro real (dinero real, suscripciones reales) — es una
decisión que debe tomarse con acceso a la cuenta de Paddle y confirmación
explícita, no algo para decidir por mi cuenta.

## Copy de campaña (una vez que el mecanismo técnico exista)

**Banner / anuncio corto (ES):**
```
🎖️ Programa Fundador — quedan [N] de 50 lugares
Activa tu Pro hoy a $1 USD/mes y consérvalo de por vida, incluso cuando el
precio suba para nuevos usuarios. Sin trucos: es el mismo precio de hoy,
congelado para siempre mientras tu suscripción siga activa.
```

**Banner / anuncio corto (EN):**
```
🎖️ Founding Member Program — [N] of 50 spots left
Activate Pro today at $1 USD/month and keep it for life, even after the
price goes up for new users. No catch: it's today's price, locked in
forever while your subscription stays active.
```

**Post de LinkedIn para lanzar el programa (ES):**
```
Los primeros 50 usuarios Pro de AI-SDLC Pro se quedan con $1 USD/mes de por
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

- [ ] Decidir el mecanismo técnico de precio congelado (ver limitación
      arriba) — requiere acceso a Paddle, fuera de este documento.
- [ ] Si se implementa, agregar el tracking de "fundador" (tabla o flag en
      Supabase) antes de anunciar el programa — anunciarlo sin poder
      cumplirlo dañaría más que no anunciarlo.
- [ ] Publicar el banner en `/precios` una vez el mecanismo exista (cambio
      de código real en `build.py`, no incluido en este PR).
- [ ] Publicar el post de lanzamiento en LinkedIn.
- [ ] Llevar un contador real de cuántos lugares quedan (dato real de
      Supabase, no un número inventado en el copy).
