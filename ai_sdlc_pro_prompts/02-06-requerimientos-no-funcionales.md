# 2.6 — Especificación de requerimientos no funcionales

## Descripción

Prompt para catalogar y documentar formalmente los **requerimientos no funcionales (RNF)** del sistema o del cambio: rendimiento, disponibilidad, escalabilidad, seguridad, usabilidad, mantenibilidad, portabilidad y compliance — cada uno numerado, con umbral medible y método de verificación. Complementa el catálogo de requerimientos funcionales que ya producen `02-05`/`04-03`, que no cubren esta categoría.

**Cuándo usarlo:** después de tener los requerimientos funcionales definidos (`02-05`) o la arquitectura tentativa (`00-D-02`), y antes del diseño de solución (`04-01`) — los RNF condicionan decisiones de diseño que son costosas de revertir si se descubren tarde.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — un RNF omitido o mal cuantificado (p. ej. "debe ser rápido" sin número) deja al diseño y al plan de pruebas sin un criterio verificable, propagando ambigüedad a `04-01`/`07-06`, aunque este prompt no ejecuta ni compromete nada por sí mismo |
| Entradas requeridas | contexto del sistema o cambio, requerimientos funcionales ya definidos (de `02-05`/`04-03`) si existen, restricciones de negocio conocidas (SLA contractual, compliance, presupuesto de infraestructura), arquitectura o stack tentativo si existe (`00-D-02`) |
| Herramientas permitidas | lectura de documentación y código existente — sin ejecución ni cambios |
| Autonomía permitida | A0 — Analizar (catalogar RNF ya declarados o inferibles del contexto); A1 — Proponer (umbrales sugeridos cuando el negocio no los ha fijado, siempre marcados explícitamente como propuesta a validar) |
| Criterios de detención | si un RNF no puede expresarse con un umbral medible (número, unidad, condición de prueba), no lo declares como definido — regístralo como "pendiente de cuantificar" en vez de inventar una cifra |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada RNF numerado (RNF-XXX) declara categoría, umbral medible o "pendiente de cuantificar", método de verificación, y si es una restricción de negocio, de dónde proviene esa restricción |
| Siguiente prompt recomendado | `04-01-diseno-solucion` (los RNF alimentan las restricciones de diseño); `07-06-pruebas-performance-carga` para los RNF de rendimiento/carga |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Cataloga y documenta formalmente los requerimientos no funcionales del sistema o del cambio, con umbral medible y método de verificación para cada uno.

Entradas:
- contexto del sistema o cambio: [DESCRIPCIÓN]
- requerimientos funcionales ya definidos: [PEGAR O "no definidos aún"]
- restricciones de negocio conocidas: [SLA contractual, compliance (GDPR/HIPAA/PCI/ISO), presupuesto de infraestructura, o "ninguna declarada"]
- arquitectura o stack tentativo: [PEGAR O "no definido aún"]
- categorías a priorizar: [ej. TODAS, o un subconjunto: rendimiento, disponibilidad, escalabilidad, seguridad, usabilidad, mantenibilidad, portabilidad, compliance]

Actividades:
1. Para cada categoría de RNF aplicable (rendimiento, disponibilidad/confiabilidad, escalabilidad, seguridad, usabilidad/accesibilidad, mantenibilidad, portabilidad, compliance/regulatorio, observabilidad), determina si el contexto la hace relevante — omite categorías no aplicables con una línea explicando por qué, no las ignores en silencio.
2. Para cada RNF relevante, define: identificador (RNF-XXX), categoría, descripción, umbral medible (número + unidad + condición), método de verificación (qué prueba o métrica lo confirma), prioridad (crítico/alto/medio/bajo), y origen (declarado por negocio / inferido de RF / inferido de compliance aplicable).
3. Si un RNF no tiene un umbral que el negocio haya fijado, propone uno basado en estándares de la industria para el tipo de sistema, márcalo explícitamente como "[UMBRAL PROPUESTO — validar con negocio]", y justifica el número propuesto.
4. Detecta conflictos entre RNF (ej. máxima seguridad vs. mínima fricción de UX, alta disponibilidad vs. presupuesto de infraestructura limitado) y decláralos explícitamente con las opciones de trade-off, sin resolver el conflicto por tu cuenta.
5. Relaciona cada RNF con los requerimientos funcionales que restringe o condiciona, si existen RF ya definidos.

Restricciones:
- nunca declares un RNF como "definido" si solo tiene una descripción cualitativa sin umbral medible — repórtalo como pendiente de cuantificar,
- distingue siempre un RNF declarado explícitamente por el negocio de uno que tú infieres o propones — nunca los presentes con el mismo nivel de certeza,
- no inventes umbrales de compliance regulatorio (p. ej. cifras de una norma específica) sin poder citar la norma exacta — si no la conoces con certeza, márcalo como "[VERIFICAR CONTRA LA NORMA APLICABLE]",
- no resuelvas conflictos entre RNF por tu cuenta (p. ej. eligiendo seguridad sobre UX) — repórtalos como decisión pendiente para el negocio o la arquitectura.

Salida:
0. Bloque JSON de metadatos (claves: status, nfr_count, categories_covered, unquantified_count, confidence_score [0.0 a 1.0]).
1. Catálogo de RNF: ID | Categoría | Descripción | Umbral medible | Método de verificación | Prioridad | Origen
2. RNF pendientes de cuantificar, con la razón de por qué no se pudo fijar un umbral.
3. Conflictos detectados entre RNF: RNF en conflicto | Naturaleza del trade-off | Opciones | Decisión requerida de
4. Relación RNF ↔ RF: qué requerimientos funcionales queda restringido por cada RNF crítico.
5. Categorías omitidas y por qué.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de requerimientos no funcionales y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- contexto del sistema o cambio: [DESCRIPCIÓN]
- requerimientos funcionales ya definidos: [PEGAR O REFERENCIA]
- documentos a revisar: Project Charter, arquitectura (00-D-02), compliance aplicable
- objetivo puntual de salida: catálogo de RNF con umbrales medibles y método de verificación
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el conteo de RNF y su estado |
| Catálogo de RNF (1) | Tabla completa, un RNF por fila, con umbral medible y método de verificación |
| RNF pendientes (2) | Lista de RNF sin umbral definido, con la razón |
| Conflictos (3) | Trade-offs detectados entre RNF, sin resolver por cuenta propia |
| Relación RNF ↔ RF (4) | Qué funcionalidad queda condicionada por cada RNF crítico |
| Categorías omitidas (5) | Justificación de qué categorías no aplican a este sistema |

### Ejemplo (fragmento)

```json
{
  "status": "catalogado_con_pendientes",
  "nfr_count": 9,
  "categories_covered": ["rendimiento", "disponibilidad", "seguridad", "escalabilidad"],
  "unquantified_count": 2,
  "confidence_score": 0.72
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Catálogo de RNF (1) | RNF-003 \| Rendimiento \| Tiempo de respuesta del endpoint de búsqueda \| ≤300ms en el percentil 95, bajo 200 req/s \| Prueba de carga con `07-06-pruebas-performance-carga` \| Alto \| Declarado por negocio (SLA con cliente Premium) |
| Conflictos (3) | RNF-005 (disponibilidad 99.95%) vs. RNF-011 (presupuesto de infraestructura ≤$500 USD/mes) \| Alta disponibilidad usualmente requiere redundancia multi-zona, que excede el presupuesto declarado \| Opciones: (a) bajar el SLA objetivo, (b) aumentar presupuesto, (c) aceptar el riesgo de una sola zona con plan de DR manual \| Decisión requerida del patrocinador del proyecto |
