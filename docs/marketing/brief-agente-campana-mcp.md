# Brief para el agente que ejecuta la campaña del servidor MCP

> Escrito el 31-oct-2026 para el agente (o la persona) que ejecutará el lanzamiento de
> `ai-sdlc-prompts-mcp`. Léelo completo antes de tocar nada. Los textos de cada publicación están en
> [`lanzamiento-mcp.md`](lanzamiento-mcp.md). Copia de ambos en Drive: 01 - LIONSYSTEMS → AI-SDLC Pro - Expediente
> del Proyecto → 07_Marketing_y_CRM → 2026-11_Lanzamiento_MCP; este documento dice **qué hacer con ellos, cuándo, con
> qué reglas y cómo medir**.

## 1. Objetivo y cómo se mide

**Objetivo:** que desarrolladores que usan agentes de IA (Claude Code, Claude Desktop, Cursor)
instalen el servidor MCP y visiten la biblioteca, y que una parte pase al plan Pro.

**Metas de las 2 primeras semanas (3 al 16 de noviembre de 2026).** Son metas de referencia, no
promesas; sirven para decidir si seguir invirtiendo tiempo en el canal.

| Indicador | Meta | Dónde se lee |
|---|---|---|
| Descargas en npm | 150 | `https://api.npmjs.org/downloads/point/last-week/ai-sdlc-prompts-mcp` |
| Visitas al sitio desde la campaña | 500 | Google Analytics 4 (`G-C5JKYNZ62F`), campaña `mcp-launch`, por `utm_source` |
| Clics por canal | — | Odoo: enlaces rastreables de la campaña «AI-SDLC Pro · Lanzamiento servidor MCP · nov-2026» |
| Estrellas nuevas en GitHub | 25 | `gh api repos/dleon55/ai-sdlc-prompts --jq .stargazers_count` |
| Altas Pro | 2 | Tablero «Ventas Lion Systems» (fila AI-SDLC Pro) o panel de Paddle |
| Alta en directorios MCP | 5 de 5 | Lista de §6 |

**Línea base al 31-oct-2026:** 0 suscripciones Pro, paquete recién publicado. Anota las cifras de
arranque el primer día, antes de publicar nada.

## 2. Reglas que no se rompen

1. **Nada sale sin el «sí» explícito de David.** Las publicaciones van desde sus cuentas personales y
   hablan en su nombre. Antes de cada publicación, enséñale el texto final y el canal, y espera su
   aprobación en el chat. Una aprobación vale para esa publicación, no para las siguientes.
2. **Tú no inicias sesión ni manejas contraseñas.** Si una plataforma pide iniciar sesión, la abre
   David. Si te dejan una sesión iniciada, úsala solo para la publicación aprobada.
3. **Solo datos verificados.** Usa únicamente la tabla «Datos verificados» de `lanzamiento-mcp.md`.
   Antes de publicar, comprueba dos cosas:
   - el precio en `https://prompts.lionsystems.com.mx/precios.html`;
   - que `npx -y ai-sdlc-prompts-mcp` responda. Si cambió algo, corrige el texto y vuelve a pedir aprobación.
4. **Prohibido:** inventar cifras (usuarios, descargas, estrellas, empresas que lo usan); decir
   «oficial», «el mejor», «certificado» o «avalado por Anthropic»; mencionar clientes; prometer
   resultados.
5. **Una comunidad por día** y respetando sus reglas de autopromoción. Si una regla prohíbe el
   enlace o exige otro formato, no se publica ahí; anótalo y sigue.
6. **No compres** anuncios, seguidores, votos ni reseñas. No pidas votos en Hacker News ni en Reddit,
   ni coordines votos con conocidos (las dos plataformas lo castigan).
7. **No respondas en nombre de David** sin que apruebe la respuesta, salvo las respuestas modelo de
   §7, que ya están aprobadas como base. Adáptalas sin cambiar su sentido.

