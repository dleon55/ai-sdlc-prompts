# 16.3 — Artículo de base de conocimiento desde ticket resuelto

## Descripción

Prompt para transformar un ticket de soporte ya resuelto (síntoma, causa raíz, solución aplicada) en un artículo de base de conocimiento reutilizable: título buscable, síntomas, causa, pasos de solución y los casos en que esa solución NO aplica. No publica ni modifica el sistema de KB en producción: redacta contenido de texto para revisión y publicación humana posterior.

**Cuándo usarlo:** después de que un ticket se resuelve y el patrón (síntoma + causa + solución) es probable que se repita, evitando que el siguiente agente de soporte tenga que re-diagnosticar el mismo caso desde cero. Diferencia con prompts relacionados: `16-02-diagnostico-respuesta-incidente-soporte` diagnostica un incidente **en curso** y propone una respuesta al usuario; este prompt actúa **después**, sobre un ticket ya cerrado con causa raíz confirmada, y su salida no es una respuesta al usuario sino un artículo reutilizable para futuros tickets similares. Si el ticket de origen no tiene causa raíz confirmada (solo un síntoma que desapareció), este prompt debe detenerse en vez de fabricar una causa.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — el prompt solo redacta un borrador de texto para revisión humana; no publica ni modifica el sistema de KB en producción. El riesgo real (una solución incorrecta publicada y aplicada por otro agente de soporte) queda contenido por el paso de revisión humana obligatorio antes de publicar |
| Entradas requeridas | ticket resuelto con síntoma reportado, causa raíz confirmada (propia o proveniente del diagnóstico de `16-02`), pasos de solución aplicada y validada, sistema/producto/versión afectado, audiencia destino del artículo |
| Herramientas permitidas | lectura del ticket resuelto y de artículos de KB existentes relacionados (para evitar duplicados y mantener convenciones de estilo); no accede a sistemas en producción, no publica ni modifica el sistema de KB — la salida es un documento de texto en borrador |
| Autonomía permitida | A1 — Proponer (redactar el artículo de KB como borrador); nunca A2/A3 — publicar el artículo en el sistema de KB de producción requiere revisión y aprobación humana explícita fuera de este prompt |
| Criterios de detención | detener y escalar si el ticket no tiene causa raíz confirmada (solo síntoma resuelto sin diagnóstico) — no inventar una causa plausible; si la solución aplicada no fue validada como efectiva (ticket cerrado sin confirmación del usuario o de QA), marcar el artículo completo como borrador de baja confianza en vez de presentarlo como listo para publicar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | el artículo cita el ticket de origen (id/link), distingue explícitamente causa raíz confirmada de causa hipotética, e incluye siempre la sección "cuándo NO aplica esta solución" |
| Siguiente prompt recomendado | `16-02-diagnostico-respuesta-incidente-soporte` como fuente típica de este artículo cuando el ticket resuelto proviene de un diagnóstico previo; el artículo generado aquí requiere revisión y publicación humana en el sistema de KB antes de considerarse activo |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Technical Writer especializado en bases de conocimiento de soporte técnico. A partir de un ticket ya resuelto, redacta un artículo de base de conocimiento reutilizable con título buscable, síntomas, causa raíz, pasos de solución validados y los casos en que esa solución NO aplica.

Entradas:
- ticket resuelto (id o link): [ID O LINK DEL TICKET]
- síntoma reportado originalmente por el usuario: [DESCRIPCIÓN DEL SÍNTOMA, MENSAJES DE ERROR EXACTOS]
- causa raíz confirmada: [CAUSA RAÍZ CONFIRMADA — o "proviene del diagnóstico de 16-02" si aplica]
- pasos de solución aplicada y validada: [PASOS EXACTOS QUE RESOLVIERON EL TICKET, EN ORDEN]
- sistema/producto/versión afectado: [SISTEMA, VERSIÓN, ENTORNO]
- audiencia del artículo: [AGENTES DE SOPORTE NIVEL 1 / USUARIOS FINALES / AMBOS]
- sistema de KB destino y convenciones de estilo si existen: [NOMBRE DEL SISTEMA DE KB, GUÍA DE ESTILO — o "no disponible"]
- artículos de KB existentes relacionados (para evitar duplicados): [LINKS O "ninguno identificado"]

