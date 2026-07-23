# AI-SDLC Pro — Biblioteca de Prompts de Ingeniería de Software

Biblioteca interactiva de prompts estructurados bajo el **AI-SDLC Enterprise Framework**: **100 prompts** organizados en **18 secciones** que cubren el ciclo completo de ingeniería de software asistida por IA.

## Entornos activos

| Entorno | URL | Plataforma | Estado |
|---|---|---|---|
| **Producción** | https://prompts.lionsystems.com.mx | GCP Nginx + TLS | ✅ Live |
| **GitHub Pages** | https://dleon55.github.io/ai-sdlc-prompts | GitHub Pages CI/CD | ✅ Live |

---

## Funcionalidades del sitio

- **Proyectos con variables por entorno** — múltiples proyectos, cada uno con **19 variables** configurables (`repositorio`, `referencia/entrada`, `rama actual/destino`, `ambiente`, `componentes`, `módulo`, `stack`, `tipo de proyecto`, `metodología`, `agentes IA`, `nivel de autonomía`, `objetivo`, `responsable`, `workspace`, `estándar/compliance`, `documentos`, `profundidad`), más asignaciones adicionales `TOKEN=valor`. Variables persisten en `localStorage`, con acceso rápido desde un panel flotante además del panel completo. Exportables/importables como JSON para llevarlas a otra máquina o compartirlas con el equipo.
- **Registro de usuarios (opcional)** — inicio de sesión con GitHub vía Supabase Auth para sincronizar proyectos entre dispositivos; el uso anónimo con `localStorage` sigue funcionando igual sin necesidad de cuenta. Requiere configuración manual, ver [`docs/auth-setup.md`](docs/auth-setup.md).
- **Framework auto-prepend** — el bloque de contexto del framework se antepone automáticamente a cada prompt copiado, con validación bloqueante de placeholders obligatorios sin resolver antes de copiar.
- **Contrato editorial por prompt** — cada uno de los 100 prompts declara tipo, riesgo esperado, autonomía permitida y siguiente prompt recomendado, expuestos como badges filtrables y publicados en `prompts-index.json` para consumo por agentes de IA.
- **Filtros por riesgo y autonomía** — chips de faceta (`Bajo/Medio/Alto/Variable`, `A0-A3`) combinables con la búsqueda de texto y los filtros por sección.
- **Onboarding guiado** — banner + overlay de bienvenida para nuevos usuarios con guía de primeros pasos.
- **Multi-select** — selección de varios prompts para copiarlos en bloque.
- **Búsqueda/filtrado** — filtro en tiempo real por texto, nombre o contenido del prompt.
- **Modal de información ⓘ** — descripción y fórmulas de uso de cada prompt sin contaminar el contenido del prompt, con trampa de foco y atributos ARIA.
- **Sidebar colapsable** — navegación por sección.
- **Diseño oscuro responsive, bilingüe (ES/EN)** (self-contained, sin CDN — excepto el SDK de Supabase, que solo se carga si el registro de usuarios ya fue configurado).

---

## Servidor MCP

