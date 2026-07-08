# 1.1 — Inventario técnico del repositorio

## Descripción

Prompt de arranque para construir un inventario técnico inicial del repositorio: estructura, workspaces/sub-módulos, tecnologías detectadas, artefactos del ciclo de ingeniería y vacíos relevantes. Es el primer paso recomendado antes de cualquier análisis o implementación sobre un repositorio nuevo o desconocido.

**Cuándo usarlo:** al arrancar trabajo sobre un repositorio del que no se tiene contexto previo, o para refrescar el inventario después de cambios estructurales significativos.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — es un inventario de solo lectura; un vacío o imprecisión se corrige en iteraciones posteriores y no genera cambios en el repositorio |
| Entradas requeridas | acceso de lectura al repositorio completo (código fuente, configuración, documentación existente); no requiere issue ni incidente de referencia |
| Herramientas permitidas | lectura de estructura de carpetas, código, configuración y documentación — sin ejecución ni cambios |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si partes del repositorio no son accesibles o el monorepo tiene workspaces no resueltos, declarar el alcance cubierto y los vacíos en vez de inferir estructura no verificada |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada carpeta, tecnología o artefacto listado en el inventario debe corresponder a una ruta o archivo verificable en el repositorio |
| Siguiente prompt recomendado | `01-02-analisis-procesos` para mapear el gobierno del proyecto; `02-01-analisis-issue` si ya existe un issue o requerimiento concreto que atender |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Quiero que analices integralmente este repositorio y construyas un inventario técnico inicial del proyecto.

Actividades:
1. Revisa la estructura completa del repositorio (detectando si es un monorrepositorio o proyecto modular).
2. Identifica:
   - workspaces / subproyectos / sub-módulos,
   - dependencias y fronteras entre paquetes internos,
   - componentes,
   - módulos,
   - capas,
   - servicios,
   - librerías internas,
   - scripts,
   - pipelines,
   - pruebas,
   - documentación,
   - archivos de configuración,
   - contenedores,
   - migraciones,
   - variables de entorno.
3. Detecta tecnologías utilizadas:
   - frontend,
   - backend,
   - base de datos,
   - infraestructura,
   - mensajería,
   - autenticación,
   - observabilidad.
4. Ubica los artefactos del ciclo de ingeniería y alineación con estándares (PSP, ISO, etc.):
   - análisis,
   - diseño,
   - casos de uso,
   - diagramas,
   - implementación,
   - pruebas,
   - CI/CD,
   - documentación.
5. Detecta vacíos o ausencias relevantes.

Restricciones:
- este es un análisis de solo lectura: no ejecutes instalaciones, builds, migraciones ni cambios en el repositorio para completar el inventario,
- no asumas convenciones no documentadas (nomenclatura, estructura de carpetas, versión de dependencias) solo porque parecen consistentes en los archivos revisados; verifícalas antes de generalizarlas como regla del proyecto,
- si una carpeta, workspace o dependencia no es accesible o no se pudo inspeccionar, decláralo como vacío de cobertura en el inventario en vez de inferir su contenido,
- si la documentación existente está desactualizada, incompleta o contradice lo observado en el código, señala la discrepancia explícitamente en vez de asumir cuál de las dos fuentes es la vigente.

Formato de salida:
1. Resumen ejecutivo
2. Inventario de carpetas y propósito
3. Arquitectura detectada
4. Tecnologías y versiones encontradas
5. Procesos/documentación localizados
6. Riesgos o vacíos
7. Recomendación de orden de revisión
```

---

## Uso con fórmula estándar

```text
Usa el prompt de inventario técnico del repositorio y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- documentos a revisar: código fuente completo, configuración, documentación existente
- objetivo puntual de salida: inventario técnico inicial con riesgos y vacíos detectados
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen ejecutivo | Panorama general del repositorio en pocas líneas |
| Inventario de carpetas | Estructura y propósito de cada carpeta principal |
| Arquitectura detectada | Monorepo/modular, capas, componentes y servicios identificados |
| Tecnologías | Stack de frontend, backend, BD, infraestructura, mensajería, auth, observabilidad |
| Procesos/documentación | Artefactos del ciclo de ingeniería ya presentes |
| Riesgos o vacíos | Ausencias relevantes detectadas |
| Orden de revisión | Recomendación de por dónde continuar el análisis |

### Ejemplo (fragmento)

| Sección | Ejemplo de contenido |
|---|---|
| Resumen ejecutivo | Librería estática bilingüe de prompts para agentes IA (`ai_sdlc_pro_prompts/*.md` + `.en.md`); sin backend ni base de datos, el sitio se genera con `build.py` a partir de pares ES/EN. |
| Tecnologías | Python 3.x (`build.py`, `extract_vars.py`), Markdown como formato de contenido, pytest para pruebas (`tests/`), GitHub Actions para despliegue (`.github/workflows/deploy.yml`); sin framework de frontend. |
| Riesgos o vacíos | No se encontró documentación de la estrategia de branching más allá de `CONTRIBUTING.md`; falta un ADR que explique por qué el índice se genera estáticamente en vez de servirse dinámicamente. |
