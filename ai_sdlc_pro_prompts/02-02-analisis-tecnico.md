# 2.2 - Análisis técnico profundo de código existente

## Descripción

Prompt de análisis estático y trazable para reconstruir cómo funciona realmente el código relacionado con un requerimiento o incidente. Examina el flujo end-to-end, contratos, datos, dependencias, seguridad, observabilidad, pruebas, deuda técnica y riesgos de regresión sin modificar archivos.

**Cuándo usarlo:** después del análisis funcional (`02-01`) y antes del análisis de impacto cruzado (`02-03`) y del diseño de la solución (`04-01`).

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — es la base para el análisis de impacto cruzado (`02-03`) y el diseño (`04-01`); un mapeo incorrecto del flujo, contratos o dependencias propaga errores a esas fases, aunque el prompt no modifica archivos |
| Entradas requeridas | resultado de `02-01`, repositorio o workspace, issue o requerimiento, rama o commit objetivo, ambiente, documentos y contratos a revisar |
| Herramientas permitidas | lectura de código, logs e historial git; ejecución no destructiva limitada a inspecciones, compilaciones o pruebas enfocadas ya aprobadas por el proyecto (máximo tres ciclos de autocorrección) — sin editar archivos ni hacer commits |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si el comportamiento no puede verificarse en runtime, declararlo como análisis estático; si el `status` del JSON de metadatos resulta `blocked`, detener y escalar en vez de forzar conclusiones |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hallazgo y riesgo debe citar ruta, símbolo y línea; cada verificación ejecutada debe registrar comando, resultado y limitaciones |
| Siguiente prompt recomendado | `02-03-impacto-cruzado` |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el código existente relacionado con el requerimiento o incidente y documenta, con evidencia verificable, cómo funciona realmente en el estado actual del repositorio.

Restricciones:
- Trabaja en modo de solo análisis. No modifiques archivos, no generes código y no realices commits.
- No completes vacíos con suposiciones presentadas como hechos.
- Excluye de búsquedas recursivas: **/node_modules/**, **/venv/**, **/.git/**, **/dist/**, **/build/** y **/*.log.
- Usa rutas exactas y referencias de línea cuando la herramienta lo permita.
- Si no puedes verificar un comportamiento por ejecución, decláralo como análisis estático.

Entradas:
- repositorio o workspace: [NOMBRE, URL O RUTA]
- issue o requerimiento: [REFERENCIA Y DESCRIPCIÓN]
- rama o commit objetivo: [RAMA / SHA]
- ambiente: [LOCAL / DEV / QA / PROD]
- componentes o módulos iniciales: [LISTA O DESCONOCIDO]
- documentos y contratos a revisar: [RUTAS O DESCONOCIDO]
- nivel de profundidad: [MEDIO / ALTO / FORENSE]

Actividades:
1. Realiza el preflight y registra:
   - rama, commit y estado del árbol de trabajo;
   - cambios recientes relevantes, ramas y worktrees activos;
   - archivos modificados sin confirmar y posibles conflictos con otros agentes;
   - políticas, estándares, documentación y archivos de gobierno aplicables.
2. Delimita el alcance:
   - traduce el requerimiento a comportamientos técnicos observables;
   - identifica puntos de entrada, salidas, actores, datos y sistemas externos;
   - declara qué queda dentro y fuera del análisis.
3. Localiza los artefactos involucrados:
   - rutas, módulos, paquetes, capas y propietarios;
   - clases, funciones, endpoints, jobs, eventos, comandos y componentes UI;
   - modelos, tablas, migraciones, consultas, cachés y almacenamiento;
   - configuración, variables de entorno, feature flags, secretos referenciados y permisos;
   - pruebas, fixtures, mocks, pipelines y documentación relacionada.
4. Reconstruye el flujo end-to-end actual, desde la entrada hasta la respuesta o efecto final:
   - UI o consumidor;
   - routing/controlador;
   - aplicación o caso de uso;
   - dominio y reglas de negocio;
   - persistencia, mensajería e integraciones;
   - manejo de errores, reintentos, transacciones, idempotencia y concurrencia;
   - logs, métricas, trazas y alertas.
