# 9.3 — Revisión de workflows de GitHub Actions

## Descripción

Prompt para auditar los workflows del repositorio y verificar si cubren adecuadamente validación, pruebas, seguridad, despliegue y calidad. Detecta vacíos, riesgos y propone mejoras.

**Cuándo usarlo:** periódicamente como revisión de salud del pipeline, o al incorporar nuevos módulos o ambientes.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — no modifica workflows directamente, solo audita y recomienda |
| Entradas requeridas | contenido de `.github/workflows/`, README de CI/CD |
| Herramientas permitidas | lectura de archivos de workflow — sin ejecución de jobs ni cambios al pipeline |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si un workflow referencia secretos o permisos no inspeccionables sin acceso a la configuración del repositorio, documentarlo como brecha de visibilidad en vez de asumir su estado |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada brecha reportada debe citar el archivo de workflow y el job específico |
| Siguiente prompt recomendado | `11-02-hardening-seguridad` si se detectan brechas de seguridad en el pipeline |

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
