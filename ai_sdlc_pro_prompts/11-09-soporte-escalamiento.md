# 11-09 — Protocolo de atención y escalamiento de tickets

```text
Objetivo:
Estandarizar la atención, escalamiento y cierre de tickets de soporte.

Inputs requeridos:
- ticket ID: [ID]
- prioridad: [BAJA / MEDIA / ALTA / CRÍTICA]
- responsable inicial: [NOMBRE]
- canal de comunicación: [EMAIL / SLACK / OTRO]

Flujo:
1. Registrar ticket y clasificar prioridad.
2. Asignar responsable y notificar.
3. Documentar diagnóstico inicial y acciones tomadas.
4. Si no se resuelve en [X] horas, escalar a siguiente nivel.
5. Notificar al usuario sobre el estado y tiempos estimados.
6. Documentar solución y pasos realizados.
7. Cerrar ticket con confirmación del usuario.

Campos personalizables:
- [ID], [PRIORIDAD], [RESPONSABLE], [CANAL]
```

## Descripción

Protocolo reutilizable para soporte y escalamiento. Permite documentar, escalar y cerrar tickets de manera controlada, asegurando trazabilidad y satisfacción del usuario.

---

Ejemplo de uso:

- ticket ID: 1234
- prioridad: ALTA
- responsable inicial: Carlos Ruiz
- canal: soporte@empresa.com
