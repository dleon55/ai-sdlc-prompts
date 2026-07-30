# 4.7 — Diseño detallado de modelo de datos: entidades, relaciones y esquema

## Descripción

Prompt para diseñar el esquema de datos detallado de una feature o proyecto: entidades con sus campos y tipos, relaciones con cardinalidad y política de borrado, nivel de normalización, índices justificados por patrón de consulta, y estrategia de evolución. Produce el diseño del esquema, no el script de migración ejecutable.

**Cuándo usarlo:** durante la fase de diseño (después de `04-01`, en paralelo o después de `04-03`), cuando el cambio o proyecto requiere un modelo de datos nuevo o una extensión significativa del existente — antes de escribir la migración real. Distinto de `00-D-02-stack-arquitectura-inicial`, que solo esboza el modelo de datos a alto nivel (máximo 10 entidades, sin detalle de campos ni índices), y de `08-05-revision-migracion-esquema-bd`, que audita la **seguridad** de una migración ya escrita (bloqueos, compatibilidad, reversibilidad): este prompt diseña el esquema detallado en sí.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | alto — el esquema de datos es una de las decisiones más costosas de revertir una vez que hay datos reales en producción (migraciones destructivas, downtime, pérdida de integridad); el prompt no ejecuta ninguna migración ni modifica ninguna base de datos |
| Entradas requeridas | entidades y relaciones del dominio (o el diseño de solución `04-01` / casos de uso `04-03` de los que inferirlas), motor de base de datos (relacional/documental/otro), volumen y patrón de acceso esperado (lecturas vs. escrituras, consultas frecuentes), modelo de datos existente si se está extendiendo uno |
| Herramientas permitidas | lectura del esquema actual y documentación relacionada — sin ejecutar migraciones ni modificar la base de datos; produce el diseño, no el script de migración |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el motor de base de datos o el patrón de acceso esperado no se conoce, detener y solicitarlo antes de proponer un esquema — la normalización y la estrategia de índices dependen directamente de esa información |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada entidad declara sus campos con tipo y nullabilidad; cada relación declara cardinalidad y política de borrado; cada índice propuesto está justificado por un patrón de consulta citado, no por intuición |
| Siguiente prompt recomendado | `08-05-revision-migracion-esquema-bd` una vez el script de migración esté escrito a partir de este diseño |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña el esquema de datos detallado para el dominio o cambio descrito: entidades, campos, relaciones, normalización, índices e integridad, con la justificación de cada decisión.

Entradas:
- entidades y relaciones del dominio: [DESCRIPCIÓN, O REFERENCIA A 04-01/04-03]
- motor de base de datos: [RELACIONAL (Postgres/MySQL/...) / DOCUMENTAL (MongoDB/...) / OTRO]
- volumen y patrón de acceso esperado: [LECTURAS VS ESCRITURAS, CONSULTAS FRECUENTES, VOLUMEN APROXIMADO]
- modelo de datos existente (si se extiende uno): [PEGAR O "modelo nuevo, sin esquema previo"]

Actividades:
1. ENTIDADES
   Para cada entidad del dominio, define sus campos: nombre, tipo, nullabilidad, valor por defecto y restricciones (unique, check). No omitas campos de auditoría básicos (creación/actualización) salvo que el dominio justifique explícitamente su ausencia.

2. RELACIONES
   Para cada relación entre entidades, define cardinalidad (1:1, 1:N, N:M), llave foránea, y política de borrado (cascade/restrict/set null) — justifica la elección de la política de borrado citando el impacto de negocio, nunca la dejes en el valor por defecto del motor sin decisión consciente.

3. NORMALIZACIÓN
   Evalúa el nivel de normalización apropiado (hasta 3FN por defecto) y justifica cualquier desnormalización deliberada citando el patrón de acceso que la motiva (ej. columna calculada para evitar un JOIN costoso en una consulta de alta frecuencia).

4. ÍNDICES
   Propone índices basados en los patrones de consulta declarados (filtros, joins, ordenamientos frecuentes). Nunca propongas un índice sin poder citar la consulta específica que lo justifica.

5. INTEGRIDAD Y RESTRICCIONES
   Define constraints a nivel de base de datos (not null, unique, check, foreign key) que deben existir independientemente de cualquier validación en la capa de aplicación.

6. ESTRATEGIA DE EVOLUCIÓN
   Señala cómo se espera que este esquema crezca (campos que probablemente se agreguen, riesgo de romper compatibilidad), y define la estrategia de soft delete vs. hard delete y de auditoría (created_at/updated_at, versión, actor) si aplica al dominio.

Restricciones:
- no propongas un índice sin poder citar el patrón de consulta específico que lo justifica — un índice sin justificación es deuda técnica, no optimización,
- toda relación debe declarar explícitamente su política de borrado (cascade/restrict/set null) — nunca la dejes implícita o "por defecto del motor" sin una decisión consciente y justificada,
- si el motor de base de datos o el patrón de acceso esperado no se conoce, detente y solicítalo — no asumas un motor ni un patrón de lectura/escritura por defecto,
- este prompt entrega el diseño del esquema; no genera el script de migración ejecutable ni lo ejecuta contra ningún ambiente — eso corresponde a la implementación y a la revisión posterior con `08-05`.

Salida:
0. Bloque JSON de metadatos (claves: status, entity_count, relationship_count, index_count, confidence_score [0.0 a 1.0]).
1. Catálogo de entidades: Entidad | Campo | Tipo | Nullable | Default | Restricciones
2. Relaciones: Entidad origen | Entidad destino | Cardinalidad | Llave foránea | Política de borrado
3. Índices propuestos: Índice | Campos | Justificación (patrón de consulta)
4. Desnormalizaciones deliberadas (si las hay) y su justificación.
5. Estrategia de evolución, soft/hard delete y auditoría.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de modelo de datos y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- componentes: [SERVICIO(S) / MÓDULO(S) QUE USARÁN ESTE ESQUEMA]
- documentos a revisar: diseño de solución (04-01), casos de uso (04-03), esquema actual si se extiende uno
- objetivo puntual de salida: esquema detallado con entidades, relaciones, índices y política de borrado
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del esquema |
| Catálogo de entidades (1) | Todos los campos de cada entidad, con tipo y nullabilidad |
| Relaciones (2) | Cardinalidad y política de borrado de cada relación |
| Índices propuestos (3) | Cada índice con la consulta que lo justifica |
| Desnormalizaciones (4) | Excepciones a la normalización, con su justificación de patrón de acceso |
| Estrategia de evolución (5) | Crecimiento esperado, soft/hard delete y auditoría |

### Ejemplo (fragmento)

```json
{
  "status": "diseñado",
  "entity_count": 4,
  "relationship_count": 3,
  "index_count": 5,
  "confidence_score": 0.8
}
```

| Entidad | Campo | Tipo | Nullable | Default | Restricciones |
|---|---|---|---|---|---|
| `orders` | `status` | `varchar(20)` | no | `'pending'` | `check (status in ('pending','paid','shipped','cancelled'))` |
| `orders` | `customer_id` | `uuid` | no | — | `foreign key -> customers(id)` |

| Índice | Campos | Justificación |
|---|---|---|
| `idx_orders_customer_status` | `(customer_id, status)` | Consulta frecuente del panel de cliente: "listar pedidos activos de este cliente", ejecutada en cada carga del dashboard |
