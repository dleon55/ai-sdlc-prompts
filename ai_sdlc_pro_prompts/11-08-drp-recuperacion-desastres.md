# 11-08 — Plan de recuperación ante desastres (DRP)

```text
Objetivo:
Guiar la recuperación total o parcial del sistema ante un desastre.

Inputs requeridos:
- tipo de desastre: [FALLA TOTAL / PARCIAL / RANSOMWARE / OTRO]
- sistemas afectados: [LISTA]
- responsable DRP: [NOMBRE]
- fecha/hora del incidente: [FECHA/HORA]

Procedimiento paso a paso:
1. Confirmar alcance y tipo de desastre.
2. Notificar a responsables y activar DRP.
3. Detener servicios afectados para evitar daños mayores.
4. Validar integridad de backups más recientes.
5. Restaurar sistemas críticos en ambiente de contingencia.
6. Validar funcionamiento y acceso.
7. Documentar acciones y tiempos.
8. Comunicar recuperación a stakeholders.
9. Realizar post-mortem y actualizar DRP si aplica.

Campos personalizables:
- [SISTEMAS], [RESPONSABLE], [FECHA], [TIPO DE DESASTRE]
```

## Descripción

Plantilla DRP para respuesta estructurada ante desastres. Incluye pasos críticos, campos personalizables y recomendaciones para documentación y mejora continua.

---

Ejemplo de uso:

- tipo de desastre: RANSOMWARE
- sistemas afectados: API, DB
- responsable DRP: Ana López
- fecha/hora: 2026-04-26 10:00
