# 7.13 — Diagnóstico y estabilización de tests inestables (flaky)

## Descripción

Prompt para diagnosticar un test automatizado que falla de forma intermitente (no determinista): reproduce el patrón de falla con múltiples corridas, evalúa las causas más comunes (condición de carrera, dependencia de orden, tiempo no determinista, estado compartido, dependencia de red), identifica la causa más probable con evidencia, y recomienda estabilizar con un fix real, poner en cuarentena temporal con seguimiento, o eliminar el test.

**Cuándo usarlo:** cuando un test ya existente falla intermitentemente en CI o localmente sin cambios de código aparentes, antes de decidir si se ignora, se reintenta automáticamente o se corrige de raíz.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diagnóstico |
| Riesgo esperado | medio — un test flaky mal diagnosticado y puesto en cuarentena permanente puede ocultar una regresión real futura; una "corrección" que solo enmascara el síntoma sin resolver la causa raíz (ej. sleeps o reintentos ciegos) da falsa confianza |
| Entradas requeridas | nombre/ruta del test, historial de ejecuciones recientes en CI (pasa/falla, timestamps), logs o stack traces de al menos 2-3 fallas, código del test y del código bajo prueba relacionado, indicación de si falla también en local o solo en CI |
| Herramientas permitidas | lectura de código, logs e historial de CI; ejecución repetida del test en un ambiente aislado (local o CI) para reproducir el patrón de falla — sin modificar el test hasta identificar la causa raíz |
| Autonomía permitida | A0 — Analizar (diagnóstico de causa); A1 — Proponer (fix, cuarentena o eliminación); A2 — Ejecutar controlado solo para correr el test repetidamente en un ambiente aislado con el propósito de reproducir el patrón, nunca para aplicar el fix sin revisión humana |
| Criterios de detención | si no se puede reproducir la falla tras el número de corridas definido en el protocolo, declarar "no reproducido" en vez de adivinar la causa; nunca recomendar cuarentena permanente sin un ticket de seguimiento con fecha de revisión |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada causa candidata respaldada por al menos una corrida reproducida o un patrón identificable en el historial de CI (ej. "falla más en el runner Linux que en macOS", "falla solo cuando corre después del test X") |
| Siguiente prompt recomendado | `07-01`/`07-02`/`07-03` (según el tipo de test) si se requiere rediseñar el test desde cero; `11-03-deuda-tecnica` si el patrón de flakiness se repite en múltiples tests y amerita una iniciativa más amplia |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diagnostica la causa raíz de un test automatizado inestable (flaky) y recomienda una acción: estabilizar con un fix concreto, poner en cuarentena temporal con seguimiento, o eliminar el test si ya no aporta valor de detección real.

Entradas:
- test a diagnosticar: [NOMBRE/RUTA DEL TEST]
- historial de ejecuciones recientes: [PEGAR O ENLACE AL HISTORIAL DE CI — pasa/falla por corrida, con timestamps]
- logs/stack traces de fallas: [PEGAR AL MENOS 2-3 CAPTURAS DE FALLA]
- código del test: [PEGAR O RUTA]
- código bajo prueba relacionado: [PEGAR O RUTA]
- contexto de entorno: [SOLO FALLA EN CI / FALLA TAMBIÉN EN LOCAL / DESCONOCIDO]

Pasos:
1. CLASIFICACIÓN DEL PATRÓN DE FALLA
   A partir del historial de CI, caracteriza el patrón: ¿falla en un porcentaje estable de corridas (ej. 1 de cada 10)? ¿Solo en cierto runner/SO? ¿Solo cuando corre en paralelo con otros tests o en cierto orden? ¿Empeora bajo carga (CI ocupado)? Si el historial no tiene suficientes datos para caracterizar el patrón, decláralo y solicita más corridas antes de continuar.

2. REPRODUCCIÓN CONTROLADA
   Diseña un protocolo de reproducción: cuántas corridas repetidas son necesarias para tener confianza estadística razonable dado el porcentaje de falla observado (ej. si falla 1 de cada 10, correrlo 20-30 veces para confirmar), en qué ambiente (local/CI aislado), y si debe correr solo o junto a la suite completa (para detectar dependencia de orden o estado compartido).

3. CHECKLIST DE CAUSAS COMUNES
   Evalúa cada categoría con evidencia del código y los logs, sin descartar ninguna sin revisarla:
   a) Tiempo/asincronía: waits fijos insuficientes, condiciones de carrera entre operaciones async, timeouts ajustados.
   b) Orden/aislamiento: el test depende de estado dejado por otro test (variables globales, base de datos no limpiada, singleton no reseteado).
   c) Red/dependencias externas: llamadas a servicios externos o de terceros no mockeados, DNS o latencia variable.
   d) Datos no deterministas: uso de fechas/horas reales, IDs generados aleatoriamente sin semilla fija, orden de iteración de estructuras no garantizado.
   e) Recursos compartidos: puertos, archivos temporales o locks compartidos entre tests que corren en paralelo.
   f) Entorno del runner: diferencias de recursos (CPU/memoria) entre runners de CI que exponen condiciones de carrera invisibles en local.

