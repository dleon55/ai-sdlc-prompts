# LinkedIn — plantillas + posts listos (issue #10)

> Sprint 3, `docs/STRATEGY.md`. Meta: 500 impresiones/post, 3 posts/semana.
> Los 3 formatos abajo son los que pide el issue: **caso de uso real**,
> **antes/después de prompt** y **tip multi-agente**. Cada uno trae la
> plantilla reutilizable y 2 posts ya redactados y listos para publicar
> (ajustar solo si algún dato cambia, ej. número de prompts).
>
> Todos enlazan a `https://prompts.lionsystems.com.mx` y usan el tagline
> oficial ("Dirige cualquier agente IA como un Ingeniero Senior") o los
> mensajes clave por audiencia ya definidos en `docs/STRATEGY.md`.
> Capturas reales en `docs/marketing/assets/` listas para adjuntar.

---

## Formato 1 — Caso de uso real

**Plantilla:**
```
[Situación concreta de un dev/equipo] + [problema con prompting genérico]
↓
[Cómo un prompt estructurado de AI-SDLC Pro lo resolvió, con detalle técnico real]
↓
[Resultado medible o cualitativo]
↓
CTA: link a prompts.lionsystems.com.mx + 1 pregunta a la audiencia
```

### Post 1.1 (imagen: `assets/01-catalogo-general.png`)

```
Un dev jr de mi equipo iba a levantar un repo nuevo desde cero. Le pedí que
usara Copilot para "armar la estructura del proyecto" y lo que salió fue...
genérico. Carpetas sin criterio, sin CODEOWNERS, sin plantillas de PR.

El problema no era el modelo. Era el prompt.

Cambiamos a un prompt estructurado tipo SDLC — el mismo formato que uso en
cada fase del ciclo de ingeniería: contexto, riesgo esperado, criterios de
parada, salida esperada. Le dimos: tipo de proyecto, metodología, stack,
plataforma de CI, tamaño de equipo, tipo de licencia.

15 minutos después: estructura de repo completa, README real, CONTRIBUTING,
.gitignore correcto para el stack, protecciones de rama sugeridas. Nada que
inventar, nada que corregir después.

La diferencia no fue el agente. Fue dirigirlo como dirigirías a un ingeniero
senior nuevo en el equipo: con contexto completo, no con una frase suelta.

115 prompts así, gratis, en español: https://prompts.lionsystems.com.mx

¿Cuál es la tarea que más veces le repites "contexto" a tu agente de IA?

#GitHubCopilot #PromptEngineering #IA #DesarrolloDeSoftware
```

### Post 1.2 (imagen: `assets/02-modal-formula-uso.png`)

```
Cada vez que un dev de mi equipo pega un stack trace en Claude sin más
contexto, sé que vamos a perder 20 minutos en ping-pong: "¿en qué archivo?",
"¿qué versión?", "¿ya lo intentaste con X?".

Lo que cambió eso para nosotros no fue un mejor modelo. Fue dejar de escribir
prompts desde cero cada vez.

Tenemos un prompt fijo para diagnóstico de bugs que ya trae la estructura:
qué evidencia mínima incluir, qué autonomía tiene el agente (¿solo proponer
o puede tocar código?), y cuál es el criterio de "esto ya está resuelto".

El resultado no es que el agente sea más inteligente. Es que deja de
adivinar qué esperamos de él.

Si tu equipo usa IA a diario y cada quien prompteas distinto, prueba
estandarizar con prompts estructurados por fase del SDLC (requerimientos,
diseño, código, pruebas, revisión, operaciones...):
https://prompts.lionsystems.com.mx

¿Tu equipo tiene prompts compartidos o cada quien improvisa los suyos?

#TechLead #EngineeringManagement #IA #Copilot
```

---

## Formato 2 — Antes / después de prompt

**Plantilla:**
```
❌ ANTES (prompt genérico) — [ejemplo corto, real]
[por qué falla: ambiguo, sin contexto, sin criterio de éxito]

✅ DESPUÉS (prompt estructurado AI-SDLC Pro)
[fragmento real de un prompt del catálogo, con placeholders visibles]

[Qué cambia en el output del agente]

CTA + link
```

### Post 2.1

