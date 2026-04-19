# 7.0 — Detección de stack de pruebas

## Descripción

Prompt para detectar y documentar el stack de pruebas activo en el repositorio. Produce un **perfil de stack de pruebas** estructurado que se adjunta como contexto a los prompts de implementación (`07-07` al `07-10`), eliminando la necesidad de que cada agente re-descubra las herramientas y convenciones del proyecto.

**Cuándo usarlo:** una sola vez por proyecto, o cuando el stack de pruebas cambie. El perfil generado se reutiliza en todas las ejecuciones de los prompts de implementación de pruebas.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Detecta y documenta el stack de pruebas del repositorio para producir un perfil
reutilizable que contextualice los prompts de implementación de pruebas.

Pasos de detección:

1. CONFIGURACIÓN DEL PROYECTO
   Revisa los archivos de configuración raíz del proyecto:
   - package.json / package-lock.json / yarn.lock / pnpm-lock.yaml
   - pyproject.toml / setup.cfg / requirements*.txt / Pipfile
   - pom.xml / build.gradle / build.sbt
   - Gemfile / .ruby-version
   - go.mod / go.sum
   - Cualquier archivo de configuración de framework detectado

2. FRAMEWORKS DE PRUEBA
   Identifica el framework activo para cada tipo:

   a) Pruebas unitarias:
      - lenguaje principal del proyecto
      - framework de pruebas unitarias (pytest, Jest, Vitest, JUnit, RSpec, Go test, etc.)
      - library de mocks/stubs (unittest.mock, pytest-mock, jest.mock, Sinon, Mockito, etc.)
      - configuración de cobertura (pytest-cov, nyc/c8, JaCoCo, SimpleCov, etc.)

   b) Pruebas de integración:
      - estrategia de integración (fixtures de DB, Testcontainers, docker-compose, etc.)
      - herramienta de HTTP testing (supertest, httpx, RestAssured, etc.)
      - proveedores de datos de prueba (factories, fixtures, seeders)

   c) Pruebas E2E:
      - framework E2E instalado (Playwright, Cypress, Selenium, Puppeteer, Robot Framework, etc.)
      - idioma de los scripts E2E (si difiere del lenguaje principal)
      - uso de Page Object Model u otro patrón de abstracción UI

   d) Smoke tests:
      - scripts existentes de smoke/healthcheck
      - endpoints de salud disponibles (/health, /ping, /status, etc.)
      - integración con pipeline CI/CD

3. CONVENCIONES DEL PROYECTO
   Detecta las convenciones activas:
   - directorio de pruebas: dónde viven los tests (tests/, __tests__/, spec/, src/**/*.test.*)
   - patrón de nombres de archivos: test_*.py, *.test.ts, *_spec.rb, etc.
   - patrón de nombres de funciones/métodos: test_*, it(), describe(), should_*, etc.
   - estructura interna preferida: AAA (Arrange/Act/Assert), Given/When/Then, etc.

4. PIPELINE CI/CD
   Revisa los workflows existentes:
   - archivos en .github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc.
   - steps que ejecutan pruebas: comandos exactos usados
   - configuración de coverage reporting y umbral mínimo si existe

5. ESTADO ACTUAL
   Reporta:
   - ¿Existen tests ya escritos? ¿Cuántos y en qué estado?
   - ¿Hay configuración de cobertura activa? ¿Cuál es el umbral actual?
   - ¿Hay tests fallando actualmente?

Entrega:
Produce el perfil de stack de pruebas en el formato estándar definido abajo.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de detección de stack de pruebas y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL O DE TRABAJO]
- documentos a revisar: archivos de configuración raíz, package.json/pyproject.toml,
  .github/workflows/, directorio de tests existente
- objetivo puntual de salida: perfil de stack de pruebas completo y verificado
- nivel de profundidad: medio
```

---

## Salida esperada — Perfil de stack de pruebas

El agente debe generar un bloque con este formato exacto, listo para ser copiado y pegado como contexto en los prompts 07-07 al 07-10:

```
── PERFIL DE STACK DE PRUEBAS ──────────────────────────────────────────
Repositorio : [nombre o URL]
Rama        : [rama analizada]
Fecha       : [fecha de detección]

LENGUAJE PRINCIPAL : [lenguaje]
RUNTIME / VERSIÓN  : [versión]

── PRUEBAS UNITARIAS ───────────────────────────────────────────────────
Framework         : [nombre y versión]
Librería de mocks : [nombre y versión]
Cobertura         : [herramienta] — umbral mínimo: [X%] | sin configurar
Directorio        : [ruta relativa]
Patrón de nombres : [patrón de archivos]
Comando de ejecución:
  [comando completo verificado]

── PRUEBAS DE INTEGRACIÓN ──────────────────────────────────────────────
Estrategia       : [fixtures / Testcontainers / docker-compose / sin detectar]
HTTP testing     : [herramienta o sin detectar]
Datos de prueba  : [factories / fixtures / seeders / sin detectar]
Directorio       : [ruta relativa]
Comando de ejecución:
  [comando completo verificado o sin detectar]

── PRUEBAS E2E ─────────────────────────────────────────────────────────
Framework        : [nombre y versión o sin detectar]
Idioma scripts   : [lenguaje]
Patrón UI        : [Page Object / sin patrón / sin detectar]
URL base QA      : [URL o variable de entorno]
Directorio       : [ruta relativa]
Comandos:
  headless : [comando]
  headed   : [comando]

── SMOKE / HEALTHCHECK ─────────────────────────────────────────────────
Script existente : [ruta o sin detectar]
Endpoints salud  : [lista de endpoints o sin detectar]
Integración CI   : [sí — step: X / no]

── PIPELINE CI/CD ──────────────────────────────────────────────────────
Plataforma       : [GitHub Actions / GitLab CI / Jenkins / sin detectar]
Archivo          : [ruta del workflow]
Steps de prueba  : [comandos exactos del workflow]
Coverage gate    : [umbral en CI o sin configurar]

── CONVENCIONES ────────────────────────────────────────────────────────
Estructura tests : [AAA / Given-When-Then / sin convención explícita]
Naming funciones : [patrón detectado]
Patrón archivos  : [patrón detectado]

── ESTADO ACTUAL ───────────────────────────────────────────────────────
Tests existentes : [N archivos / N tests]
Tests fallando   : [N o ninguno]
Cobertura actual : [X% o sin medir]

── NOTAS Y SUPUESTOS ───────────────────────────────────────────────────
[cualquier hallazgo relevante, ambigüedad o recomendación]
────────────────────────────────────────────────────────────────────────
```

> Este bloque debe pegarse al inicio (después del bloque de `00-framework.md`) de cualquier
> prompt de implementación de pruebas: `07-07`, `07-08`, `07-09`, `07-10`.
