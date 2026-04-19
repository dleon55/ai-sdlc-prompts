# 11.6 — Gestión de Parches y Actualizaciones

## Descripción

Prompt para planificar y ejecutar el ciclo completo de gestión de parches: inventario de dependencias y componentes, evaluación de criticidad de actualizaciones, plan de aplicación por entorno, verificación de regresiones y documentación del ciclo. Cubre dependencias de aplicación, sistema operativo, contenedores e infraestructura.

**Cuándo usarlo:** como revisión periódica de actualizaciones pendientes (mensual/trimestral), al recibir alertas de CVE que afectan dependencias del proyecto (`13-02` SCA), o antes de un release mayor para garantizar componentes actualizados.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Si existe resultado de `13-02` (SCA) o `13-07` (Gestión de vulnerabilidades), adjúntalo para priorizar parches de seguridad.

---

## Prompt completo

```text
Objetivo:
Planificar y ejecutar el ciclo completo de gestión de parches para el proyecto:
inventariar componentes desactualizados, evaluar criticidad de cada actualización,
definir el plan de aplicación por entorno con criterios de rollback, verificar que no
se introducen regresiones y documentar el estado del parche para auditoría.

Pasos:

1. INVENTARIO DE COMPONENTES A PARCHEAR
   Generar el inventario completo de componentes que pueden tener actualizaciones:
   
   a) Dependencias de aplicación (por gestor de paquetes):
      - Node.js: `npm outdated` o `yarn outdated`
      - Python: `pip list --outdated` o `pip-review`
      - PHP: `composer outdated`
      - Java/Maven: `mvn versions:display-dependency-updates`
      - Ruby: `bundle outdated`
      - Go: `go list -m -u all`
      - .NET: `dotnet list package --outdated`
   
   b) Imágenes de contenedor (si aplica Docker):
      - imágenes base usadas en Dockerfiles: ¿hay versiones más recientes?
      - imágenes de servicios auxiliares (BD, caché, proxy): ¿versiones actuales vs. disponibles?
      - ¿se usan tags flotantes (`:latest`) que enmascaran versiones reales?
   
   c) Sistema operativo y runtime (si se gestiona infraestructura):
      - parches de SO pendientes: Ubuntu/Debian (`apt list --upgradable`), RHEL (`yum check-update`)
      - versión del runtime: Node.js, Python, Java, PHP — ¿en versión LTS con soporte activo?
      - versión del servidor web / proxy: Nginx, Apache, Caddy
   
   d) Herramientas de infraestructura:
      - versión de Kubernetes / Helm / kubectl
      - versión de Terraform / Ansible / CDK
      - versión de agentes de CI/CD (runners, agents)
      - certificados TLS: fecha de expiración (alertar si < 30 días)

2. CLASIFICACIÓN DE ACTUALIZACIONES
   Para cada componente desactualizado, clasificar:
   
   Tipo de actualización (semver):
   - PATCH (x.x.N → x.x.N+1): corrección de bugs — riesgo bajo, aplicar siempre
   - MINOR (x.N.x → x.N+1.x): nueva funcionalidad retrocompatible — riesgo medio, revisar changelog
   - MAJOR (N.x.x → N+1.x.x): posible breaking change — riesgo alto, requiere testing completo
   
   Categoría de la actualización:
   - SEGURIDAD: soluciona CVE — prioridad máxima, SLA según CVSS
   - CORRECCIÓN: resuelve bug que nos afecta — prioridad alta
   - CORRECCIÓN: resuelve bug que no nos afecta directamente — prioridad media
   - MEJORA: nueva funcionalidad — prioridad baja, evaluar en ciclo planificado
   - DEPRECACIÓN: avisa de eliminación futura en próxima MAJOR — planificar migración
   
   Matriz de prioridad:
   | Categoría | PATCH | MINOR | MAJOR |
   |---|---|---|---|
   | Seguridad CRÍTICO | Aplicar < 24h | Aplicar < 7 días | Evaluar urgente |
   | Seguridad ALTO | Aplicar < 7 días | Aplicar < 30 días | Evaluar en sprint |
   | Bug que nos afecta | Aplicar este sprint | Evaluar | Planificar |
   | Mejora / Otro | Ciclo mensual | Ciclo trimestral | Evaluar roadmap |

3. ANÁLISIS DE IMPACTO Y RIESGO
   Para actualizaciones MINOR y MAJOR:
   
   a) Revisar el changelog / release notes entre la versión actual y la nueva:
      - ¿hay cambios en la API que usen en el proyecto? (breaking changes)
      - ¿hay cambios de comportamiento por defecto que puedan afectar tests?
      - ¿hay nuevas dependencias transitivas que introduzcan conflictos?
   
   b) Evaluar la superficie de cambio en el proyecto:
      - ¿cuántos archivos usan la dependencia directamente?
      - ¿test coverage cubre el código que usa esta dependencia?
      - ¿hay workarounds o patches locales que puedan romperse?
   
   c) Riesgo de regresión:
      - BAJO: dependencia con buena cobertura de tests, sin breaking changes, PATCH o MINOR sin API changes
      - MEDIO: dependencia importante, MINOR con algunos cambios de API, cobertura parcial
      - ALTO: dependencia crítica, MAJOR, breaking changes, cobertura baja

4. PLAN DE APLICACIÓN POR ENTORNO
   Definir la secuencia de aplicación por entorno con validaciones intermedias:
   
   Entorno 1 — Desarrollo (local / rama feature):
   - aplicar la actualización en rama dedicada: `chore/update-[package]-vX.Y.Z`
   - ejecutar suite de pruebas completa: unitarias + integración + E2E
   - revisar manualmente flujos críticos si los tests no tienen cobertura completa
   - criterio de avance: 0 tests fallidos, sin errores en startup
   
   Entorno 2 — Staging:
   - desplegar la rama con la actualización a staging
   - ejecutar smoke tests (`07-10`) para validar que el sistema arranca correctamente
   - ejecutar benchmark de performance (`07-11`) para detectar regresiones de rendimiento
   - dejar activo en staging mínimo 24 horas antes de promover a producción
   
   Entorno 3 — Producción:
   - desplegar en ventana de mantenimiento de bajo tráfico (si el cambio tiene riesgo MEDIO o ALTO)
   - despliegue canary o blue-green si está disponible
   - monitor activo durante 1 hora post-despliegue: métricas, tasa de error, logs
   - criterio de rollback: tasa de error > N% o P95 > umbral × 1.5 durante 5 minutos
   
   Plan de rollback:
   - definir el commit o versión anterior exacta a restaurar
   - tiempo estimado de rollback: [minutos]
   - responsable de autorizar el rollback: [rol]

5. AGRUPACIÓN PARA MINIMIZAR DISRUPCIONES
   Organizar las actualizaciones en grupos lógicos para aplicar de forma eficiente:
   
   Grupo 1 — Actualizaciones de seguridad urgentes (aplicar inmediatamente):
   - listar CVEs críticos/altos con SLA vencido o próximo a vencer
   
   Grupo 2 — Correcciones de PATCH + actualizaciones de seguridad medias/bajas:
   - agrupar en un único PR para minimizar ruido
   
   Grupo 3 — Actualizaciones MINOR sin breaking changes:
   - aplicar una por una con tests intermedios, o en lotes pequeños con buena cobertura
   
   Grupo 4 — Actualizaciones MAJOR / breaking changes:
   - cada una en su propio PR, con spike de análisis previo si es crítica
   - planificar en sprint dedicado

6. DOCUMENTACIÓN Y AUDITORÍA
   Al completar el ciclo de parches:
   - generar el registro del ciclo: fecha, componentes actualizados, versiones, resultado de tests
   - actualizar el CHANGELOG del proyecto con las actualizaciones de dependencias
   - actualizar el inventario de dependencias (si se mantiene separado)
   - registrar cualquier actualización postergada (con justificación y fecha de revisión siguiente)
   - reportar estado a stakeholders: "N componentes actualizados, M postergados, K pendientes de versión MAJOR"

7. AUTOMATIZACIÓN PREVENTIVA
   Si no existe automatización, proponer:
   - Dependabot (GitHub) o Renovate: PRs automáticos de actualización con grouping configurado
   - alertas automáticas de CVE sobre dependencias (GitHub Security Advisories, Snyk, Socket)
   - pipeline de CI que ejecute `npm audit` / `pip-audit` / `trivy` en cada PR
   - certificados TLS monitoreados con alerta de expiración a 30 y 7 días

Entregables:
- inventario de componentes desactualizados con clasificación (tipo, categoría, prioridad),
- tabla de plan de parches por grupo con secuencia de entornos y criterios de rollback,
- análisis de riesgo para actualizaciones MINOR y MAJOR,
- registro de auditoría del ciclo de parches completado,
- recomendaciones de automatización preventiva para el proyecto.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de gestión de parches y adáptalo a:
- repositorio: [NOMBRE O URL]
- stack tecnológico: [lenguaje, gestor de paquetes, runtime, contenedores]
- ambientes disponibles: [dev / staging / producción]
- contexto de vulnerabilidades: [ADJUNTAR RESULTADO DE 13-02 SCA si existe]
- herramientas de CI/CD: [GitHub Actions / GitLab CI / Jenkins / otro]
- automatización existente: [Dependabot / Renovate / ninguna]
- última vez que se aplicaron parches: [fecha]
- SLAs de seguridad comprometidos: [estándar de SLA por severidad de CVE]
- documentos a revisar: package.json, requirements.txt, Dockerfile, Terraform/Helm files
- objetivo de salida específico: inventario + plan agrupado + análisis de riesgo
- nivel de profundidad: alto
```

