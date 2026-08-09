# Estrategia de Producto y Monetización — AI-SDLC Pro

> Documento vivo. Última actualización: 2026-07-30.  
> Propietario: LionSystems — dleon55

---

## Visión del producto

**AI-SDLC Pro** es la primera biblioteca interactiva de prompts estructurados en español para dirigir agentes IA (GitHub Copilot, Claude, Cursor, Windsurf, Codex, Antigravity) a través del ciclo completo de ingeniería de software.

AI-SDLC Pro es un producto de **Lion Systems**: su función es demostrar la
capacidad de la organización, adquirir usuarios y validar capacidades de
plataforma. No sustituye los servicios B2B de arquitectura, desarrollo,
automatización, seguridad y soporte ofrecidos por la marca institucional.

**Propuesta de valor central:**  
Un dev o equipo que usa AI-SDLC Pro obtiene outputs consistentes, trazables y de calidad de ingeniería — sin importar qué agente IA usa ni qué tan experimentado es con prompting.

**Diferenciadores competitivos confirmados:**
- Único catálogo estructurado SDLC end-to-end en español
- Framework de contexto multi-agente (auto-prepend)
- Sistema de proyectos con 19 variables persistentes
- Infraestructura production-grade (GCP + TLS + CI/CD)
- Licencia propietaria — contenido curado por LionSystems

---

## Mercado objetivo

### Buyer Personas

| Persona | Descripción | Dolor principal | Disposición a pagar |
|---------|-------------|-----------------|---------------------|
| **Dev Sr / Tech Lead** | 5-10 años exp, usa Copilot/Claude diario | Contexto repetitivo, outputs inconsistentes entre el equipo | Alta |
| **CTO / Engineering Manager** | Equipos 3-15 devs | Brecha de madurez AI entre devs, inconsistencia de calidad | Muy alta |
| **Dev Jr / Bootcamp grad** | Aprendiendo con IA | No sabe estructurar prompts para tareas reales de ingeniería | Media |
| **Freelancer / Consultor** | Multi-cliente, multi-stack | Necesita ramp-up rápido en cada repositorio nuevo | Alta |
| **Agencia de desarrollo** | 10-50 personas | Estandarizar calidad entre proyectos y clientes | Muy alta |

### Competencia

| Competidor | Debilidad que AI-SDLC Pro resuelve |
|------------|-------------------------------------|
| PromptBase | Prompts individuales sin estructura SDLC, sin multi-agente, en inglés |
| FlowGPT / PromptHero | Sin framework, sin variables, sin proyectos, prompts sueltos |
| Recursos estáticos / marketplaces | Contenido aislado, no interactivo ni adaptable al proyecto real |
| GitHub Copilot instructions DIY | Requiere experiencia, sin guía SDLC, sin estructura |

---

## Modelo de monetización

