# 10.2 — Memoria técnica del cambio

## Descripción

Prompt para generar una memoria técnica clara y ejecutiva del cambio realizado: contexto, problema, análisis, solución implementada, pruebas, riesgos, resultados y puntos pendientes.

**Cuándo usarlo:** al cierre de cada issue o sprint, como registro formal del trabajo realizado para auditoría y referencia futura.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera una memoria técnica clara y ejecutiva del cambio realizado.

Incluye:
1. contexto
2. problema o requerimiento
3. análisis
4. causa raíz si aplica
5. solución implementada
6. componentes modificados
7. pruebas ejecutadas
8. riesgos
9. resultados
10. puntos pendientes
```

---

## Uso con fórmula estándar

```text
Usa el prompt de memoria técnica y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA INTEGRADA]
- ambiente: [PROD / STAGING]
- componentes: [COMPONENTES MODIFICADOS]
- documentos a revisar: commits, PRs, diseño aprobado, resultados de pruebas
- objetivo puntual de salida: memoria técnica completa para auditoría
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido |
|---|---|
| Contexto | Antecedentes del cambio |
| Problema / Requerimiento | Qué se necesitaba resolver |
| Análisis | Hallazgos del análisis previo |
| Causa raíz | Si aplica, causa confirmada |
| Solución implementada | Qué se hizo exactamente |
| Componentes modificados | Lista de archivos y módulos |
| Pruebas ejecutadas | Tipos de prueba y resultados |
| Riesgos | Residuales o pendientes |
| Resultados | Estado final del sistema |
| Puntos pendientes | Tareas derivadas o deuda nueva |
