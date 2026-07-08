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

Compara:
- lo solicitado,
- lo diseñado,
- lo implementado,
- lo probado.

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

### Resultado de cumplimiento

| Ítem | Estado | Diferencias | Riesgo | Acción requerida |
|---|---|---|---|---|