Pasos:

1. VALIDAR QUE HAY CAUSA RAÍZ CONFIRMADA
   Revisa el ticket antes de redactar nada. Si el ticket solo registra que el síntoma desapareció (ej. "el usuario reinició y funcionó") sin un diagnóstico de causa, indícalo explícitamente y detente: pide la causa raíz confirmada o el diagnóstico de `16-02` antes de continuar. No fabriques una causa plausible para rellenar el artículo.

2. VERIFICAR SI YA EXISTE UN ARTÍCULO SIMILAR
   Revisa los artículos de KB existentes relacionados provistos como entrada. Si el patrón ya está documentado, indícalo y propone actualizar el artículo existente en vez de crear uno duplicado.

3. TÍTULO BUSCABLE
   Redacta un título en el lenguaje que usaría la audiencia destino al buscar el problema (síntoma o mensaje de error tal como lo describiría un usuario), no en jerga interna del equipo de ingeniería.

4. SÍNTOMAS
   Lista los síntomas observables de forma concreta: mensajes de error exactos, comportamiento visible, condiciones bajo las que ocurre (versión, entorno, configuración). Evita descripciones vagas tipo "no funciona".

5. CAUSA RAÍZ
   Explica la causa raíz en el nivel de detalle apropiado para la audiencia destino. Distingue explícitamente si es una causa confirmada (validada en el ticket o en el diagnóstico de origen) o si queda algún elemento sin confirmar, y márcalo como tal.

6. PASOS DE SOLUCIÓN
   Redacta los pasos de solución de forma numerada y reproducible, en el orden en que se aplicaron y funcionaron. Incluye prerrequisitos o permisos necesarios si aplica.

7. CUÁNDO NO APLICA ESTA SOLUCIÓN
   Identifica síntomas similares que podrían tener una causa distinta (falsos positivos conocidos, condiciones que descartan este diagnóstico) y qué hacer en su lugar (ej. escalar, diagnosticar de nuevo con `16-02`). Esta sección es obligatoria: un artículo sin límites de aplicabilidad induce a aplicar la solución incorrecta.

8. METADATA Y CLASIFICACIÓN
   Propone producto, versión, categoría y tags para facilitar la búsqueda futura, y referencia el ticket de origen (id/link) como evidencia trazable.

9. NOTA DE REVISIÓN Y ESTADO DEL BORRADOR
   Cierra el artículo con una nota explícita de que es un borrador que requiere revisión humana antes de publicarse en el sistema de KB, e indica el nivel de confianza del artículo (alto si la causa y la solución están completamente validadas; bajo si algún elemento quedó sin confirmar).

Restricciones:
- nunca inventes causa raíz si el ticket no la registra explícitamente ni proviene de un diagnóstico previo (`16-02`); si falta, detente y señálalo como bloqueante en vez de rellenar con una hipótesis presentada como hecho.
- nunca publiques ni modifiques el sistema de KB en producción, ni ningún otro sistema; la única salida de este prompt es un documento de texto en borrador para revisión humana.
- generaliza el caso solo hasta donde la evidencia del ticket lo soporte; no extrapoles a escenarios, versiones o configuraciones no comprobadas sin marcarlas explícitamente como no verificadas.
- incluye siempre la sección "cuándo NO aplica esta solución" — nunca entregues un artículo sin definir sus límites de aplicabilidad.
- si la solución aplicada no fue validada como efectiva (ticket cerrado sin confirmación del usuario o de QA), marca el artículo completo como borrador de baja confianza en vez de presentarlo como listo para publicar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de artículo de base de conocimiento desde ticket resuelto y adáptalo a:
- repositorio/sistema de soporte: [NOMBRE O URL]
- ticket resuelto: [ID O LINK]
- síntoma reportado: [DESCRIPCIÓN]
- causa raíz confirmada: [CAUSA RAÍZ O "diagnóstico de 16-02"]
- pasos de solución aplicada: [PASOS]
- sistema/producto/versión: [SISTEMA, VERSIÓN]
- audiencia: [SOPORTE NIVEL 1 / USUARIOS FINALES / AMBOS]
- sistema de KB destino: [NOMBRE O "no disponible"]
- documentos a revisar: ticket de origen, artículos de KB relacionados existentes
- objetivo puntual de salida: artículo de KB en borrador listo para revisión humana
- nivel de profundidad: medio
```

---

## Salida esperada

```markdown
# Título: "Error 'No se pudo sincronizar el calendario' al conectar cuenta de Google Workspace"

