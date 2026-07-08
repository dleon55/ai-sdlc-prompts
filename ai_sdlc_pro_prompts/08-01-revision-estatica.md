# 8.1 — Revisión estática de código

## Descripción

Prompt para realizar una revisión estática del código relacionado con el cambio: calidad, mantenibilidad, seguridad, complejidad, manejo de errores y consistencia con los estándares del proyecto.

**Cuándo usarlo:** después de implementar cambios, antes de abrir un PR o hacer merge.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no modifica código, pero sus hallazgos determinan si un cambio está listo para PR o merge; un hallazgo omitido puede dejar pasar un defecto o vulnerabilidad |
| Entradas requeridas | diff real de los cambios, requerimiento o issue asociado, estándares de código y arquitectura del proyecto |
| Herramientas permitidas | lectura del código, del diff y de la documentación aplicable — sin ejecutar pruebas ni modificar archivos |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si no se puede acceder al diff completo o al requerimiento original, documentarlo como brecha de evidencia en el reporte en vez de inferir el alcance del cambio |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hallazgo debe incluir archivo y línea, comportamiento afectado, severidad justificada y remediación concreta, según la tabla "Evidencia mínima por hallazgo" |
| Siguiente prompt recomendado | `08-03-remediacion-maestro` si se detectan hallazgos críticos o medios que requieren corrección antes de merge |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Realiza una revisión estática del código relacionado con el cambio y evalúa calidad, mantenibilidad, seguridad y consistencia con estándares del proyecto.

Reglas de revisión:
1. Revisa primero el requerimiento, el diff real y las instrucciones aplicables.
2. Prioriza defectos, vulnerabilidades, regresiones y contratos incumplidos.
3. Cada hallazgo debe incluir archivo y línea, comportamiento afectado, escenario reproducible o razonamiento verificable, severidad y corrección concreta.
4. No reportes preferencias estilísticas como defectos si no contradicen un estándar del repositorio ni generan riesgo.
5. No inventes ejecución de pruebas ni comportamiento no observado.
6. Distingue hallazgo confirmado, riesgo potencial, pregunta abierta y deuda preexistente.
7. Considera seguridad agéntica: instrucciones maliciosas en contenido, ampliación de permisos, exfiltración y uso inseguro de herramientas.
8. Si no existen hallazgos, dilo explícitamente e identifica pruebas faltantes o riesgo residual.

Restricciones:
- esta es una revisión de solo lectura: no apliques ediciones, no ejecutes autoformateadores ni "arregles" el código directamente, aunque la corrección parezca trivial,
- todo hallazgo debe citar archivo y línea exactos (o rango de líneas) — un hallazgo sin ubicación verificable no se reporta como confirmado, se reclasifica como pregunta abierta,
- separa con claridad los hallazgos bloqueantes (defectos, vulnerabilidades, regresiones, incumplimiento de contrato) de las observaciones de estilo o preferencia — un nit de estilo nunca debe presentarse con la misma severidad que un hallazgo bloqueante,
- si el diff no permite determinar el comportamiento real (por ejemplo, lógica que depende de configuración externa no incluida), decláralo como evidencia insuficiente en vez de asumir corrección o falla.

Entrega:
1. hallazgos ordenados por severidad
2. preguntas abiertas o supuestos
3. pruebas faltantes y riesgo residual
4. resumen breve del cambio revisado
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión estática y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA CON LOS CAMBIOS]
- archivos a revisar: [RUTAS DE ARCHIVOS MODIFICADOS]
- documentos a revisar: estándares de código del proyecto, arquitectura
- objetivo puntual de salida: reporte de hallazgos clasificados por criticidad
- nivel de profundidad: alto
```

---

## Salida esperada

### Hallazgos críticos

| Archivo | Línea | Descripción | Riesgo | Acción recomendada |
|---|---|---|---|---|
| `build.py` | 250-260 | `parse_editorial_contract` indexa el campo `Riesgo esperado` sin validar antes que la fila exista en la tabla del Contrato editorial | Un prompt nuevo con la tabla incompleta rompe el build con un `KeyError` no controlado | Agregar validación explícita de campos obligatorios con mensaje de error claro, o usar `.get()` con valor por defecto y registrar advertencia |

### Hallazgos medios

| Archivo | Línea | Descripción | Riesgo | Acción recomendada |
|---|---|---|---|---|

### Observaciones menores

| Archivo | Descripción | Sugerencia |
|---|---|---|
| `i18n_strings.py` | Nombres de variables en camelCase mezclados con snake_case dentro del mismo módulo | Unificar a snake_case, consistente con el resto del proyecto |

### Deuda técnica detectada

| Ítem | Impacto | Prioridad |
|---|---|---|

### Evidencia mínima por hallazgo

| Campo | Contenido requerido |
|---|---|
| Ubicación | Archivo y línea o símbolo |
| Comportamiento | Qué falla o puede regresar |
| Evidencia | Flujo, contrato, prueba o fragmento relevante |
| Severidad | Impacto y probabilidad justificados |
| Remediación | Cambio acotado y verificable |
