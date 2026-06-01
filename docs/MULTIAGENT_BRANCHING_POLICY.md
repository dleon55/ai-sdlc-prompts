# Politica de Branching e Integracion Multi-Agente

Fecha de entrada en vigor: 2026-05-31
Estado: Activa
Alcance: Repositorio WEB_PROMPTS y coordinacion con workspace raiz

## 1) Objetivo

Reducir conflictos entre agentes, mantener trazabilidad y asegurar integraciones controladas con commits atomicos.

## 2) Regla de congelamiento de main (OP-001)

- Se congela el push directo a main durante ejecucion multi-agente.
- Toda integracion a main requiere revision previa y ventana de integracion.
- Ventanas sugeridas: 12:00 y 18:00 (hora local).

## 3) Convencion de ramas (OP-003)

Formato:

<tipo>/<scope>/<ticket>-<descripcion-corta>

Tipos permitidos:
- feat
- fix
- docs
- ops
- sec
- qa
- chore

Ejemplos:
- feat/prompts/iss-142-nuevo-prompt-performance
- fix/build/iss-155-bug-parser-formulas
- ops/ci/iss-160-hardening-workflow

## 4) Reglas de integracion

- Un objetivo tecnico por rama.
- Commits atomicos por unidad logica.
- Rebase/fetch antes de solicitar integracion.
- Resolver conflictos en la rama de trabajo, no en main.
- Prohibido mezclar cambios de raiz y subrepositorio en el mismo commit de integracion.

## 5) Checklist minimo antes de integrar

- git fetch actualizado
- rama local sin conflictos pendientes
- pruebas minimas ejecutadas
- changelog/documentacion actualizada si aplica
- evidencia de validacion adjunta

## 6) Coordinacion entre repositorio raiz y subrepositorio

- WEB_PROMPTS: aplica flujo Git completo con ramas y PR.
- Workspace raiz: al no tener .git en la raiz, registrar decisiones y cambios en bitacora operativa y ejecutar validacion cruzada antes de aplicar cambios productivos.

## 7) Evidencias operativas esperadas

- Estado de ramas activas y remotas
- Log corto actualizado tras integracion
- Registro de ventana de integracion utilizada
