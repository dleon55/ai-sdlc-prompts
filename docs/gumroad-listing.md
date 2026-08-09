# Listado de Gumroad — Pack completo AI-SDLC Pro

> **Estado: canal de adquisición ratificado el 2026-08-09** (ver "Decisiones
> registradas" en `docs/STRATEGY.md`). Esta decisión reemplaza el archivo del
> 2026-08-02: Gumroad opera como canal de **adquisición**, no de ingreso — el
> producto es "pay what you want" con mínimo $0 y su `LEEME.md` dirige a la
> suscripción de la plataforma ($1 USD/mes vía Paddle).
>
> Este documento es solo texto de referencia para crear el producto
> manualmente en https://gumroad.com — no hay forma de publicarlo desde este
> repositorio (Gumroad no ofrece una API de creación de producto sin las
> credenciales de la cuenta del propietario). El archivo a subir como
> "contenido" del producto es `dist/ai-sdlc-pro-pack-completo.zip`, generado
> con `python3 build_gumroad_pack.py` (ver ese script para regenerarlo con
> el catálogo más reciente antes de publicar).

## Datos del producto

| Campo | Valor |
|-------|-------|
| Nombre | AI-SDLC Pro — Pack completo de prompts |
| Precio | **"Pay what you want"**, sugerido $5 USD, mínimo $0 (ver nota) |
| Categoría | Software Development / Productivity |
| Tags sugeridos | `ai`, `prompts`, `chatgpt`, `github-copilot`, `claude`, `software-development`, `sdlc`, `productivity` |
| Archivo a subir | `dist/ai-sdlc-pro-pack-completo.zip` (112 prompts × ES/EN + framework de contexto) |

> **Nota sobre el precio.** El precio fijo original ($499 MXN) se calibró
> cuando la suscripción costaba $299 MXN/mes. Con la suscripción en $1 USD/mes
> ese precio equivalía a ~27 meses de plataforma a cambio de una copia del
> catálogo que el tier Free ya regala para siempre (issue #7). Este canal se
> posiciona como **adquisición, no ingreso**: Gumroad aporta tráfico propio, y
> el `LEEME.md` del pack dirige a la suscripción. De ahí el "pay what you want"
> con mínimo $0 — cobrar por lo que se regala en el sitio sería incoherente.
> Ver MR-04 en `docs/requirements/BusinessRules.md`.

## Descripción corta (subtítulo / preview)

> La primera biblioteca estructurada de prompts en español para dirigir agentes IA a través del ciclo completo de ingeniería de software — 112 prompts, bilingüe, listos para copiar.

## Descripción completa

```
AI-SDLC Pro es la primera biblioteca interactiva de prompts estructurados
en español para dirigir agentes IA (GitHub Copilot, Claude, Cursor,
Windsurf, Codex, Antigravity) a través del ciclo completo de ingeniería de
software: desde el project charter hasta el postmortem de producción.

Este pack incluye:

✅ 112 prompts en español e inglés, cubriendo las 18 etapas del SDLC
   (requerimientos, diseño, implementación, pruebas, revisión, CI/CD,
   seguridad, operaciones, back office de ingeniería, y más)
✅ Framework de contexto multi-agente para anteponer a cualquier prompt
✅ Organizado en carpetas es/ · en/ · framework/, listo para usar

TRANSPARENCIA ANTE TODO: este mismo contenido está disponible gratis y sin
límite en https://prompts.lionsystems.com.mx — este pack no es contenido
exclusivo. Lo que compras es una copia offline organizada para trabajar sin
conexión, integrarla a tu propio flujo, o simplemente apoyar el desarrollo
del proyecto. Si solo necesitas copiar prompts uno por uno con variables
resueltas automáticamente, la app web gratuita sigue siendo la forma más
cómoda de usarlos.

Ideal para: dev seniors y tech leads que quieren estandarizar cómo su
equipo usa IA, freelancers que hacen ramp-up en stacks nuevos
constantemente, y cualquiera que quiera una copia de referencia sin
depender de una conexión a internet.

Licencia: uso individual de quien lo adquiere. No redistribuir ni revender.
```

## Nota sobre honestidad de la oferta

Esta descripción declara explícitamente que el contenido es el mismo que el
del sitio gratuito -- es intencional, no un descuido. El repositorio de
este proyecto es público (ver `docs/STRATEGY.md`, decisión 2026-07-30):
vender el pack como si fuera contenido exclusivo sería engañoso y fácil de
desmentir por cualquier comprador técnico. El valor real que se vende aquí
es la conveniencia (copia offline organizada) y el apoyo al proyecto, no
exclusividad de contenido -- mismo criterio ya aplicado al muro Free/Pro de
la plataforma (issue #7).

## Checklist de publicación manual

- [ ] Ejecutar `python3 build_gumroad_pack.py` para regenerar el .zip con el
      catálogo más reciente (confirma el conteo de prompts en la salida).
- [ ] Crear el producto en Gumroad con los datos de la tabla de arriba.
- [ ] Subir `dist/ai-sdlc-pro-pack-completo.zip` como archivo del producto.
- [ ] Usar una captura de la app (`https://prompts.lionsystems.com.mx`)
      como imagen de portada -- evitar assets genéricos de stock.
- [ ] Publicar y enlazar el producto desde el sitio (footer o `/precios`,
      sección "Canal alternativo") una vez que la URL de Gumroad exista.
- [ ] Cerrar issue #9 con el link del producto publicado.
