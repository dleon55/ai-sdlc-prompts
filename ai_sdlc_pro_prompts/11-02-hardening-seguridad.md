# 11.2 — Hardening y seguridad operativa

## Descripción

Prompt para analizar el repositorio y la configuración operativa en busca de oportunidades de fortalecimiento de seguridad: hardening, manejo de secretos, permisos, exposición de servicios y riesgos de despliegue.

**Cuándo usarlo:** periódicamente como revisión de seguridad, antes de un despliegue a producción, o cuando se detectan hallazgos de seguridad en code review.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el repositorio y la configuración operativa para detectar oportunidades de fortalecimiento de seguridad, hardening, manejo de secretos, permisos, exposición de servicios y riesgos de despliegue.

Entrega:
- hallazgos,
- criticidad,
- mitigación,
- prioridad.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de hardening y seguridad y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- ambiente: [PROD / STAGING]
- componentes: [INFRAESTRUCTURA, SERVICIOS, CONFIGURACIONES]
- documentos a revisar: docker-compose, nginx, .env, workflows, permisos de GitHub
- objetivo puntual de salida: reporte de hallazgos de seguridad con plan de mitigación priorizado
- nivel de profundidad: alto
```

---

## Salida esperada

| Hallazgo | Categoría | Criticidad | Componente | Mitigación | Prioridad |
|---|---|---|---|---|---|
| | secretos expuestos | | | | |
| | permisos excesivos | | | | |
| | servicios expuestos | | | | |
| | configuración insegura | | | | |
| | dependencias vulnerables | | | | |
| | logging insuficiente | | | | |
