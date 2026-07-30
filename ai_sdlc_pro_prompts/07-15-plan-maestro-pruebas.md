# 7.15 — Plan maestro de pruebas: estrategia de QA del proyecto

## Descripción

Prompt para definir la estrategia de pruebas de todo el proyecto o release: alcance y objetivos de calidad, niveles de prueba con su cobertura objetivo, ambientes y datos, roles y responsabilidades, criterios de entrada/salida del ciclo de pruebas, y manejo de defectos durante el ciclo. Amarra el enfoque global de QA antes de diseñar pruebas individuales por tipo.

**Cuándo usarlo:** al inicio de un proyecto (después de `07-00`, detección del stack de pruebas) o al planificar un release/hito mayor, antes de diseñar pruebas individuales por tipo (`07-01` a `07-06`). Distinto de `07-00` (que solo detecta el stack técnico de pruebas) y de los prompts `07-01` a `07-14` (que diseñan/implementan **un tipo** de prueba puntual): este prompt define el enfoque global — qué se prueba, con qué profundidad, en qué ambiente, y cuándo un release se considera listo desde QA.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — una estrategia de pruebas incompleta (sin criterios de salida claros, sin cobertura por nivel definida) no bloquea nada por sí misma, pero deja que features salgan a producción sin un criterio objetivo de "listo", propagando riesgo de calidad de forma silenciosa hasta que se materializa en producción |
| Entradas requeridas | perfil de stack de pruebas (`07-00`) si existe, alcance del proyecto o release, requerimientos no funcionales relevantes (`02-06`) si existen, restricciones de tiempo/recursos de QA, ambientes disponibles |
| Herramientas permitidas | lectura de documentación y configuración existente — sin ejecución de pruebas ni cambios; produce el documento de estrategia |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no puede definirse un criterio de salida objetivo y verificable para al menos los niveles críticos (unitaria, integración, E2E de los flujos core), no declares la estrategia como completa — repórtalo como vacío pendiente en vez de rellenarlo con un criterio subjetivo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada nivel de prueba (unitaria/integración/E2E/humo/performance/seguridad/accesibilidad) declara cobertura objetivo, responsable y punto en el pipeline; los criterios de entrada y salida del ciclo de pruebas están definidos explícitamente y son verificables |
| Siguiente prompt recomendado | `07-01-pruebas-unitarias` (y los prompts `07-02` a `07-06` correspondientes) para diseñar cada tipo de prueba conforme a esta estrategia |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Define la estrategia de pruebas de todo el proyecto o release: alcance, niveles de prueba con cobertura objetivo, ambientes, roles, criterios de entrada/salida y manejo de defectos durante el ciclo.

Entradas:
- perfil de stack de pruebas: [PEGAR O REFERENCIA A 07-00, O "no detectado aún"]
- alcance del proyecto o release: [DESCRIPCIÓN]
- requerimientos no funcionales relevantes: [PEGAR O REFERENCIA A 02-06, O "no definidos aún"]
- restricciones de tiempo/recursos de QA: [DESCRIPCIÓN O "ninguna declarada"]
- ambientes disponibles: [DEV / QA / STAGING / PROD, Y CUÁLES EXISTEN REALMENTE]

Actividades:
1. ALCANCE Y OBJETIVOS DE CALIDAD
   Define qué se va a probar (componentes o flujos críticos) y qué queda explícitamente fuera de alcance para este ciclo, con la razón — nunca dejes un área fuera de alcance sin justificación explícita.

2. NIVELES DE PRUEBA Y COBERTURA OBJETIVO
   Para cada nivel aplicable (unitaria, integración, E2E, humo, performance/carga, seguridad, accesibilidad), define el objetivo de cobertura (porcentaje o alcance cualitativo), si se prueba manual o automatizado, y por qué esa elección para ese nivel específico. Justifica la cobertura objetivo contra el riesgo del componente: un componente crítico de negocio no puede tener el mismo objetivo que uno cosmético sin decirlo explícitamente.

3. AMBIENTES Y DATOS
   Define qué ambiente corresponde a cada nivel de prueba y la estrategia de datos de prueba (referencia a `07-14-gestion-datos-prueba` si aplica).

4. ROLES Y RESPONSABILIDADES
   Define quién diseña, implementa y mantiene cada nivel de prueba (desarrollador, QA dedicado, agente IA) — ningún nivel puede quedar sin responsable asignado.

