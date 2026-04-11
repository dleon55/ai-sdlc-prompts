# 4.4 — Architecture Decision Records (ADR)

## Descripción

Prompt para documentar decisiones arquitectónicas de forma estructurada: contexto del problema, opciones evaluadas, decisión tomada, consecuencias y estado. Genera ADRs numerados y versionados que quedan como registro permanente del por qué del diseño.

**Cuándo usarlo:** al tomar una decisión arquitectónica significativa (elección de tecnología, patrón de diseño, estrategia de integración, estructura de datos), al documentar decisiones pasadas que no quedaron registradas, o como revisión al inicio de un proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Documenta la decisión arquitectónica de este proyecto como un Architecture Decision Record (ADR) numerado y trazable.

Inputs requeridos:
- número del ADR: [ADR-NNN]
- título corto de la decisión: [TÍTULO]
- fecha: [FECHA]
- estado: [propuesto / aceptado / descartado / deprecado / supersede por ADR-NNN]
- autor(es): [NOMBRE O AGENTE]

Genera un ADR completo con las siguientes secciones:

## 1. Contexto
Describe la situación, el problema o la necesidad que requirió tomar una decisión.
Incluye:
- restricciones del sistema o del equipo
- fuerzas en juego (performance, costo, tiempo, seguridad, mantenibilidad)
- qué pasaría si NO se toma ninguna decisión

## 2. Decisión
La decisión tomada, expresada de forma directa y sin ambigüedades.
Una sola oración clara: "Hemos decidido usar X para Y."

## 3. Opciones evaluadas
Por cada opción considerada (incluyendo la descartada):
- nombre de la opción
- descripción breve
- pros concretos
- contras concretos
- por qué fue descartada (si aplica)

## 4. Consecuencias
### Positivas
- qué mejora con esta decisión

### Negativas o compromisos aceptados (trade-offs)
- qué se sacrifica o complica

### Neutras
- cambios de proceso o convención que se derivan

## 5. Cumplimiento y validación
- cómo se verifica que la decisión fue implementada correctamente
- qué métricas o evidencias confirman que fue la decisión correcta

## 6. Referencias
- documentos relacionados
- issues o PRs que motivaron la decisión
- ADRs relacionados

Formato del archivo de salida: docs/decisions/ADR-NNN-titulo-corto.md
```

---

## Uso con fórmula estándar

```text
Usa el prompt de Architecture Decision Records y adáptalo a:
- repositorio: [NOMBRE O URL]
- número ADR: [ADR-NNN]
- título: [TÍTULO DE LA DECISIÓN]
- contexto del proyecto: [STACK, RESTRICCIONES, EQUIPO]
- opciones evaluadas: [LISTA DE ALTERNATIVAS CONSIDERADAS]
- documentos a revisar: README, arquitectura existente, issues relacionados
- objetivo puntual de salida: ADR completo listo para guardar en docs/decisions/
- nivel de profundidad: alto
```

---

## Salida esperada

```markdown
# ADR-001: Uso de GitHub Pages + GCP dual-deploy para el portal de prompts

**Fecha:** 2026-04-10
**Estado:** Aceptado
**Autor:** David León / GitHub Copilot Agent

## Contexto
El portal AI-SDLC Pro necesita ser accesible públicamente para todo el equipo...

## Decisión
Hemos decidido usar GitHub Pages para la URL pública y GCP con Nginx para el
dominio corporativo `prompts.lionsystems.com.mx`.

## Opciones evaluadas
| Opción | Pros | Contras | Resultado |
|---|---|---|---|
| Solo GitHub Pages | Gratuito, CI/CD automático | Sin dominio personalizado sin DNS externo | Parcialmente elegida |
| Solo GCP Nginx | Dominio corporativo, control total | Despliegue manual, costo de VM | Parcialmente elegida |
| Vercel / Netlify | CI/CD + dominio fácil | Dependencia de tercero, restricciones de uso | Descartada |
| Dual GitHub Pages + GCP | Lo mejor de ambos | Mayor complejidad de sincronización | **Elegida** |

## Consecuencias positivas
- URL pública gratuita para equipo externo
- URL corporativa con TLS para uso interno
...
```

---

## Índice de ADRs recomendado (`docs/decisions/README.md`)

| ADR | Título | Estado | Fecha |
|---|---|---|---|
| ADR-001 | [Primer ADR] | propuesto | |
| ADR-002 | [Segundo ADR] | aceptado | |
