# 11-07 — Checklist de salud operativa diaria

```text
Objetivo:
Realizar un checklist de salud diaria para el sistema/proyecto.

Inputs requeridos:
- ambiente: [DEV / QA / PROD]
- servicios críticos: [LISTA]
- responsables: [NOMBRES]
- fecha: [FECHA]

Checklist:
- [ ] Todos los servicios están activos y responden a healthcheck.
- [ ] No hay alertas críticas en el monitoreo.
- [ ] Backups automáticos ejecutados y verificados.
- [ ] Espacio en disco y recursos dentro de umbrales.
- [ ] No hay errores en logs críticos.
- [ ] Tareas de mantenimiento programadas ejecutadas.
- [ ] Incidentes abiertos revisados y asignados.
- [ ] Checklist firmado por: [RESPONSABLE]
```

## Descripción

Checklist reutilizable para validar la salud operativa diaria de sistemas críticos. Permite personalizar servicios, responsables y ambiente. Facilita la trazabilidad y cumplimiento de rutinas de operación.

---

Ejemplo de uso:

- ambiente: PROD
- servicios críticos: API, DB, Redis
- responsables: Juan Pérez
- fecha: 2026-04-26