El catálogo también se expone a agentes de IA (Claude Code, Claude Desktop, Cursor) vía [Model Context Protocol](https://modelcontextprotocol.io), sin necesidad de copiar/pegar desde el navegador: `list_prompts`, `get_prompt`, `resolve_prompt` (sustituye variables), `get_framework` y `recommend_next`. Ver [mcp-server/README.md](mcp-server/README.md) para instalación y configuración.

---

## Estructura del proyecto

```
ai_sdlc_pro_prompts/    # 100 prompts Markdown (18 secciones, ciclo SDLC completo)
build.py                # Generador: produce index.html y prompts-index.json desde los .md
extract_vars.py         # Analiza tokens [PLACEHOLDER] en los prompts
verify_clean.py         # QA gate: valida prompts limpios (integrado en CI)
nginx_prompts.conf      # Config Nginx para producción GCP
deploy-to-gcp.sh        # Script de re-deploy manual a GCP
index.html              # Artefacto generado (~1.32 MB, no editar manualmente)
prompts-index.json      # Índice machine-readable (contrato editorial por prompt), no editar manualmente
mcp-server/             # Servidor MCP (Node) que expone el catálogo a agentes de IA vía stdio — ver mcp-server/README.md
docs/                   # Memorias técnicas (MT-001, MT-002)
.github/workflows/      # CI/CD — build + QA gate + deploy GitHub Pages + GCP
CONTRIBUTING.md         # Guía de contribución y convenciones
LICENSE                 # Licencia del proyecto
```

---

## Desarrollo local

```bash
# Regenerar index.html
python build.py

# Validar prompts limpios
python verify_clean.py

# Ver el sitio (Live Server en VSCode o doble clic)
# index.html se abre en el navegador — funciona sin servidor
```

---

## Flujo operativo

Todo trabajo técnico (P0/P1/P2) se gestiona en **GitHub Issues** con su **Milestone** y **Project** correspondientes — no en documentos transitorios del repositorio:

```
issue (milestone + project) → rama de trabajo → Pull Request → CI (gates) → merge controlado a main
```

1. **Issue**: se crea con objetivo, alcance, criterios de aceptación y evidencia esperada; se asigna a un Milestone y al Project de seguimiento.
2. **Rama**: se crea desde `main` actualizado (nunca se trabaja directo en `main` — política **OP-001**, ver [CONTRIBUTING.md](CONTRIBUTING.md)).
3. **Pull Request**: contra `main`, referenciando el issue que cierra.
4. **CI**: el workflow valida el PR (`build.py` + `verify_clean.py` + `pytest`) **sin desplegar**.
5. **Merge controlado**: requiere revisión; al mergear a `main`, `.github/workflows/deploy.yml` publica automáticamente en **GitHub Pages** (staging) y **GCP** (`prompts.lionsystems.com.mx`).

**Bitácora operativa:** las decisiones, el estado de avance y la evidencia (validaciones, diffs, resultados) se registran como **comentarios en el issue o el PR vinculado** — no en archivos nuevos del repositorio. El repo conserva solo documentación estable (README, CONTRIBUTING, arquitectura y políticas vigentes).

> `bash deploy-to-gcp.sh` queda como **respaldo manual** de re-deploy a GCP; el flujo normal no lo requiere.

---

## Agregar un nuevo prompt

1. Crea `ai_sdlc_pro_prompts/XX-YY-nombre-del-prompt.md` siguiendo el patrón existente.
2. Ejecuta `python build.py` y verifica localmente.
3. Ejecuta `python verify_clean.py` — debe reportar 0 prompts contaminados.
4. Haz commit en una **rama de trabajo** (no `main`) y abre un **Pull Request**; el CI valida el PR.
5. Al **mergear a `main`**, CI/CD despliega automáticamente a GitHub Pages y GCP producción.

---

## Secciones de prompts

| Grupo | Sección | Prompts |
|---|---|---|
| 00 | Framework base (obligatorio — se antepone en cada copia; no cuenta en el total) | 1 |
| 00-B | Scaffolding: repositorio, gobernanza, GitHub, metodología, stack | 5 |
| 00-C | Multi-agente: issues para IA, plan mode, configuración por agente | 3 |
| 00-D | Definición de proyecto: Project Charter, stack y arquitectura inicial | 2 |
| 01 | Comprensión del repositorio | 2 |
| 02 | Análisis (elicitación de requerimientos, issue, técnico, impacto cruzado, triage backlog, requerimientos) | 6 |
| 03 | Incidentes (GitHub, causa raíz) | 2 |
| 04 | Diseño de solución (diseño, Mermaid, casos de uso, ADR, versionado y deprecación de API) | 5 |
| 05 | Plan de implementación (plan, riesgos) | 2 |
| 06 | Ejecución (multi-agente, commits, coordinación de programa multi-agente) | 3 |
| 07 | Pruebas (diseño + implementación: stack, unitarias, integración, E2E, humo, automatización, performance, accesibilidad, diagnóstico de tests flaky, gestión de datos de prueba) | 15 |
| 08 | Revisión y remediación (estática, cumplimiento, maestro, SQL profiling, migración de esquema de BD) | 5 |
| 09 | Integración y CI/CD (ramas, monitoreo, workflows, promotion, feature flags, coordinación de breaking changes) | 6 |
| 10 | Documentación (técnica, memoria, changelog, observabilidad) | 4 |
| 11 | Operaciones (troubleshooting, hardening, deuda técnica, incident response, performance, parches, postmortem, FinOps, runbook de rollback, capacity planning, decomiso de sistemas legacy, ruido de alertas, salud de rotación on-call) | 13 |
| 12 | Orquestador maestro (ciclo completo) | 1 |
| 13 | Seguridad y DevSecOps (SAST, SCA, Secure SDLC, Threat Modeling, DAST, Pentesting, CVE, Secrets) | 8 |
| 14 | Monorepo y estándares (workspaces/dependencias, PSP/TSP, ISO/MoProSoft) | 3 |
| 15 | Negocio y QA funcional (historias Gherkin, casos de prueba manuales, defectos de negocio) | 3 |
| 16 | Soporte y Mesa de Ayuda (triage de tickets, diagnóstico y respuesta, base de conocimiento, SLA/escalamiento, tendencias, auditoría de salud de la KB) | 6 |
| 17 | Back Office de Ingeniería (onboarding/offboarding técnico, evaluación de herramientas, capacidad del equipo, renovación de vendors, reporte de estado a stakeholders) | 6 |
| **Total** | | **100** |

---

## Documentación técnica

| Documento | Descripción |
|---|---|
| [docs/MT-001](docs/MT-001-publicacion-github-pages.md) | Memoria técnica — publicación GitHub Pages con CI/CD |
| [docs/MT-002](docs/MT-002-feature-proyectos-gcp-deploy.md) | Memoria técnica — feature Proyectos + despliegue GCP |
| [CHANGELOG.md](CHANGELOG.md) | Historial de cambios por versión |

---

> Parte del stack AI-SDLC Enterprise — LionSystems © 2026
