# 13.9 — Evaluación de impacto de privacidad de datos (DPIA)

## Descripción

Prompt para evaluar el impacto de privacidad de un procesamiento de datos personales o sensibles nuevo o significativamente modificado: inventario de datos, propósito y base legal, minimización, terceros y transferencias internacionales, mecanismo de derechos del titular, retención y riesgo residual. Complementa `13-04-threat-modeling` (amenazas de seguridad técnicas) y `14-03-iso-moprosoft-compliance` (conformidad de proceso) — ninguno de los dos evalúa base legal ni derechos del titular de los datos.

**Cuándo usarlo:** al diseñar una funcionalidad que procesa datos personales o sensibles nuevos, o antes de un cambio significativo en cómo se procesan datos ya existentes.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | alto — una DPIA incompleta puede dejar pasar a producción un procesamiento de datos sin base legal válida o sin mecanismo real para ejercer derechos del titular, con exposición regulatoria real (multas GDPR/CCPA/leyes locales de protección de datos); el prompt no ejecuta ni aprueba nada por sí mismo |
| Entradas requeridas | descripción de los datos personales/sensibles procesados, propósito del procesamiento, base legal propuesta, terceros involucrados (procesadores/subencargados), ubicación geográfica de los usuarios y del almacenamiento |
| Herramientas permitidas | lectura de documentación y diseño existente — sin ejecución |
| Autonomía permitida | A0 — Analizar; A1 — Proponer (base legal sugerida, controles de mitigación) |
| Criterios de detención | si no puede determinarse una base legal válida para el procesamiento, no asumas una — repórtalo como bloqueante que requiere decisión legal antes de continuar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada categoría de dato personal declara propósito, base legal, plazo de retención y mecanismo de ejercicio de derechos (acceso/rectificación/eliminación) |
| Siguiente prompt recomendado | `13-04-threat-modeling` para los controles de seguridad técnicos que protegen los datos identificados aquí; `13-08-gestion-secretos-credenciales` si el procesamiento involucra credenciales |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Evalúa el impacto de privacidad del procesamiento de datos personales o sensibles descrito: qué datos, para qué, bajo qué base legal, con qué terceros, con qué mecanismo de derechos del titular, y con qué riesgo residual.

Entradas:
- datos personales/sensibles procesados: [DESCRIPCIÓN]
- propósito del procesamiento: [PARA QUÉ SE USAN ESOS DATOS]
- base legal propuesta: [CONSENTIMIENTO / CONTRATO / INTERÉS LEGÍTIMO / OBLIGACIÓN LEGAL / NO DEFINIDA AÚN]
- terceros involucrados: [PROCESADORES/SUBENCARGADOS, O "ninguno"]
- ubicación geográfica: [PAÍSES DE LOS USUARIOS Y DEL ALMACENAMIENTO]

Actividades:
1. INVENTARIO DE DATOS
   Identifica qué datos personales o sensibles se procesan, por categoría (identificación, salud, financieros, biométricos, ubicación, comportamiento, etc.) y su nivel de sensibilidad.

2. PROPÓSITO Y BASE LEGAL
   Para cada categoría de dato, define para qué se procesa y bajo qué base legal específica (consentimiento, ejecución de contrato, interés legítimo, obligación legal) — nunca asumas una base legal sin justificarla contra el propósito declarado.

3. MINIMIZACIÓN
   Evalúa si se está recolectando solo lo necesario para el propósito declarado, o si hay sobre-recolección de datos que no se usan.

4. TERCEROS Y TRANSFERENCIAS
   Identifica qué procesadores o subencargados tienen acceso a los datos, y si hay transferencia internacional con las salvaguardas legales correspondientes (cláusulas contractuales tipo, decisión de adecuación, u otra).

5. DERECHOS DEL TITULAR
   Define el mecanismo real (no solo la intención declarada) por el cual un usuario puede acceder, corregir, eliminar o exportar sus datos.

6. RETENCIÓN
   Define el plazo de conservación de cada categoría de dato y el mecanismo de eliminación al vencer ese plazo.

7. RIESGO RESIDUAL
   Dado el diseño evaluado, identifica si queda algún riesgo de privacidad sin mitigar, y su severidad.

Restricciones:
- nunca asumas una base legal sin justificación explícita contra el propósito declarado — si no es clara, márcala como "[DECISIÓN LEGAL PENDIENTE]" en vez de elegir una por tu cuenta,
- no declares "cumplimiento" de un mecanismo de derechos del titular que solo existe como intención sin implementación real verificable,
- toda transferencia internacional de datos debe declarar la salvaguarda legal aplicable o marcarse explícitamente como riesgo abierto — nunca asumir que es segura sin esa salvaguarda citada,
- este prompt no sustituye asesoría legal formal — para decisiones de base legal en jurisdicciones específicas, señala explícitamente que requiere validación de un equipo legal antes de proceder.

Salida:
0. Bloque JSON de metadatos (claves: status, personal_data_categories, unmitigated_risks_count, confidence_score [0.0 a 1.0]).
1. Inventario de datos personales/sensibles por categoría.
2. Propósito y base legal por categoría.
3. Evaluación de minimización.
4. Terceros y transferencias internacionales, con salvaguardas.
5. Mecanismo real de derechos del titular.
6. Política de retención por categoría.
7. Riesgo residual identificado.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de evaluación de impacto de privacidad (DPIA) y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- funcionalidad que procesa datos: [DESCRIPCIÓN]
- datos personales/sensibles involucrados: [DESCRIPCIÓN]
- documentos a revisar: diseño de la funcionalidad, política de privacidad vigente, contratos con terceros procesadores
- objetivo puntual de salida: DPIA completa con base legal y riesgo residual
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de la evaluación |
| Inventario de datos (1) | Categorías de datos personales/sensibles identificadas |
| Propósito y base legal (2) | Base legal específica por categoría, justificada |
| Minimización (3) | Evaluación de sobre-recolección si existe |
| Terceros y transferencias (4) | Procesadores y salvaguardas de transferencia internacional |
| Derechos del titular (5) | Mecanismo real de acceso/rectificación/eliminación |
| Retención (6) | Plazo y mecanismo de eliminación por categoría |
| Riesgo residual (7) | Riesgos de privacidad no mitigados, con severidad |

### Ejemplo (fragmento)

```json
{
  "status": "evaluado_con_pendiente_legal",
  "personal_data_categories": 4,
  "unmitigated_risks_count": 1,
  "confidence_score": 0.7
}
```

| Categoría de dato | Propósito | Base legal | Retención | Derechos del titular |
|---|---|---|---|---|
| Ubicación GPS del dispositivo | Calcular tiempo estimado de entrega | Ejecución de contrato (servicio solicitado por el usuario) | 90 días, eliminación automática vía job programado | Endpoint `DELETE /me/location-history` ya implementado |
| Historial de búsquedas | Personalizar recomendaciones | [DECISIÓN LEGAL PENDIENTE] — el equipo propone "interés legítimo" pero no se ha validado con legal si aplica dado el volumen de datos de comportamiento recolectado | No definida aún | No implementado |

| Sección | Ejemplo de contenido |
|---|---|
| Riesgo residual (7) | Alto: el historial de búsquedas se procesa sin base legal validada y sin mecanismo de eliminación — bloqueante para lanzar esta funcionalidad hasta resolver ambos puntos con el equipo legal |
