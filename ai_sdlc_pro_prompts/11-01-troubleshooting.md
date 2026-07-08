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

Pasos:
1. Reproduce el problema: intenta reproducir el síntoma de forma controlada (mismo input, mismo ambiente si es posible) antes de teorizar sobre la causa — sin una reproducción confiable, cualquier hipótesis es especulación.
2. Aísla variables: identifica qué cambió respecto al último estado conocido como funcional (código, configuración, datos, infraestructura, dependencias externas) para acotar el espacio de búsqueda.
3. Revisa primero los cambios recientes: prioriza deploys, cambios de configuración, actualizaciones de dependencias o migraciones de los últimos días — la mayoría de los incidentes de ambiente se correlacionan con un cambio reciente, no con una causa espontánea.
4. Recolecta evidencia de solo lectura: logs, estado de servicios, métricas (CPU, memoria, latencia, tasa de error) y trazas relacionadas con el síntoma, sin modificar nada del ambiente en este paso.
5. Formula hipótesis ordenadas por probabilidad: para cada una, indica cómo validarla con evidencia concreta (no solo intuición) y qué resultado la confirmaría o la descartaría.
6. Valida o descarta cada hipótesis en orden, documentando el resultado de cada verificación — incluidas las que no llevan a nada, porque delimitan el problema para quien continúe la investigación.
7. Converge en la causa raíz: no te detengas en el primer síntoma coincidente; confirma que la causa explica por completo el comportamiento observado, no solo una parte de él.
8. Propón la ruta de resolución: pasos concretos para resolver, señalando cuáles requieren aprobación humana antes de ejecutarse (reinicios, rollbacks, cambios de configuración).
9. Verifica que la solución propuesta ataca la causa raíz y no solo enmascara el síntoma (ej: reiniciar un servicio que alivia temporalmente un memory leak sin resolverlo) — señala explícitamente si una acción es paliativa o definitiva.

Restricciones:
- prioriza comandos de solo lectura para diagnóstico (logs, estado de servicios, métricas); no ejecutes reinicios, rollbacks, cambios de configuración ni comandos destructivos — inclúyelos como parte de la "ruta de resolución" propuesta, pendiente de aprobación,
- no apliques ni recomiendes aplicar una corrección sin haber confirmado la causa raíz con evidencia: una corrección sobre una hipótesis no verificada puede ocultar el problema real o introducir uno nuevo,
- no ejecutes ni propongas ejecutar ninguna acción contra producción sin aprobación humana explícita, incluso si el diagnóstico sugiere una solución obvia,
- documenta el rastro completo de la investigación, incluidas las hipótesis descartadas y los callejones sin salida — esa traza evita que alguien repita la misma verificación fallida en un incidente futuro,
- si el ambiente es PROD y hay impacto significativo en usuarios, detente y deriva a `11-04-incident-response` en vez de continuar con este troubleshooting estándar.

Entrega:
- síntoma,
- servicios involucrados,
- revisión sugerida,
- comandos o evidencias revisadas,
- hipótesis ordenadas con su validación,
- ruta de resolución.
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

### Ejemplo aplicado

| Hipótesis | Probabilidad | Cómo validarla | Resultado |
|---|---|---|---|
| El deploy de las 14:32 introdujo una variable de entorno faltante | Alta | Revisar el diff del deploy y los logs de arranque del contenedor | Confirmada — el contenedor loguea `KeyError: DATABASE_URL` tras el deploy `a1b2c3d` |
| El certificado TLS del balanceador expiró | Media | `openssl s_client -connect lb.internal:443` y revisar la fecha de expiración | Descartada — certificado válido hasta 2027-01 |