---

## Resultado esperado

### Inventario de actualizaciones pendientes

| Componente | Versión actual | Versión disponible | Tipo | Categoría | Prioridad | Riesgo |
|---|---|---|---|---|---|---|
| `express` | 4.17.1 | 4.21.2 | PATCH | Seguridad — CVE-2024-43796 | CRÍTICO | Bajo |
| `django` | 4.1.0 | 5.0.4 | MAJOR | Seguridad + nuevas features | ALTO | Alto |
| `lodash` | 4.17.20 | 4.17.21 | PATCH | Corrección de bug | Media | Bajo |
| `react` | 17.0.2 | 18.3.1 | MAJOR | Mejora — Concurrent Mode | Baja | Alto |
| Imagen base node | `node:18-alpine` | `node:22-alpine` | MAJOR | LTS upgrade | Media | Alto |

### Plan de parches agrupado

| Grupo | Componentes | Entorno inicio | Fecha estimada | Responsable |
|---|---|---|---|---|
| 1 — Seguridad urgente | `express` + 2 CVEs más | Dev → Staging → Prod | Esta semana | Backend lead |
| 2 — PATCH + Seguridad media | `lodash` + 8 más | Dev → Staging | Este sprint | Cualquier dev |
| 3 — MINOR sin breaking | 12 dependencias | Dev → Staging | Próximo sprint | Tech lead |
| 4 — MAJOR (`django`) | `django` 4→5 | Análisis previo primero | Q3 | Equipo completo |
