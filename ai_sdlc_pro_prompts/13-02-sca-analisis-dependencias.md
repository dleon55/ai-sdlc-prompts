# 13.2 — SCA: Análisis de composición de software y dependencias

## Descripción

Prompt para analizar las dependencias de terceros del proyecto e identificar vulnerabilidades conocidas (CVEs), licencias problemáticas, dependencias abandonadas y riesgos de cadena de suministro (supply chain). Aplica a dependencias directas e indirectas (transitivas).

**Cuándo usarlo:** en cada PR que modifique dependencias, como revisión periódica (al menos mensual), antes de un release a producción, y como respuesta a alertas de seguridad publicadas (GitHub Dependabot, OSS-Index, etc.).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Si hay hallazgos de `13-07` (Gestión de CVEs), adjúntalo para correlacionar con el estado de triaje actual.

---

## Prompt completo

```text
Objetivo:
Analiza las dependencias de terceros del proyecto para identificar vulnerabilidades
conocidas (CVEs), licencias problemáticas, dependencias abandonadas y riesgos de
cadena de suministro (supply chain attack).

Pasos:

1. INVENTARIO DE DEPENDENCIAS
   Identifica los archivos de gestión de dependencias presentes:
   - Python: requirements.txt, requirements-dev.txt, Pipfile, pyproject.toml
   - JavaScript/Node: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
   - Java: pom.xml, build.gradle
   - Ruby: Gemfile, Gemfile.lock
   - Go: go.mod, go.sum
   - PHP: composer.json, composer.lock
   - .NET: *.csproj, packages.config

   Para cada archivo detectado:
   - lista el total de dependencias directas
   - lista el total de dependencias transitivas (si el lock file está disponible)
   - identifica si se usa pinning exacto de versiones o rangos permisivos

2. HERRAMIENTAS DE ANÁLISIS RECOMENDADAS
   Según el lenguaje detectado, proporciona los comandos exactos para ejecutar el análisis:
   - Python: pip-audit, safety check, dependabot
   - JavaScript: npm audit, yarn audit, npm audit --json
   - Java: OWASP Dependency-Check, mvn dependency-check:check
   - Ruby: bundle audit
   - Go: govulncheck ./...
   - PHP: composer audit
   - Multi-lenguaje: Snyk (snyk test), Trivy (trivy fs .), Grype (grype dir:.)
   - GitHub: Dependabot alerts + Security Advisories

3. ANÁLISIS DE VULNERABILIDADES CONOCIDAS
   Para cada vulnerabilidad detectada (o simulada si no hay acceso a ejecución):
   - paquete afectado y versión instalada
   - CVE ID y puntuación CVSS v3.1
   - descripción del impacto
   - versión con fix disponible
   - si no hay fix: mitigación alternativa
   - si el proyecto realmente usa la funcionalidad vulnerable (análisis de alcance)

4. ANÁLISIS DE LICENCIAS
   Clasifica las licencias encontradas:
   - PERMISIVAS (MIT, BSD, Apache 2.0): sin restricciones comerciales
   - COPYLEFT DÉBIL (LGPL, MPL): condiciones específicas de distribución
   - COPYLEFT FUERTE (GPL, AGPL): requiere apertura del código si se distribuye
   - PROBLEMÁTICAS o SIN LICENCIA: riesgo legal — escalar a legal/compliance

5. SALUD DE LAS DEPENDENCIAS
   Para las 20 dependencias más críticas (por uso y acceso a datos):
   - última versión disponible vs versión instalada
   - fecha del último commit en el repositorio de la dependencia
   - número de mantenedores activos
   - si la dependencia fue abandonada o deprecada oficialmente
   - si la dependencia tiene más de 2 años sin actualizarse: marcar como riesgo

6. RIESGOS DE CADENA DE SUMINISTRO (Supply Chain)
   Evalúa los siguientes vectores:
   - ¿Se usa lock file con hashes de integridad? (npm --integrity, pip hash)
   - ¿Se publican las dependencias desde registros oficiales? (npmjs.com, pypi.org)
   - ¿Hay dependencias con nombres similares a paquetes populares? (typosquatting)
   - ¿El pipeline de CI valida la integridad de las dependencias antes de instalarlas?
   - ¿Se usan dependencias de repositorios git directamente (sin versión fija)?

7. PRIORIZACIÓN Y PLAN DE REMEDIACIÓN
   Clasifica los hallazgos:
   - CRÍTICO: CVE con CVSS ≥ 9.0 o licencia GPL en producto comercial
   - ALTO: CVE con CVSS 7.0-8.9 o dependencia abandonada en ruta crítica
   - MEDIO: CVE con CVSS 4.0-6.9 o dependencia desactualizada > 2 años
   - BAJO: CVE con CVSS < 4.0 o licencia ambigua
   - INFORMATIVO: dependencia con actualizaciones menores disponibles

Entrega:
- inventario de dependencias con versiones y estado de seguridad,
- tabla de CVEs encontrados con severidad y fix disponible,
- tabla de licencias con clasificación de riesgo,
- reporte de salud de dependencias críticas,
- plan de actualización priorizado,
- comandos de remediación listos para ejecutar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de SCA y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL O DE TRABAJO]
- lenguaje(s): [AUTO-DETECTAR]
- tipo de producto: [COMERCIAL / OPEN SOURCE / INTERNO] — afecta análisis de licencias
- herramienta preferida: [AUTO-DETECTAR / npm audit / pip-audit / Snyk / Trivy]
- documentos a revisar: archivos de dependencias, lock files, Dependabot alerts activos
- objetivo puntual de salida: reporte de CVEs + licencias + plan de actualización
- nivel de profundidad: alto
```

---

## Salida esperada

### Resumen de vulnerabilidades

| Severidad | Cantidad | Con fix disponible | Sin fix |
|---|---|---|---|
| Crítico | N | N | N |
| Alto | N | N | N |
| Medio | N | N | N |
| Bajo | N | N | N |

### Tabla de CVEs

| Paquete | Versión instalada | CVE | CVSS | Descripción | Fix en versión | Acción |
|---|---|---|---|---|---|---|
| nombre-paquete | x.y.z | CVE-YYYY-NNNNN | 9.8 | Descripción del impacto | x.y.z+1 | Actualizar inmediatamente |

### Plan de actualización

| Paquete | De versión | A versión | Cambio | Riesgo de breaking change | Prioridad |
|---|---|---|---|---|---|
| nombre-paquete | x.y.z | a.b.c | Mayor | Alto — revisar migración | 1 |
