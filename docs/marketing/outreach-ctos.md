# Outreach directo a CTOs / Tech Leads (issue #13)

> Sprint 4, `docs/STRATEGY.md`. El issue original (abril 2026) pedía cotizar
> "licencia equipo $799 MXN/mes (hasta 5 devs)" — desactualizado: el sitio
> vigente (`/precios`, `terminos.html`) solo tiene el plan Individual a
> **$1 USD/mes** (introductorio de piloto); el tier de Equipo/Enterprise
> está explícitamente "por definir con datos del piloto" en
> `docs/STRATEGY.md`. Los mensajes de abajo usan el precio real vigente y
> **no inventan un número de equipo** — lo tratan como una conversación
> abierta, no una cotización cerrada, para no contradecir lo que el
> prospecto va a ver si visita el sitio.

## Por qué no incluyo una lista de 20 nombres reales

Identificar 20 CTOs/Tech Leads reales en LinkedIn LATAM requiere buscar en
LinkedIn con una cuenta real (Sales Navigator o búsqueda manual) — no tengo
acceso a LinkedIn ni a ninguna base de datos de contactos, y no voy a
inventar nombres o perfiles falsos para simular que la lista existe. Lo que
sí puedo dejar listo: el criterio de búsqueda, la plantilla de mensaje y el
flujo de seguimiento, para que armar la lista real sea rápido.

## Criterio de búsqueda (para armar la lista real en LinkedIn)

- **Cargo**: CTO, VP Engineering, Head of Engineering, Tech Lead, Engineering Manager.
- **Región**: LATAM (México primero — mismo mercado que la moneda del pricing actual, luego Colombia/Argentina/Chile).
- **Señal de encaje**: empresa con equipo de 3-15 devs (según buyer persona de `docs/STRATEGY.md`), stack visible que usa GitHub/GitLab, menciones de "IA"/"Copilot"/"agentes" en su actividad reciente de LinkedIn (mayor probabilidad de respuesta).
- **Evitar**: perfiles sin actividad en los últimos 3 meses (baja probabilidad de leer un DM frío).

## Plantilla de mensaje — primer contacto (LinkedIn DM)

**ES:**
```
Hola [NOMBRE] — vi que [empresa] usa [Copilot/Claude/IA] en el equipo de
ingeniería. Te escribo porque construí algo que puede ahorrarles la fricción
de que cada dev le dé contexto distinto al agente de IA en cada tarea.

Es una biblioteca de 112 prompts estructurados por fase del SDLC (no
prompts sueltos) — cada uno declara qué riesgo tiene y cuánta autonomía
puede tener el agente. La usan equipos que quieren que "usar IA bien" no
dependa de qué tan senior es cada dev.

Está gratis para probar sin cuenta: prompts.lionsystems.com.mx — si quieres
te muestro en 15 min cómo lo usaríamos con el stack de [empresa]
específicamente, sin compromiso.

¿Te late una llamada corta esta semana o la que sigue?
```

**EN:**
```
Hi [NAME] — saw that [company] uses [Copilot/Claude/AI] on the engineering
team. Reaching out because I built something that can save the friction of
every dev giving the AI agent different context on every task.

It's a library of 112 prompts structured by SDLC phase (not loose prompts)
— each one declares its risk level and how much autonomy the agent gets.
Teams use it so "using AI well" doesn't depend on how senior each dev is.

Free to try, no account needed: prompts.lionsystems.com.mx — happy to show
you in 15 min how we'd apply it to [company]'s specific stack, no strings
attached.

Up for a quick call this week or next?
```

## Plantilla — seguimiento si no responde (7 días después)

**ES:**
```
[NOMBRE], sé que estás ocupado — solo quería dejarte esto por si sirve: la
biblioteca completa (112 prompts, framework de contexto multi-agente) sigue
gratis y sin cuenta en prompts.lionsystems.com.mx. Si en algún momento tu
equipo quiere estandarizar cómo usan IA, aquí ando.
```

**EN:**
```
[NAME], I know you're busy — just wanted to leave this in case it's useful:
the full library (112 prompts, multi-agent context framework) is still free
and account-free at prompts.lionsystems.com.mx. If your team ever wants to
standardize how they use AI, I'm around.
```

## Conversación de propuesta de equipo (para la llamada, NO como mensaje frío)

No cotizar un precio de equipo en el mensaje inicial — el tier de equipo
todavía no existe formalmente. En la llamada, si hay interés real:

```
Ahora mismo el plan individual está a $1 USD/mes, precio introductorio
mientras validamos el piloto. Para equipos como el de ustedes ([3-15] devs)
todavía estamos definiendo el tier — si les interesa, los primeros equipos
en sumarse ayudan a definir qué necesitan (SSO, proyectos compartidos,
miembros) y se quedan con condiciones preferenciales cuando el tier de
equipo se formalice. No es una promesa de descuento fijo — es una invitación
a ser parte del piloto antes de que el precio de equipo esté cerrado.
```

Esto es intencional: prometer $799 MXN/mes por escrito y luego lanzar el
tier de equipo con otro precio (o sin ese precio) dañaría la credibilidad
más de lo que ayudaría a cerrar una conversación. Ver
`docs/STRATEGY.md` → "Decisiones registradas" para el criterio de honestidad
ya aplicado en #7 y #9.

## Checklist de ejecución

- [ ] Armar la lista real de 20 CTOs/Tech Leads en LinkedIn con el criterio
      de arriba (tarea manual, requiere cuenta de LinkedIn).
- [ ] Personalizar `[empresa]`/`[stack]` por prospecto antes de enviar —
      nunca mandar la plantilla genérica tal cual.
- [ ] Registrar respuestas/no-respuestas en una hoja de seguimiento (no
      versionada aquí — datos de prospectos no van al repo).
- [ ] Seguimiento a los 7 días si no hay respuesta; no insistir más de 2
      veces sin respuesta.
- [ ] Si hay ≥3 conversaciones con interés real en tier de equipo, eso es
      la señal para formalizar el precio (con datos reales, no adivinado)
      y actualizar `docs/STRATEGY.md` + `/precios`.
