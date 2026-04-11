# 4.3 — Diseño de casos de uso

## Descripción

Prompt para documentar formalmente los casos de uso del requerimiento o módulo analizado: actores, disparadores, flujos principal y alternos, reglas de negocio y criterios de aceptación.

**Cuándo usarlo:** durante la fase de diseño, para formalizar el comportamiento esperado del sistema antes de implementar.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Documenta formalmente los casos de uso relacionados con el requerimiento o módulo analizado.

Para cada caso de uso incluye:
- nombre,
- objetivo,
- actores,
- disparador,
- precondiciones,
- flujo principal,
- flujos alternos,
- postcondiciones,
- reglas de negocio,
- criterios de aceptación,
- componentes técnicos relacionados.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de casos de uso y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- módulo: [MÓDULO O FUNCIONALIDAD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: análisis funcional, documentación existente de CU
- objetivo puntual de salida: casos de uso formales listos para revisión y validación
- nivel de profundidad: alto
```

---

## Estructura de cada caso de uso

| Campo | Contenido |
|---|---|
| Nombre | Nombre del caso de uso |
| Objetivo | Qué logra este caso de uso |
| Actores | Quién lo ejecuta o participa |
| Disparador | Qué evento o acción lo inicia |
| Precondiciones | Qué debe ser verdad antes de ejecutar |
| Flujo principal | Secuencia de pasos del camino feliz |
| Flujos alternos | Variaciones y excepciones |
| Postcondiciones | Estado del sistema al terminar |
| Reglas de negocio | Restricciones y validaciones aplicables |
| Criterios de aceptación | Cómo verificar que está correctamente implementado |
| Componentes técnicos | Módulos, servicios y tablas involucradas |
