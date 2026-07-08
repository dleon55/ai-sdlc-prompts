# 8.2 — Revisión de cumplimiento contra requerimiento

## Descripción

Prompt para validar si la implementación realmente cumple con el issue, requerimiento, caso de uso y criterios de aceptación. Compara lo solicitado, lo diseñado, lo implementado y lo probado.

**Cuándo usarlo:** antes de cerrar un issue o abrir un PR para merge, como paso de cierre de calidad.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | validación |
| Riesgo esperado | medio — el veredicto determina si un issue puede cerrarse; un falso "cumple" puede cerrar trabajo incompleto y un falso "no cumple" bloquea innecesariamente |
| Entradas requeridas | issue o requerimiento original, diseño aprobado, código implementado, resultados de pruebas |
| Herramientas permitidas | lectura del issue, diseño, código y resultados de pruebas existentes — sin ejecutar pruebas nuevas ni modificar código |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si falta alguno de los cuatro insumos a comparar (lo solicitado, lo diseñado, lo implementado o lo probado), detener y reportarlo como brecha de evidencia antes de emitir un veredicto de cumplimiento |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada criterio de aceptación debe quedar marcado como cumplido, parcial o no cumplido, con la brecha específica citada en la matriz |
| Siguiente prompt recomendado | `09-01-integracion-ramas` si el cumplimiento es total y el cambio queda listo para integrar |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Valida si la implementación realmente cumple con el issue, requerimiento, caso de uso y criterios de aceptación.

Pasos:
1. Reúne los cuatro insumos a comparar: issue o requerimiento original, diseño aprobado, código implementado y resultados de pruebas; si falta alguno, detente y repórtalo como brecha de evidencia antes de continuar.
2. Compara lo solicitado contra lo diseñado: verifica que el diseño aprobado cubra literalmente cada criterio de aceptación del issue y señala cualquier caso que el diseño haya dejado fuera.
3. Compara lo diseñado contra lo implementado: verifica que cada decisión del diseño se haya traducido en código real, no en un subconjunto simplificado o en un atajo no documentado.
4. Compara lo implementado contra lo probado: verifica que exista evidencia de prueba para cada criterio de aceptación, no solo para el camino feliz — la ausencia de prueba es una brecha aunque el código "se vea correcto".
5. Para cada criterio de aceptación, asigna un estado (cumple / parcial / no cumple) citando la brecha específica que lo sustenta; nunca marques "cumple" sin evidencia trazable a los cuatro insumos.
6. Prioriza las brechas por riesgo: una brecha en un criterio de negocio crítico o de seguridad pesa más que una brecha cosmética o de nomenclatura.

Restricciones:
- no marques un criterio como "cumple" si no hay evidencia de prueba que lo respalde, aunque el código parezca correcto a simple vista,
- no ejecutes pruebas nuevas ni modifiques código — esta revisión es de solo lectura sobre evidencia existente,
- si falta alguno de los cuatro insumos (solicitado, diseñado, implementado, probado), detén el análisis y repórtalo como brecha de evidencia en vez de asumir cumplimiento,
- distingue explícitamente entre "no implementado" y "no probado" — son brechas distintas que requieren acciones distintas.

Entrega:
- cumplimiento total/parcial/no cumple,
- diferencias detectadas,
- riesgos por incumplimiento,
- acciones requeridas.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de cumplimiento contra requerimiento y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA CON LOS CAMBIOS]
- documentos a revisar: issue original, diseño aprobado, código implementado, resultados de pruebas
- objetivo puntual de salida: matriz de cumplimiento con brechas y acciones requeridas
- nivel de profundidad: alto
```

---

## Salida esperada

| Criterio de aceptación | Solicitado | Diseñado | Implementado | Probado | Estado | Brecha |
|---|---|---|---|---|---|---|
| El usuario puede exportar el listado filtrado por rango de fechas a CSV | sí — issue #482 lo pide explícitamente | sí — sección 3.2 del diseño aprobado | sí — endpoint `GET /reports/export` acepta `from`/`to` | no — solo existe test de exportación sin filtro | parcial | falta caso de prueba que cubra el filtro de fecha |
| La exportación de 10k registros debe completarse en menos de 5s (NFR) | sí — NFR listado en el issue | no — el diseño no define estrategia de paginación ni streaming | no verificable sin diseño de referencia | no | no cumple | el requerimiento de performance nunca se tradujo a diseño ni a prueba |

### Resultado de cumplimiento

| Ítem | Estado | Diferencias | Riesgo | Acción requerida |
|---|---|---|---|---|
| Filtro de fecha sin prueba automatizada | parcial | la prueba unitaria cubre la exportación pero no el parámetro de fecha | bug silencioso si el filtro se rompe en un refactor futuro | agregar caso de prueba con rango de fechas antes de cerrar el issue |
| NFR de performance no diseñado ni probado | no cumple | el issue exige <5s para 10k registros; no hay evidencia de diseño ni de prueba de carga | exportaciones grandes podrían agotar el tiempo de espera (timeout) en producción | definir estrategia de paginación/streaming y ejecutar `07-06-pruebas-performance-carga` antes del merge |