4. IDENTIFICACIÓN DE CAUSA MÁS PROBABLE
   Con base en el patrón de falla (paso 1) y la checklist (paso 3), identifica la causa más probable con su evidencia de respaldo. Si más de una categoría es plausible, decláralo y prioriza por la que tenga más evidencia directa, no por cuál sea más fácil de corregir.

5. RECOMENDACIÓN DE ACCIÓN
   - Si la causa raíz es clara y corregible: propone el fix concreto (evita "agregar un sleep" o "aumentar el timeout" como solución final salvo que sea la corrección real de una condición de carrera documentada, no un parche cosmético).
   - Si la causa no puede confirmarse con la evidencia disponible pero el test bloquea CI: recomienda cuarentena temporal (marcar como skip/quarantine) con un ticket de seguimiento y fecha de revisión — nunca cuarentena sin fecha ni ticket.
   - Si el test ya no aporta valor de detección real (prueba una ruta obsoleta, duplica cobertura de otro test estable): recomienda eliminarlo, justificando por qué no representa pérdida de cobertura.

Restricciones:
- no apliques ni recomiendes un fix que solo enmascare el síntoma (aumentar timeouts arbitrariamente, agregar reintentos sin límite, agregar sleeps sin relacionarlos con una condición de carrera identificada) como solución final — si no hay causa raíz confirmada, decláralo y recomienda cuarentena en vez de un parche cosmético,
- nunca recomiendes cuarentena permanente sin ticket de seguimiento y fecha de revisión explícita — un test en cuarentena sin plan de retorno dejará de detectar regresiones reales de forma silenciosa,
- no propongas cambios al código de producción para "solucionar" el flaky si la causa está en el test mismo (aislamiento, orden) y no en el comportamiento real del sistema,
- toda causa candidata debe estar respaldada por al menos una corrida reproducida o un patrón identificable en el historial — no por intuición de qué "suele" causar flakiness,
- si no puedes reproducir la falla tras el número de corridas definido en el protocolo, decláralo como "no reproducido" y no inventes una causa para cerrar el diagnóstico.

Salida:
0. Bloque JSON de metadatos (claves: status, failure_pattern, root_cause_category, confidence_score [0.0 a 1.0]).
1. Patrón de falla caracterizado (frecuencia, condiciones asociadas).
2. Protocolo de reproducción aplicado y resultado.
3. Evaluación de la checklist de causas comunes, por categoría, con evidencia.
4. Causa raíz más probable, con evidencia de respaldo.
5. Recomendación de acción (fix / cuarentena con ticket y fecha / eliminación), con justificación.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diagnóstico de tests flaky y adáptalo a:
- repositorio: [NOMBRE O URL]
- test a diagnosticar: [NOMBRE/RUTA DEL TEST]
- historial de ejecuciones: [ENLACE AL HISTORIAL DE CI]
- logs de fallas: [PEGAR AL MENOS 2-3 CAPTURAS]
- ambiente: [SOLO FALLA EN CI / TAMBIÉN EN LOCAL]
- documentos a revisar: código del test, código bajo prueba, historial de CI
- objetivo puntual de salida: causa raíz confirmada y recomendación de acción
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con metadatos del diagnóstico |
| Patrón de falla (1) | Frecuencia observada y condiciones asociadas a la falla |
| Protocolo de reproducción (2) | Corridas ejecutadas, ambiente usado, resultado obtenido |
| Checklist de causas (3) | Evaluación de cada categoría común con evidencia citada |
| Causa raíz (4) | Causa más probable con su evidencia de respaldo |
| Recomendación (5) | Fix concreto, cuarentena con ticket/fecha, o eliminación justificada |

### Ejemplo (fragmento)

```json
{
  "status": "causa_confirmada",
  "failure_pattern": "falla ~1 de cada 8 corridas, solo cuando corre después de test_create_user",
  "root_cause_category": "orden/aislamiento",
  "confidence_score": 0.85
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Causa raíz (4) | `test_login_flow` depende de un usuario creado por `test_create_user` en la misma base de datos de prueba sin transacción aislada; cuando el orden de ejecución cambia (paralelización de CI), el usuario aún no existe — confirmado reproduciendo la falla 6/30 corridas al forzar el orden inverso |
| Recomendación (5) | Fix: crear el usuario de prueba dentro del propio `test_login_flow` (fixture con setup/teardown aislado) en vez de depender de otro test; no se recomienda cuarentena porque la causa ya está confirmada y el fix es de bajo riesgo |
