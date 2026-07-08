# 13.2 — SCA: Análisis de composición de software y dependencias

## Descripción

Prompt para analizar las dependencias de terceros del proyecto e identificar vulnerabilidades conocidas (CVEs), licencias problemáticas, dependencias abandonadas y riesgos de cadena de suministro (supply chain). Aplica a dependencias directas e indirectas (transitivas).

**Cuándo usarlo:** en cada PR que modifique dependencias, como revisión periódica (al menos mensual), antes de un release a producción, y como respuesta a alertas de seguridad publicadas (GitHub Dependabot, OSS-Index, etc.).

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | seguridad |
| Riesgo esperado | medio — análisis de solo lectura, pero una vulnerabilidad de cadena de suministro no detectada o mal priorizada puede escalar a alto si no se remedia a tiempo |
| Entradas requeridas | archivos de gestión de dependencias y lock files del proyecto (package.json, requirements.txt, go.mod, etc.), tipo de producto (comercial/open source/interno) para el análisis de licencias; hallazgos previos de `13-07` si existen |
| Herramientas permitidas | lectura de archivos de dependencias y lock files; recomienda comandos de pip-audit/npm audit/Snyk/Trivy/etc., pero no los ejecuta ni modifica versiones instaladas |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si no hay acceso a lock files, declarar el análisis como incompleto e indicar qué falta en vez de simular CVEs inexistentes; escalar a legal/compliance ante licencias problemáticas o sin licencia detectada |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada CVE reportado incluye paquete, versión instalada, CVSS y versión con fix disponible (o mitigación alternativa si no existe fix) |
| Siguiente prompt recomendado | `13-07-gestion-vulnerabilidades-cves` para triaje y priorización de los CVEs y licencias encontradas |

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

Restricciones:
- nunca inventes un CVE, un CVSS o un estado de fix — reporta solo vulnerabilidades verificables en bases públicas (NVD, GitHub Advisory Database, OSV) y marca como "requiere confirmación con herramienta de auditoría" cualquier hallazgo que no puedas verificar directamente,
- este es un análisis de solo lectura: no ejecutes `npm audit fix`, `pip install --upgrade` ni ningún comando que modifique versiones instaladas o archivos de lock — entrega los comandos para que un humano los ejecute,
- si detectas un token o credencial embebido en un archivo de dependencias, lock file o configuración de registro privado, trátalo como secreto: nunca reveles su valor, solo su ubicación y tipo,
- ante una licencia problemática o sin licencia detectada, escala a legal/compliance en vez de asumir que es aceptable para el tipo de producto,
- si no tienes acceso a los lock files, declara el análisis como incompleto e indica exactamente qué falta en vez de simular CVEs inexistentes.

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
| `lodash` | 4.17.15 | CVE-2020-8203 | 7.4 | Prototype pollution: permite añadir o modificar propiedades arbitrarias del objeto global vía `_.merge`/`_.zipObjectDeep` con input no confiable | 4.17.19 | Actualizar inmediatamente |
| `axios` | 0.21.1 | CVE-2021-3749 | 5.3 | ReDoS por expresión regular vulnerable en el manejo de `trailing slash` de URLs | 0.21.2 | Actualizar en el próximo sprint |

### Plan de actualización

| Paquete | De versión | A versión | Cambio | Riesgo de breaking change | Prioridad |
|---|---|---|---|---|---|
| `lodash` | 4.17.15 | 4.17.21 | Menor | Bajo — sin cambios de API pública | 1 |
| `axios` | 0.21.1 | 0.21.4 | Parche | Bajo — compatible, solo corrige el parseo de URL | 2 |
