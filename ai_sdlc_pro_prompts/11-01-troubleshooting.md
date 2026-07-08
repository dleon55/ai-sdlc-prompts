# 11.1 — Troubleshooting de ambiente

## Descripción

Prompt para analizar un problema de ambiente, despliegue, servicio, contenedor, pipeline o configuración: síntoma, servicios involucrados, hipótesis, comandos a revisar y ruta de resolución.

**Cuándo usarlo:** cuando un servicio falla, un despliegue no funciona como esperado, o hay un problema de configuración en cualquier ambiente. Si el ambiente es PROD y hay impacto significativo en usuarios, usa `11-04-incident-response` en su lugar.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — analiza un ambiente con posible impacto en servicio; si el ambiente es PROD con impacto significativo, el propio prompt exige derivar a `11-04-incident-response` |
| Entradas requeridas | síntoma, ambiente (DEV/QA/STAGING/PROD), servicios involucrados, evidencias disponibles (logs, errores, capturas) |
| Herramientas permitidas | solo lectura para diagnóstico (logs, estado de servicios, métricas); prohibido explícitamente ejecutar reinicios, rollbacks, cambios de configuración o comandos destructivos |
| Autonomía permitida | A0 — Analizar: diagnóstico e hipótesis; la ruta de resolución queda propuesta y pendiente de aprobación antes de pasar a A2 |
| Criterios de detención | si el ambiente es PROD y hay impacto significativo en usuarios, debe detenerse y derivar a `11-04-incident-response` en vez de continuar el troubleshooting estándar |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | hipótesis ordenadas por probabilidad con evidencia asociada, y comandos de diagnóstico limitados a solo lectura |
| Siguiente prompt recomendado | `11-04-incident-response` si escala a incidente en PROD con impacto significativo; `03-02-causa-raiz` si se requiere análisis de causa raíz formal tras resolver |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza un problema de ambiente, despliegue, servicio, contenedor, pipeline o configuración y determina posibles causas, validaciones necesarias y ruta de solución.

Incluye:
- síntoma,
- servicios involucrados,
- revisión sugerida,
- comandos o evidencias a revisar,
- hipótesis,
- ruta de resolución.

⚠️ Prioriza comandos de solo lectura para diagnóstico (logs, estado de servicios, métricas). No ejecutes reinicios, rollbacks, cambios de configuración o comandos destructivos — inclúyelos como parte de la "ruta de resolución" propuesta, pendientes de aprobación.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de troubleshooting de ambiente y adáptalo a:
- repositorio: [NOMBRE O URL]
- síntoma: [DESCRIPCIÓN DEL PROBLEMA]
- ambiente: [DEV / QA / STAGING / PROD]
- servicios involucrados: [CONTENEDORES, SERVICIOS, PIPELINES]
- evidencias disponibles: [LOGS, ERRORES, CAPTURAS]
- documentos a revisar: configuraciones, docker-compose, nginx, variables de entorno
- objetivo puntual de salida: hipótesis ordenadas + comandos de diagnóstico + ruta de resolución
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido |
|---|---|
| Síntoma | Comportamiento observado con evidencia |
| Servicios involucrados | Contenedores, servicios y componentes afectados |
| Revisión sugerida | Qué revisar primero y por qué |
| Comandos a ejecutar | Comandos de diagnóstico ordenados |
| Hipótesis | Posibles causas por orden de probabilidad |
| Ruta de resolución | Pasos concretos para resolver |