## 3. Lo que necesitas antes de empezar

| Qué | Quién lo da | Estado al 31-oct |
|---|---|---|
| Paquete en npm, funcionando | — | Listo (1.0.0) |
| Sección MCP en la portada (`/` y `/en/`) | — | Lista |
| Cuenta de Dev.to | David | Por confirmar |
| Perfil de LinkedIn | David | Existe |
| Cuenta de X y/o Bluesky | David | Por confirmar |
| Cuenta de Reddit con historial | David | Por confirmar. Una cuenta nueva sin karma suele quedar filtrada |
| Cuenta de Hacker News | David | Por confirmar |
| Acceso de lectura a Google Analytics 4 | David | Por confirmar |
| Imagen de portada para Dev.to (1000×420) y LinkedIn (1200×627) | Tú la preparas y David la aprueba | Pendiente |

Pregunta a David por las cuentas que falten **el primer día**, todas juntas. Un canal sin cuenta se
salta; no se crea una cuenta nueva solo para la campaña.

**Imagen sugerida:** fondo oscuro con el bloque de configuración `mcpServers` y la frase «112 SDLC
prompts, each with its operating contract». Sin logotipos de Anthropic, Cursor ni de otras marcas.

## 4. Calendario

Hora de referencia: Ciudad de México (UTC-6). Si un día se cae, se recorre todo un día; no se
publican dos canales grandes el mismo día.

| Fecha | Canal | Texto (en `lanzamiento-mcp.md`) | Hora sugerida |
|---|---|---|---|
| Lun 2-nov | Preparación: línea base, cuentas, imágenes, aprobación de textos | — | — |
| Mar 3-nov | Dev.to (inglés) | §1 | 8:00 |
| Mar 3-nov | LinkedIn en español | §2 | 9:00 |
| Mié 4-nov | LinkedIn en inglés | §3 | 9:00 |
| Mié 4-nov | X y/o Bluesky | §4 | 10:00 |
| Jue 5-nov | Reddit r/ClaudeAI | §5 | 9:00 |
| Vie 6-nov | Directorios MCP (los 5) | §7 de `lanzamiento-mcp.md` y §6 de este brief | Cualquier hora |
| Lun 9-nov | Reddit r/mcp | §5 | 9:00 |
| Mar 10-nov | Show HN | §6 | 7:30 (9:30 en Nueva York) |
| Jue 12-nov | Reddit r/cursor | §5, adaptando la primera línea a Cursor | 9:00 |
| Vie 13-nov | Informe de la semana 1 a David | §8 | — |
| 16-nov | Informe final y recomendación | §8 | — |

**Seguimiento diario** (unos 20 minutos): responde comentarios con §7, anota cifras en la tabla de
§8 y avisa a David de cualquier pregunta que no cubra §7.

## 5. Cómo publicar en cada canal

**Dev.to**
- Nueva publicación → pega el bloque de §1 sin las comillas de código exteriores.
- Título exacto de §1 y etiquetas `mcp`, `ai`, `claude`, `productivity`.
- Imagen de portada.
- En *Canonical URL* no pongas nada: el artículo original es este.
- Revisa la vista previa y comprueba que los bloques de código se vean como código.

**LinkedIn**
- Publicación normal, no artículo.
- El enlace va al final del texto: LinkedIn muestra menos las publicaciones con enlace, pero aquí
  importa medir el origen.
- Agrega la imagen. No etiquetes a personas ni a empresas sin permiso de David.

**X / Bluesky**
- Una sola publicación con el texto de §4.
- Si alguien pregunta, responde en el mismo hilo.

**Reddit**
- Lee las reglas del subreddit antes de publicar.
- Usa *flair* de proyecto o *showcase* si existe. Publica como texto, no como enlace.
- Quédate 2 horas pendiente de los comentarios.
- Si un moderador lo retira, no lo vuelvas a publicar. Anótalo.