5. Traza dependencias y fronteras:
   - imports y llamadas internas relevantes;
   - dependencias entre paquetes o workspaces;
   - contratos API, eventos, esquemas y compatibilidad;
   - dependencias externas y versiones cuando estén declaradas;
   - acoplamientos circulares, acceso indebido entre capas o fronteras vulneradas.
6. Evalúa comportamiento y calidad:
   - validaciones, autorización, autenticación y tratamiento de datos sensibles;
   - estados vacíos, carga, error, éxito y accesibilidad si existe UI;
   - deuda técnica, duplicación, complejidad y código muerto;
   - cobertura existente y escenarios críticos sin prueba;
   - diferencias entre documentación, configuración, pruebas y código ejecutable.
7. Verifica de forma no destructiva cuando sea viable:
   - ejecuta solo inspecciones, compilaciones o pruebas enfocadas aprobadas por el proyecto;
   - registra comando, resultado y limitaciones;
   - aplica el límite máximo de tres ciclos de autocorrección definido por el framework.
8. Clasifica cada afirmación como:
   - HECHO CONFIRMADO: respaldado por código, configuración, prueba o ejecución;
   - HALLAZGO: conclusión técnica derivada de evidencia citada;
   - SUPUESTO: hipótesis pendiente de confirmar;
   - RIESGO: posible impacto con probabilidad y severidad;
   - RECOMENDACIÓN: siguiente acción, sin implementarla.
9. Finaliza con preguntas abiertas y la evidencia que falta para confirmar el comportamiento en runtime.

Formato de salida:
0. Metadatos JSON válidos y sin comentarios:
   {
     "status": "complete|partial|blocked",
     "analysis_mode": "static|static_and_runtime",
     "repository": "",
     "branch": "",
     "commit": "",
     "scope": [],
     "entry_points": [],
     "file_dependencies": [{"from": "", "to": "", "type": "import|call|data|event|config"}],
     "couplings": [{"source": "", "target": "", "evidence": "", "severity": "low|medium|high|critical"}],
     "risks": [{"id": "", "description": "", "probability": "low|medium|high", "impact": "low|medium|high|critical"}],
     "verification": [{"command": "", "result": "passed|failed|not_run", "evidence": ""}],
     "open_questions": []
   }
1. Resumen ejecutivo
2. Alcance, exclusiones y estado del repositorio
3. Flujo end-to-end actual
4. Mapa de componentes, capas y dependencias
5. Contratos, datos, seguridad y observabilidad
6. Archivos relevantes con ruta, símbolo, líneas y función
7. Pruebas existentes, cobertura observable y validaciones ejecutadas
8. Hechos confirmados
9. Hallazgos técnicos priorizados
10. Supuestos y preguntas abiertas
11. Riesgos de modificación
12. Recomendaciones y orden sugerido para el análisis de impacto (`02-03`)

Criterios de calidad:
- Cada hallazgo y riesgo referencia evidencia concreta.
- Se distingue código vigente de código legado, generado, de prueba o no utilizado.
- El flujo incluye rutas alternativas y manejo de errores, no solo el camino feliz.
- No se afirma comportamiento de runtime basándose únicamente en nombres de archivos.
- La salida permite continuar con `02-03` y `04-01` sin repetir el levantamiento.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis técnico profundo y adáptalo a:
- repositorio: [NOMBRE O URL]
- workspace/subproyecto: [RUTA O NO APLICA]
- issue o requerimiento: [REFERENCIA]
- rama o commit: [RAMA / SHA]
- ambiente: [LOCAL / DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: [RUTAS]
- objetivo puntual de salida: flujo actual verificable + mapa de dependencias + riesgos de modificación
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Estado, alcance, dependencias, acoplamientos, riesgos y verificaciones |
| Resumen y alcance (1-2) | Resultado ejecutivo, exclusiones y estado Git analizado |
| Flujo actual (3) | Secuencia end-to-end, variantes, errores y efectos laterales |
| Arquitectura técnica (4-5) | Capas, fronteras, contratos, datos, seguridad y observabilidad |
| Evidencia (6-8) | Rutas, símbolos, líneas, pruebas y hechos confirmados |
| Evaluación (9-11) | Hallazgos, supuestos y riesgos priorizados |
| Continuidad (12) | Recomendaciones para impacto cruzado y diseño posterior |