5. CRITERIOS DE ENTRADA Y SALIDA
   Define qué debe cumplirse antes de iniciar el ciclo de pruebas de un release (entrada) y qué debe cumplirse para considerarlo listo para producción (salida). Todo criterio debe ser verificable objetivamente (métrica, checklist, resultado de pipeline) — nunca un criterio subjetivo como "se ve bien" o "parece estable".

6. GESTIÓN DE DEFECTOS DURANTE EL CICLO
   Define qué severidad de defecto bloquea un release y cuál se puede posponer, y quién tiene autoridad para tomar esa decisión.

7. HERRAMIENTAS Y PIPELINE
   Define en qué punto del pipeline CI/CD corre cada nivel de prueba (local, PR, pre-merge, pre-deploy, post-deploy), referenciando el stack detectado en `07-00`.

Restricciones:
- no declares una cobertura objetivo sin justificarla contra el riesgo del componente — toda diferencia de exigencia entre componentes debe quedar explícita, no implícita,
- todo criterio de entrada o salida debe ser verificable objetivamente (métrica, checklist, resultado de pipeline) — nunca aceptes un criterio subjetivo sin forma de confirmarlo,
- si falta el perfil de stack de pruebas (`07-00`) o el alcance del proyecto/release, detente y solicítalo antes de proponer la estrategia,
- distingue explícitamente qué niveles de prueba ya existen (y con qué cobertura real, si es verificable) de los que se proponen desde cero — nunca los presentes como si ya estuvieran implementados.

Salida:
0. Bloque JSON de metadatos (claves: status, test_levels_covered, entry_criteria_count, exit_criteria_count, confidence_score [0.0 a 1.0]).
1. Alcance y objetivos de calidad, con exclusiones justificadas.
2. Niveles de prueba y cobertura objetivo: Nivel | Cobertura objetivo | Manual/Automatizado | Responsable | Ambiente | Punto en el pipeline
3. Criterios de entrada del ciclo de pruebas.
4. Criterios de salida (Definition of Done de QA).
5. Gestión de defectos durante el ciclo: severidad que bloquea vs. severidad que se puede posponer, y quién decide.
6. Vacíos y siguientes pasos pendientes de confirmar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de plan maestro de pruebas y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- alcance del proyecto o release: [DESCRIPCIÓN]
- perfil de stack de pruebas: [REFERENCIA A 07-00]
- documentos a revisar: perfil de stack (07-00), requerimientos no funcionales (02-06)
- objetivo puntual de salida: estrategia de QA completa con niveles, cobertura y criterios de entrada/salida
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de la estrategia |
| Alcance y objetivos (1) | Qué se prueba y qué queda fuera, con justificación |
| Niveles de prueba (2) | Tabla completa con cobertura objetivo, responsable y ubicación en el pipeline |
| Criterios de entrada (3) | Condiciones verificables para iniciar el ciclo de pruebas |
| Criterios de salida (4) | Definition of Done de QA, verificable objetivamente |
| Gestión de defectos (5) | Severidad que bloquea vs. pospone, y quién decide |
| Vacíos (6) | Información pendiente de confirmar antes de aprobar la estrategia |

### Ejemplo (fragmento)

```json
{
  "status": "estrategia_definida_con_vacios",
  "test_levels_covered": 6,
  "entry_criteria_count": 3,
  "exit_criteria_count": 4,
  "confidence_score": 0.73
}
```

| Nivel | Cobertura objetivo | Manual/Automatizado | Responsable | Ambiente | Punto en el pipeline |
|---|---|---|---|---|---|
| Unitaria | ≥80% en módulos de negocio críticos (pagos, autenticación); ≥50% en el resto | Automatizado | Desarrollador que implementa el cambio | Local + CI | Cada push, gate obligatorio para merge |
| E2E | Los 5 flujos core declarados en el Charter (registro, checkout, cancelación, reembolso, exportación) | Automatizado | QA dedicado | Staging | Pre-deploy a producción, gate obligatorio |

| Sección | Ejemplo de contenido |
|---|---|
| Criterios de salida (4) | 100% de pruebas unitarias e integración en verde · 0 defectos de severidad crítica o alta abiertos · pruebas de performance dentro de los umbrales de `02-06` · pruebas de humo pasadas en staging tras el último deploy |