```
❌ ANTES:
"Ayúdame a documentar este issue para que un agente de IA lo resuelva."

Resultado: el agente hace preguntas, asume cosas, o peor — empieza a
programar sin confirmar el alcance real.

✅ DESPUÉS (prompt 0-C.1 del catálogo AI-SDLC Pro):
El prompt pide explícitamente:
- criterios de aceptación verificables
- alcance explícito de lo que NO se debe tocar
- nivel de autonomía permitido (¿solo proponer? ¿puede hacer commit?)
- criterio de parada si algo es ambiguo

Resultado: el agente entrega un plan claro antes de tocar una sola línea, o
declara la ambigüedad en vez de asumir. Nada de "creo que esto es lo que
querías".

La diferencia entre un prompt y un prompt DE INGENIERÍA es que el segundo
define qué pasa cuando algo no está claro.

115 prompts estructurados así, gratis: https://prompts.lionsystems.com.mx

#PromptEngineering #GitHubCopilot #ClaudeAI #SDLC
```

### Post 2.2

```
❌ ANTES:
"Revisa este PR y dime si está bien."

El agente dice "se ve bien" sin criterio real. Cero trazabilidad de qué
evaluó.

✅ DESPUÉS (prompt de revisión de código, catálogo AI-SDLC Pro):
Define explícitamente: qué riesgo se espera de este tipo de cambio (bajo/
medio/alto), qué evidencia mínima debe aportar el agente para decir
"aprobado" (no solo una opinión), y qué prompt usar después según el
resultado (documentación, siguiente fase, rollback).

El agente deja de dar una opinión y empieza a dar una evaluación con
criterio explícito — la misma diferencia entre "se ve bien" y un checklist
real de revisión.

Bilingüe (ES/EN), sin cuenta, copia y pega:
https://prompts.lionsystems.com.mx

¿Qué prompt le repites más seguido a tu agente sin darte cuenta?

#CodeReview #IA #DevTools
```

---

## Formato 3 — Tip multi-agente

**Plantilla:**
```
[Tip concreto y accionable sobre usar MÁS DE UN agente de IA en el mismo
flujo — Copilot + Claude, Cursor + Codex, etc.]

[Por qué importa / qué falla sin esto]

[Cómo aplicarlo con AI-SDLC Pro]

CTA + link
```

### Post 3.1

```
Tip multi-agente: si usas Copilot en el editor Y Claude/ChatGPT para
planear, y les das contexto distinto a cada uno, vas a tener dos versiones
distintas de "la verdad" sobre tu proyecto.

Nosotros resolvemos esto con un framework de contexto que se antepone a
CUALQUIER prompt, sin importar el agente: mismo stack, mismas convenciones,
mismo nivel de autonomía permitido. Un solo "cerebro compartido" para todos
los agentes que tocan el mismo repo.

No es un prompt más. Es la capa de contexto que hace que Copilot, Claude,
Cursor, Windsurf, Codex o Antigravity trabajen con la MISMA información base,
en vez de cada uno improvisando la suya.

Framework + 115 prompts, gratis: https://prompts.lionsystems.com.mx

¿Usas más de un agente de IA en tu flujo de trabajo? ¿Cómo mantienes el
contexto consistente entre ellos?

#MultiAgent #AIagents #GitHubCopilot #ClaudeAI #Cursor
```

### Post 3.2

```
Tip multi-agente: no todos los agentes deberían tener el mismo nivel de
autonomía en el mismo repo.

Un agente que solo propone cambios (revisión, análisis) no necesita el
mismo permiso que uno que puede hacer commit directo (implementación
acotada, bajo riesgo).

En el catálogo AI-SDLC Pro cada prompt declara su "autonomía permitida"
explícita: A0 (solo lectura/análisis) hasta A3 (ejecución con mínima
supervisión). Es la diferencia entre dejar que un agente "opine" sobre tu
arquitectura y dejar que la modifique sin que nadie la haya revisado.

Si coordinas varios agentes en el mismo proyecto, definir esto por
adelantado evita sorpresas — no después de que algo ya se rompió.

Ver el catálogo completo con niveles de riesgo y autonomía por prompt:
https://prompts.lionsystems.com.mx

#AIagents #SoftwareEngineering #DevOps
```

---

## Notas de uso

- Publicar en el orden 1 → 2 → 3 y repetir el ciclo (mantiene los 3 formatos
  balanceados en el feed, según pide el issue).
- Adjuntar siempre una imagen real de `docs/marketing/assets/` — nunca un
  gráfico genérico de stock; el producto es el mejor asset visual disponible.
- Medir impresiones/comentarios por post en un doc aparte (no versionado
  aquí) para ajustar qué formato rinde mejor antes de escalar frecuencia.