**Producto/versión:** App móvil, v4.2+ · **Entorno:** iOS y Android · **Categoría:** Integraciones > Google Workspace
**Ticket de origen:** SUP-4821 (link) · **Confianza del artículo:** alta (causa y solución validadas por QA)

## Síntomas
- El usuario ve el mensaje "No se pudo sincronizar el calendario" al vincular una cuenta de Google Workspace (no ocurre con cuentas Gmail personales).
- El evento de calendario no aparece en la app aunque sí existe en Google Calendar.
- Ocurre solo en organizaciones donde el administrador de Workspace tiene restringido el scope `calendar.readonly` para apps de terceros.

## Causa raíz (confirmada)
La app solicita el scope `calendar.events` por defecto, pero la política de la organización en Google Workspace solo autoriza `calendar.readonly` a apps de terceros no verificadas por el admin. Google rechaza la solicitud de sincronización silenciosamente y la app muestra un error genérico en vez de indicar el scope faltante. Confirmado en el ticket SUP-4821 revisando los logs de la API de Google (error `insufficientPermissions`) junto con el administrador de Workspace del cliente.

## Pasos de solución
1. Confirmar con el usuario que la cuenta afectada es de Google Workspace (no Gmail personal) — ver Síntomas.
2. Pedir al usuario que solicite a su administrador de Workspace habilitar el scope `calendar.events` para la app en la consola de administración de Google (Seguridad > Control de acceso a apps).
3. Una vez habilitado el scope, pedir al usuario que desvincule y vuelva a vincular la cuenta desde Ajustes > Integraciones > Google Calendar.
4. Verificar que el evento de prueba sincroniza correctamente en menos de 2 minutos.

## Cuándo NO aplica esta solución
- Si la cuenta afectada es Gmail personal (no Workspace): este error no debería ocurrir por esta causa; escalar a diagnóstico general con `16-02`.
- Si el usuario ya tiene el scope `calendar.events` habilitado y el error persiste: la causa es distinta (posible expiración de token OAuth); no aplicar estos pasos, escalar como incidente nuevo.
- Si el error ocurre de forma intermitente (a veces sincroniza, a veces no): sugiere un problema de rate limiting de la API de Google, no de permisos; no aplica esta solución.

## Metadata
- **Tags:** google-workspace, calendario, oauth-scope, sincronización
- **Audiencia:** agentes de soporte nivel 1
- **Estado:** borrador — pendiente de revisión humana antes de publicar en el sistema de KB
```

### Resumen ejecutivo

- **Artículo generado:** título buscable, síntomas, causa raíz (confirmada o marcada como hipótesis), pasos de solución numerados y sección obligatoria de "cuándo no aplica".
- **Ticket de origen:** [ID/LINK] — trazabilidad conservada para auditoría futura.
- **Nivel de confianza del borrador:** [ALTO / BAJO] según si la causa y la solución quedaron completamente validadas en el ticket.
- **Estado:** borrador — requiere revisión y publicación humana explícita en el sistema de KB; este prompt no publica ni modifica el sistema de KB en producción.
