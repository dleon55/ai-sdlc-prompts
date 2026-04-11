# 9.3 — Revisión de workflows de GitHub Actions

## Descripción

Prompt para auditar los workflows del repositorio y verificar si cubren adecuadamente validación, pruebas, seguridad, despliegue y calidad. Detecta vacíos, riesgos y propone mejoras.

**Cuándo usarlo:** periódicamente como revisión de salud del pipeline, o al incorporar nuevos módulos o ambientes.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza los workflows del repositorio y determina si cubren adecuadamente validación, pruebas, seguridad, despliegue y calidad.

Incluye:
- inventario de workflows,
- disparadores,
- jobs,
- validaciones existentes,
- faltantes,
- riesgos,
- mejoras recomendadas.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de revisión de workflows y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- documentos a revisar: .github/workflows/, README de CI/CD
- objetivo puntual de salida: inventario de workflows con brechas y mejoras recomendadas
- nivel de profundidad: medio
```

---

## Salida esperada

### Inventario de workflows

| Workflow | Archivo | Disparador | Jobs | Propósito |
|---|---|---|---|---|

### Análisis de cobertura

| Área | Cubierta | Workflow | Faltante | Riesgo | Recomendación |
|---|---|---|---|---|---|
| validación / lint | | | | | |
| build | | | | | |
| pruebas unitarias | | | | | |
| pruebas integración | | | | | |
| análisis seguridad | | | | | |
| despliegue DEV | | | | | |
| despliegue QA | | | | | |
| despliegue PROD | | | | | |
| notificaciones | | | | | |