**Show HN**
- *Submit*: título exacto de §6 y URL del repositorio.
- Justo después, publica como comentario el texto de §6.
- No compartas el enlace pidiendo votos.
- Responde con calma y con datos; las críticas técnicas se agradecen y se contestan.

**Después de cada publicación**
- Guarda la URL de la publicación en la tabla de §8.

## 6. Directorios MCP

Dar de alta el paquete en los cinco de la tabla de `lanzamiento-mcp.md` §7. Para cada uno:

1. Lee sus requisitos del día: los procesos cambian seguido.
2. Usa siempre los mismos datos:
   - **Nombre:** AI-SDLC Prompts
   - **Paquete:** `ai-sdlc-prompts-mcp`
   - **Repositorio:** `https://github.com/dleon55/ai-sdlc-prompts`
   - **Sitio:** `https://prompts.lionsystems.com.mx`
   - **Licencia:** MIT (código) y CC BY 4.0 (prompts)
   - **Descripción corta (inglés):** *112 software-lifecycle prompts for coding agents, each with an
     operating contract: autonomy ceiling, allowed tools, stop-and-ask rules and minimum evidence.
     Read-only, stdio, no network.*
3. Si piden verificar la propiedad del paquete o del repositorio con una cuenta de David, prepara
   todo y pídele que haga ese paso.
4. **MCP Registry oficial:** necesita un archivo `server.json` en el repositorio. Eso es un cambio de
   código: hazlo en una rama, con PR y con las pruebas en verde, y que lo integre quien mantiene el
   repositorio.

## 7. Respuestas modelo para comentarios

Adapta el tono; no cambies los datos.

| Pregunta | Respuesta (inglés) |
|---|---|
| ¿Es gratis? | Yes. The 112 prompts and the MCP server are free (MIT code, CC BY 4.0 prompts). There's an optional Pro plan for saved projects and per-prompt customization on the website. |
| ¿Qué datos envía? ¿Abre red? | None. It runs locally over stdio, opens no network connections and is read-only: every prompt ships inside the package. |
| ¿Por qué no un repositorio de prompts sin más? | You can use them that way too, they're all on GitHub. The MCP server adds search, variable resolution and the operating contract, so the agent gets the limits along with the instructions. |
| ¿El agente respeta de verdad el contrato? | Not always. It's an instruction, not an enforcement mechanism. It makes overreach visible: the prompt tells the agent to say so when a task contradicts its limits. We'd like to hear what you see in practice. |
| ¿Funciona con X cliente? | Any MCP client that supports stdio servers. Tested with Claude Code, Claude Desktop and Cursor. *(Si preguntan por otro, no afirmes que funciona: pide que lo prueben y lo cuenten.)* |
| ¿Por qué en español? | The library started in Spanish for Latin American teams, and every prompt is also available in English. |
| Una crítica o un error | Thank the person, ask for details if needed and open an issue in the repository with a link to the comment. Don't argue. |

Cualquier pregunta sobre precio futuro, empresa, clientes, roadmap o temas legales se le pasa a
David sin responder.

## 8. Registro e informe

Lleva este registro, por ejemplo en una hoja o al final de este archivo, en un PR aparte:

| Fecha | Canal | URL de la publicación | Reacciones / comentarios | Visitas `utm_source` (GA4) | Notas |
|---|---|---|---|---|---|

**Cifras diarias:** descargas de npm de la última semana, estrellas de GitHub, clics de cada enlace
rastreable en Odoo y visitas por `utm_source` con `utm_campaign=mcp-launch` en Google Analytics.

**Informe a David** (13 y 16 de noviembre), en una pantalla:

1. Las cifras frente a las metas de §1.
2. Los dos canales que mejor funcionaron y el peor, con datos.
3. Lo que más preguntó la gente.
4. Una recomendación: repetir, ajustar el mensaje o abandonar cada canal.
