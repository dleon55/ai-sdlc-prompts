# 0-B.3 — Configuración de repositorio GitHub (protecciones, plantillas y settings)

## Descripción

Prompt para configurar el repositorio GitHub de forma completa y segura: protección de ramas, plantillas de issues y PRs, Dependabot, GitHub Actions permissions, Environments, secrets y quality gates. Alinea la plataforma con la metodología y el nivel de madurez del equipo.

**Cuándo usarlo:** al crear un repositorio nuevo, al estandarizar uno existente, o cuando el repo no tiene protecciones formales y se va a incorporar IA o múltiples contribuidores.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera la configuración completa del repositorio GitHub, sus protecciones y plantillas de trabajo.

Inputs requeridos:
- organización o usuario GitHub: [ORG/USER]
- nombre del repositorio: [REPO]
- metodología de branching: [GitFlow / GitHub Flow / Trunk-Based / otro]
- ramas protegidas: [ej: main, develop, release/*]
- equipo: [roles y tamaños, ej: 3 devs + 2 QA + AI agents]
- ambientes de despliegue: [dev / staging / prod]
- stack CI: [GitHub Actions / CircleCI / otro]

Entrega:

1. PROTECCIÓN DE RAMAS (Branch Protection Rules)
   Por cada rama protegida indica:
   - requires pull request before merging: sí/no, número de reviewers
   - require status checks: qué checks deben pasar (lint, tests, build)
   - require branches to be up to date: sí/no
   - require conversation resolution: sí/no
   - restrict who can push: lista de roles
   - allow force push: nunca en main/develop
   - allow deletions: sí/no
   - require signed commits: recomendación
   Entrega el comando gh CLI equivalente para cada regla.

2. GITHUB ACTIONS PERMISSIONS
   - workflow permissions (read-only tokens por defecto)
   - environments con required reviewers para staging y prod
   - restricción de qué workflows pueden usar cada secreto
   - OIDC vs PAT: recomendación por ambiente

3. DEPENDABOT
   Genera el archivo .github/dependabot.yml completo con:
   - ecosistema detectado según el stack
   - frecuencia de actualizaciones
   - límite de PRs abiertos
   - auto-merge para patch updates (solo si hay tests verdes)
   - ignore list para dependencias que no deben actualizarse

4. PLANTILLAS DE ISSUES (.github/ISSUE_TEMPLATE/)
   Genera los siguientes archivos con contenido completo:
   a) bug_report.md:
      - descripción del bug
      - pasos para reproducir
      - comportamiento esperado vs actual
      - ambiente (OS, versión, stack)
      - logs o capturas
      - criterios de aceptación para considerar el bug cerrado
   b) feature_request.md:
      - descripción funcional
      - problema que resuelve
      - comportamiento esperado
      - casos de uso
      - criterios de aceptación
      - dependencias o impacto en otros módulos
   c) ai_task.md (para tareas delegadas a agentes IA):
      - descripción de la tarea
      - contexto del repositorio relevante
      - archivos involucrados
      - restricciones y reglas
      - criterios de aceptación verificables por el agente
      - nivel de autonomía permitido
      - checklist de validación humana post-ejecución

5. PLANTILLA DE PULL REQUEST (.github/PULL_REQUEST_TEMPLATE.md)
   - descripción del cambio
   - issue relacionado (#)
   - tipo de cambio (feat / fix / docs / refactor / test / chore)
   - checklist: tests, docs, impacto en otros módulos, sin secretos, revisión de seguridad
   - instrucciones para el reviewer
   - notas para despliegue

6. CODEOWNERS (.github/CODEOWNERS o raíz)
   - mapa de responsables por directorio/tipo de archivo
   - regla especial: revisión humana obligatoria para cambios en /.github/, /workflows/, /migrations/

Formato de salida:
- contenido completo de cada archivo listo para copiar
- comandos gh CLI para configurar las protecciones de ramas
- tabla de resumen: área | configuración | prioridad | riesgo si se omite
```

---

## Uso con fórmula estándar

```text
Usa el prompt de configuración de repositorio GitHub y adáptalo a:
- repositorio: [ORG/REPO]
- metodología: [BRANCHING STRATEGY]
- stack CI: [GITHUB ACTIONS / OTRO]
- ambientes: [DEV / STAGING / PROD]
- equipo: [COMPOSICIÓN]
- documentos a revisar: workflows existentes, README, CONTRIBUTING
- objetivo puntual de salida: archivos ISSUE_TEMPLATE/, PR_TEMPLATE, dependabot.yml, CODEOWNERS + comandos gh CLI para branch protection
- nivel de profundidad: alto
```

---

## Salida esperada

| Área | Archivo/Configuración | Prioridad | Riesgo si se omite |
|---|---|---|---|
| Branch protection | `gh api` rules para main | Obligatorio | Commits directos, fuerza mayor sobre historial |
| Plantilla PR | `.github/PULL_REQUEST_TEMPLATE.md` | Obligatorio | PRs sin contexto, revisiones incompletas |
| Template bug | `.github/ISSUE_TEMPLATE/bug_report.md` | Obligatorio | Issues sin datos suficientes para reproducción |
| Template feature | `.github/ISSUE_TEMPLATE/feature_request.md` | Obligatorio | Requerimientos ambiguos sin criterios de aceptación |
| Template AI task | `.github/ISSUE_TEMPLATE/ai_task.md` | Obligatorio si se usan agentes | Agentes operando sin límites ni criterios claros |
| CODEOWNERS | `.github/CODEOWNERS` | Recomendado | PRs aprobados sin revisión del dueño del área |
| Dependabot | `.github/dependabot.yml` | Recomendado | Dependencias vulnerables no detectadas automáticamente |
| Environments | GitHub Settings → Environments | Recomendado | Despliegues a prod sin aprobación humana |