> **Actualizado 2026-07-30** — el modelo original de esta sección (4 tiers
> con paywall sobre los prompts) se reemplazó al confirmar que el
> repositorio es **público**: el texto de los 112 prompts ya es legible por
> cualquiera en GitHub o vía el servidor MCP sin autenticación, así que
> gatear el CONTENIDO no protege nada real. La decisión (issue #7, "Opción
> B") fue monetizar la **plataforma**, no el texto — ver "Decisiones
> registradas" al final de este documento.

### Tiers del producto (vigente)

| Tier | Precio | Contenido | Target |
|------|--------|-----------|--------|
| **Free** | $0 | Los 112 prompts, copia ilimitada y para siempre, sin cuenta. 1 proyecto activo (variables, checklist de progreso, modo guiado). | Adquisición — todo el catálogo |
| **Pro (prueba 1 semana)** | $0, con GitHub | Todo Free + proyectos ilimitados + personalización por prompt + guardado de resultados de IA. Renovable semanalmente con feedback mientras dure el piloto. | Conversión a cuenta |
| **Pro (suscripción)** | $1 USD/mes (introductorio) | Todo Pro sin muro de prueba ni renovación por feedback. | Individual, sin límite de tiempo |
| **Pro Equipo / Enterprise** | Por definir con datos del piloto | Todo Pro + funciones de equipo (a definir: miembros, proyectos compartidos, SSO) | Equipos y agencias — pendiente de validar demanda antes de construir |

### Canal alternativo — Producto digital

Tras el issue #7, Gumroad dejó de ser una integración de cobro y una vía de
ingreso del producto. El 2026-08-09 se ratificó como **canal de adquisición**
(no de ingreso): el pack completo se publica en modalidad "pay what you want"
con mínimo $0, su descripción declara explícitamente que el contenido es el
mismo que el del sitio gratuito, y su `LEEME.md` dirige a la suscripción de la
plataforma ($1 USD/mes vía Paddle). Ver "Decisiones registradas".

- **Pack completo único:** activo como adquisición. Material de publicación en
  `docs/gumroad-listing.md`; el .zip se regenera con `build_gumroad_pack.py`.
  Nunca vender como exclusivo un contenido público.
- **Packs por industria:** pospuestos hasta validar demanda y una propuesta de
  valor diferenciada.

> El precio anterior ($499 MXN fijo) se fijó cuando la suscripción costaba $299
> MXN/mes: el pack equivalía a ~1.7 meses. Con la suscripción en $1 USD/mes ese
> mismo precio equivalía a ~27 meses de plataforma por una copia de lo que ya se
> regala. Ver la nota de MR-04 en `docs/requirements/BusinessRules.md`.

### Proyección de ingresos

| Escenario | Mes 3 | Mes 6 | Mes 12 |
|-----------|-------|-------|--------|
| Conservador | $3,000 MXN | $12,000 MXN | $35,000 MXN |
| Moderado | $8,000 MXN | $30,000 MXN | $90,000 MXN |
| Optimista | $15,000 MXN | $60,000 MXN | $200,000 MXN |

> Supuestos moderados mes 6: 60 usuarios Pro Individual + 5 licencias equipo.

---

## Roadmap

El roadmap se gestiona vía GitHub Milestones e Issues.  
Ver: [Milestones](https://github.com/dleon55/ai-sdlc-prompts/milestones) · [Issues del roadmap](https://github.com/dleon55/ai-sdlc-prompts/issues?q=label%3Amonetization+label%3Amarketing+label%3Aux)

### Corto plazo — 0 a 90 días

#### Sprint 1 — Presencia y captura (Sem 1-2)

| # | Acción | Labels |
|---|--------|--------|
| 1 | Cambiar "Herramienta gratuita" → "Prueba gratis · Plan Pro" en header | `ux`, `monetization` |
| 2 | Agregar meta tags SEO (description, og:title, og:image, keywords) | `seo` |
| 3 | Integrar Google Analytics 4 | `analytics` |
| 4 | Captura de email en onboarding (Mailchimp/ConvertKit free tier) | `monetization`, `ux` |
| 5 | Crear landing page de conversión (/ separada de /app) | `ux`, `monetization` |

#### Sprint 2 — Producto vendible (Sem 3-4)

| # | Acción | Labels |
|---|--------|--------|
| 6 | ~~Definir prompts Free vs Pro — gate de conversión en sidebar~~ **Completado 2026-07-30, rediseñado**: dado que el repo es público, el gate no se aplicó a los prompts (no protege nada) sino a la plataforma — 1 proyecto gratis vs. proyectos ilimitados + personalización + resultados de IA en Pro. Ver issue #7 y `docs/trial-gate-setup.md`. | `monetization`, `ux` |
| 7 | Crear página de precios /precios con 3 tiers | `monetization`, `ux` |
| 8 | ~~Evaluar canales alternativos de adquisición sólo después de validar cobro, atribución y oferta~~ **Decidido 2026-08-09**: Gumroad ratificado como canal de adquisición ("pay what you want", mínimo $0). Material en `docs/gumroad-listing.md`; pendiente solo la publicación manual en la cuenta del propietario. | `monetization` |

#### Sprint 3 — Distribución (Sem 5-8)

| # | Acción | Labels |
|---|--------|--------|
| 9 | Estrategia LinkedIn: 3 posts/semana — plantillas + casos de uso. **Contenido listo 2026-07-31**: 3 plantillas + 6 posts redactados en `docs/marketing/linkedin-posts.md`. Pendiente: publicación y medición manual. | `marketing` |
| 10 | Artículo Dev.to/Hashnode: "Framework para dirigir agentes IA en el SDLC". **Artículo listo 2026-07-31**: borrador completo en `docs/marketing/dev-to-article.md`, con capturas reales en `docs/marketing/assets/`. Pendiente: publicación manual. | `marketing`, `seo` |
| 11 | ProductHunt launch planeado — semana 8. **Copy listo 2026-07-31**: tagline, descripción y comentario de apertura en `docs/marketing/producthunt-launch.md`. Pendiente: GIF demo, hunter y fecha (requieren decisión/grabación humana). | `marketing` |

#### Sprint 4 — Primera factura (Sem 9-12)

| # | Acción | Labels |
|---|--------|--------|
| 12 | Outreach directo: 20 CTOs/Tech Leads en LinkedIn, propuesta licencia equipo. **Plantillas listas 2026-07-31**: `docs/marketing/outreach-ctos.md` — usa el precio Individual vigente ($1 USD/mes); el tier de equipo se posiciona como "en definición con el piloto" en vez del $799 MXN/mes original del issue (desactualizado, contradice `/precios`). Pendiente: armar la lista real de 20 prospectos (requiere LinkedIn) y enviar. | `marketing`, `monetization` |
| 13 | Programa early adopters: primeros 50 Pro a $99 MXN/mes de por vida. **Rediseñado 2026-07-31**: `docs/marketing/early-adopters-program.md` — reemplaza el precio original ($99 MXN, desactualizado) por congelar el precio vigente ($1 USD/mes) de por vida para los primeros 50. **Mecanismo decidido 2026-08-09**: el congelado es el default de Paddle Billing (los cambios de precio solo afectan suscripciones nuevas); implementados el tracking de cohorte (`subscriptions.created_at`) y el contador real (`founding_spots_left()` + banner en `/precios`). Pendiente: ejecutar la migración en Supabase y publicar el post de lanzamiento. | `monetization` |
| 14 | Recopilar 3 testimonios de devs para social proof en landing | `marketing`, `ux` |

---

### Mediano plazo — 3 a 12 meses

#### Mes 3-6 — Escalar producto

- Backend mínimo (Supabase free tier): auth, perfil, proyectos sincronizados entre dispositivos
- Packs temáticos por industria (FinTech, eCommerce, SaaS B2B)
- Integración con GitHub API: prompts pre-rellenos con contexto real del repositorio
- Newsletter semanal "Prompt of the Week" (retención de lista)
- Canal YouTube: tutorial completo issue → deploy con AI-SDLC Pro

#### Mes 6-12 — Escalar negocio

- Certificación "Certified AI-SDLC Engineer" (acceso via suscripción anual $2,999 MXN)
- Plan Enterprise: SSO, equipos múltiples, prompts privados, soporte
- Marketplace de prompts comunitario (comisión 20% o curado Pro)
- API de prompts para integración en pipelines CI/CD (modelo por llamada)
- Partnerships con bootcamps (Platzi, Kodemia) — acceso grupal

---

## Estrategia de distribución

### Canales prioritarios (90 días)

| Canal | Frecuencia | Formato | KPI objetivo |
|-------|-----------|---------|--------------|
| LinkedIn | 3x/sem | Casos de uso reales + antes/después | 500 impresiones/post |
| Twitter/X | Diario | Tips + threads de prompts | 100 RTs en primer mes |
| YouTube Shorts | 2x/sem | Demo 60 seg: copy prompt → código real | 1,000 subs en 60 días |
| Reddit | 1x/sem | Value-first en r/ChatGPT, r/github, r/programming | 500 upvotes totales/mes |
| Dev.to / Hashnode | 2x/mes | Artículos técnicos con SEO | 300 visitas/artículo |
| ProductHunt | 1 launch | Preparación semana 6-7, lanzamiento semana 8 | Top 5 del día |

### SEO — Keywords objetivo

- "prompts ingeniería software IA español"
- "prompts GitHub Copilot SDLC"
- "biblioteca prompts Claude desarrollo software"
- "AI-SDLC framework español"
- "prompts multi-agente desarrollo software"

---

## Métricas de éxito

| Métrica | Actual | Meta Mes 3 | Meta Mes 6 | Meta Mes 12 |
|---------|--------|-----------|-----------|------------|
| Usuarios únicos/mes | Desconocido (sin GA) | 500 | 2,000 | 8,000 |
| Lista de email | 0 | 200 | 800 | 3,000 |
| MRR (ingresos recurrentes) | $0 | $3,000 MXN | $30,000 MXN | $90,000 MXN |
| Conversión Free→Pro | — | 2% | 5% | 8% |
| Prompts copiados/mes | Desconocido | Baseline GA | 10,000 | 50,000 |

---

## Branding y posicionamiento

**Nombre de producto:** AI-SDLC Pro  
**Tagline:** "Dirige cualquier agente IA como un Ingeniero Senior"  
**Categoría:** Prompt Engineering para SDLC Profesional  
**Marca paraguas:** LionSystems  
**Web:** https://prompts.lionsystems.com.mx  
**Repositorio:** https://github.com/dleon55/ai-sdlc-prompts

### Mensajes clave por audiencia

| Audiencia | Mensaje |
|-----------|---------|
| Dev Sr | "Deja de escribir el mismo contexto en cada prompt. Usa un framework que ya funciona." |
| Tech Lead | "Estandariza cómo tu equipo usa IA. Mismos prompts = mismo nivel de calidad." |
| CTO | "Reduce el tiempo dev→PR en un equipo con niveles mixtos de experiencia en IA." |
| Freelancer | "Ramp-up en cualquier stack en minutos. Los prompts adaptan el contexto automáticamente." |

---

## Decisiones registradas

| Fecha | Decisión | Razón |
|-------|---------|-------|
| 2026-04-11 | Modelo Freemium + Licencia equipo como estrategia principal | Mayor potencial de MRR recurrente vs venta única |
| 2026-04-11 | Gumroad como canal de validación rápida antes de implementar paywall | Decisión histórica reemplazada: no es integración de cobro ni oferta activa del producto |
| 2026-04-11 | Mantener sitio self-contained (sin backend en corto plazo) | Minimizar complejidad operativa en fase de validación |
| 2026-04-11 | Priorizar distribución orgánica antes de paid advertising | CAC desconocido, construir audiencia antes de escalar |
| 2026-07-30 | Gate Free/Pro sobre la PLATAFORMA (proyectos múltiples, personalización, resultados de IA), no sobre el TEXTO de los prompts ("Opción B", issue #7) | El repositorio es público — el texto ya es legible por cualquiera en GitHub o vía el servidor MCP sin autenticación; gatear la copia solo agregaba fricción sin proteger contenido real. La plataforma (gestión de proyecto) sí es exclusiva del sitio y monetizable de forma honesta. |
| 2026-08-06 | Licencia **por alcance**: prompts CC BY 4.0, servidor MCP MIT, plataforma propietaria | La `LICENSE` anterior ("All Rights Reserved", prohibía reproducir y usar sin permiso escrito) contradecía esta misma tabla: el plan Free promete "copia ilimitada y para siempre, sin cuenta", y publicar el servidor MCP era imposible porque instalar es reproducir y ejecutar es usar. La licencia por alcance codifica la decisión del 2026-07-30 en términos legales: libre el texto, propietaria la plataforma. Se eligió CC BY (y no BY-NC) porque prohibir el uso comercial dejaría fuera al freelancer/consultor, la persona con mayor disposición a pagar. La atribución convierte cada reuso en un enlace de vuelta. |
| 2026-08-09 | Mecanismo del Programa Fundador: **grandfathering por defecto de Paddle** + opción "a" (los suscriptores 51+ pre-subida también conservan su precio) | En Paddle Billing un cambio de precio solo afecta suscripciones nuevas — las activas siguen cobrándose al monto original salvo migración explícita vía API, que no se hará para nadie. Al subir el precio se crea un price NUEVO (no se edita el actual) y se actualiza `PADDLE_PRICE_ID`; el price de $1 queda como marcador de cohorte. La garantía pública es solo para los primeros 50 (tracking: `subscriptions.created_at` + RPC `founding_spots_left()`); los 51+ pre-subida reciben más de lo prometido a costo cero — migrarlos activamente arriesgaría churn por un puñado de dólares. |
| 2026-08-09 | Gumroad ratificado como **canal de adquisición** (no de ingreso): pack completo "pay what you want" con mínimo $0, publicación manual por el propietario | Reemplaza el archivo del 2026-08-02, que exigía una decisión comercial nueva antes de publicar — esta es esa decisión. El pack no vende exclusividad (el catálogo es público): vende una copia offline organizada y expone la marca al tráfico propio de Gumroad; su `LEEME.md` dirige a la suscripción de la plataforma. Material revisado en `docs/gumroad-listing.md`; responsable: propietario del proyecto (única cuenta con acceso a Gumroad). |

---

> Para cambiar este documento: abrir un issue con label `strategy` y proponer el cambio antes de editar.  
> LionSystems © 2026
