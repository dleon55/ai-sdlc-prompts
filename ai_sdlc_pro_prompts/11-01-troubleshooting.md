# 11.1 — Troubleshooting de ambiente

## Descripción

Prompt para analizar un problema de ambiente, despliegue, servicio, contenedor, pipeline o configuración: síntoma, servicios involucrados, hipótesis, comandos a revisar y ruta de resolución.

**Cuándo usarlo:** cuando un servicio falla, un despliegue no funciona como esperado, o hay un problema de configuración en cualquier ambiente.

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
