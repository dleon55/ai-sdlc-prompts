# Lanzamiento en ProductHunt (issue #12)

> Sprint 3, `docs/STRATEGY.md`: "preparación semana 6-7, lanzamiento semana
> 8". Este doc cubre todo lo que se puede preparar desde el repo/contenido;
> los pasos que requieren la cuenta real de ProductHunt (crear el listing,
> coordinar el hunter, publicar el día D) son manuales — ver checklist al
> final.

## Checklist (del issue)

- [x] Tagline
- [x] Descripción
- [x] Comentario de apertura (primer comentario del maker)
- [x] Assets — capturas reales de la app (`docs/marketing/assets/`)
- [ ] Assets — GIF demo (requiere grabación de pantalla real, no generable
      desde este repo)
- [ ] Hunter — coordinar con alguien de perfil relevante en PH que publique
      el producto (decisión humana, fuera de alcance del repo)
- [ ] Comunidad de apoyo — lista de contactos/canales a avisar el día del
      lanzamiento (decisión humana)
- [ ] Fecha de lanzamiento confirmada (recomendado: martes-jueves, según
      práctica estándar de PH — mayor tráfico que lunes/viernes)

## Tagline (máx. ~60 caracteres en PH)

**ES:** `Prompts de ingeniería de software para dirigir cualquier IA`
**EN:** `Structured software-engineering prompts for any AI agent`

Alternativas:
- `115 prompts para dirigir Copilot y Claude como un ingeniero senior`
- `The prompt library that runs your AI agent through the full SDLC`

## Descripción (para el listing, ~250-300 caracteres funciona bien en PH)

**ES:**
```
AI-SDLC Pro es una biblioteca de 115 prompts estructurados (español + inglés)
que dirige agentes IA — Copilot, Claude, Cursor, Windsurf, Codex — a través
de todo el ciclo de ingeniería de software: requerimientos, diseño, código,
pruebas, revisión, operaciones. Cada prompt declara su nivel de riesgo y
autonomía permitida. Gratis, sin cuenta, copia y pega.
```

**EN:**
```
AI-SDLC Pro is a library of 115 structured prompts (Spanish + English) that
steer AI agents — Copilot, Claude, Cursor, Windsurf, Codex — through the
full software engineering lifecycle: requirements, design, code, testing,
review, operations. Every prompt declares its risk level and allowed
autonomy. Free, no account needed, copy and paste.
```

## Comentario de apertura del maker

**ES:**
```
¡Hola Product Hunt! 👋

Construí AI-SDLC Pro porque me cansé de reescribir el mismo contexto en
cada prompt que le daba a mi agente de IA — y de ver que cada dev de mi
equipo lo hacía distinto, con resultados distintos.

Lo que hace diferente a esta biblioteca:

→ 115 prompts organizados por las 18 etapas reales del SDLC, no prompts
  sueltos sin estructura
→ Cada prompt declara su nivel de riesgo y cuánta autonomía puede tener el
  agente (¿solo puede opinar? ¿puede ejecutar cambios?)
→ Un framework de contexto multi-agente que funciona igual con Copilot,
  Claude, Cursor, Windsurf o Codex — mismo "cerebro compartido" para todos
→ 19 variables de proyecto reutilizables entre prompts, para no repetir
  contexto en cada copia
→ Todo el catálogo es gratis, sin cuenta, copiar y pegar

Es completamente gratis usarlo — el catálogo es público y va a seguir
siéndolo. Si gestionas varios proyectos, hay una capa opcional con sesión
de GitHub (prueba de 1 semana incluida) para eso, pero el contenido en sí
nunca está detrás de un muro.

Me encantaría leer qué tareas repiten más en su flujo con IA y que todavía
no tienen un prompt estandarizado — lo agrego con gusto.

¡Gracias por pasar! 🙌
```

**EN:**
```
Hey Product Hunt! 👋

I built AI-SDLC Pro because I got tired of rewriting the same context in
every prompt I gave my AI agent — and of watching every dev on my team do
it differently, with different results.

What makes this different:

→ 115 prompts organized by the 18 real stages of the SDLC, not loose
  prompts with no structure
→ Every prompt declares its risk level and how much autonomy the agent
  gets (can it only suggest? can it execute changes?)
→ A multi-agent context framework that works the same with Copilot,
  Claude, Cursor, Windsurf, or Codex — one shared "brain" for all of them
→ 19 reusable project variables so you don't repeat context on every copy
→ The whole catalog is free, no account, copy and paste

It's completely free to use — the catalog is public and will stay that way.
If you manage multiple projects, there's an optional layer behind a GitHub
session (1-week trial included) for that, but the content itself is never
behind a wall.

I'd love to hear what tasks you repeat most in your AI workflow that don't
have a standardized prompt yet — happy to add it.

Thanks for stopping by! 🙌
```

## Assets disponibles

| Archivo | Uso sugerido en el listing |
|---------|----------------------------|
| `assets/01-catalogo-general.png` | Imagen principal / gallery #1 — vista general del catálogo |
| `assets/02-modal-formula-uso.png` | Gallery #2 — detalle de un prompt (fórmula de uso, riesgo, autonomía) |
| `assets/03-panel-variables.png` | Gallery #3 — variables de proyecto reutilizables |

PH recomienda 3-5 imágenes en el gallery más un GIF corto (10-20s) mostrando
el flujo completo: elegir prompt → copiar → pegar en el agente. El GIF no
se puede generar desde este repo (requiere grabación real de pantalla con
audio/interacción humana) — pendiente de grabar antes del lanzamiento.

## Notas de honestidad (mismo criterio que #7 y #9)

El copy de arriba NO promete "contenido exclusivo" ni usa lenguaje de
paywall — el repo es público, así que cualquier claim de exclusividad sería
falso y fácil de desmentir por la propia comunidad técnica de PH. El pitch
real es: biblioteca curada + estructura de ingeniería real, no cantidad de
prompts genéricos.
