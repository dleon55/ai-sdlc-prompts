# 6.2 — Generación de mensajes de commit de calidad

## Descripción

Prompt para generar mensajes de commit pequeños, claros y trazables, alineados al estándar del proyecto. Incluye alternativas si el cambio debe dividirse en múltiples commits.

**Cuándo usarlo:** antes de hacer commit de cualquier cambio, para garantizar trazabilidad y consistencia con el historial del repositorio.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera mensajes de commit pequeños, claros, trazables y alineados al estándar del proyecto.

Entradas:
- issue,
- tipo de cambio,
- componente,
- descripción breve.

Entrega:
1. commit principal sugerido
2. commits alternativos si el cambio debe dividirse
3. justificación de por qué conviene dividir el trabajo
```

---

## Uso con fórmula estándar

```text
Usa el prompt de mensajes de commit y adáptalo a:
- issue: [NÚMERO O REFERENCIA]
- tipo de cambio: [feat / fix / refactor / docs / test / chore]
- componente: [MÓDULO O ARCHIVO AFECTADO]
- descripción breve: [QUÉ SE HIZO EN UNA LÍNEA]
- objetivo puntual de salida: commit principal + alternativas si aplica dividir
```

### Ejemplo real

```text
Usa el prompt de mensajes de commit y adáptalo a:
- issue: #842
- tipo de cambio: fix
- componente: api/notificaciones
- descripción breve: corrige envío duplicado de notificaciones push al actualizar orden
```

---

## Formatos de commit recomendados

```text
fix(api/notificaciones): corrige envío duplicado al actualizar orden #842

feat(auth): agrega validación de expiración de token en middleware #123

refactor(db): extrae consulta de usuarios a repositorio separado #456

docs(readme): actualiza instrucciones de despliegue en Docker #78

test(pagos): agrega casos borde para monto negativo en procesador #99
```

## Salida esperada

| Commit | Descripción | Justificación |
|---|---|---|
| Principal | | |
| Alternativa 1 | | |
| Alternativa 2 | | |
