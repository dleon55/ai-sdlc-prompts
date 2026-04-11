# MT-002 — Feature: Proyectos con Variables por Entorno + Despliegue GCP

| Campo | Valor |
|---|---|
| **ID** | MT-002 |
| **Tipo** | Feature + Infraestructura / DevOps |
| **Fecha** | 2026-04-10 |
| **Autor** | David León Gómez (dleon55) |
| **Repositorio** | https://github.com/dleon55/ai-sdlc-prompts |
| **Commits** | `513891d` → `ac074bb` → `2d84005` → `568a40b` |
| **Rama** | `main` |
| **Ambientes** | GitHub Pages (CI/CD) + GCP Nginx (`prompts.lionsystems.com.mx`) |
| **Estado** | Completado ✓ |

---

## 1. Contexto

El sitio **AI-SDLC Pro** (`index.html` generado por `build.py`) tenía un panel de variables estático: 7 campos de texto que se vaciaban al recargar la página y no soporten múltiples contextos de proyecto en simultáneo.

Adicionalmente, el sitio solo estaba disponible en GitHub Pages (`dleon55.github.io`) sin dominio propio, sin HTTPS personalizado y sin estar integrado al servidor de producción de LionSystems en GCP.

---

## 2. Requerimiento

### 2.1 Feature — Proyectos con variables por entorno
Inspirado en el modelo de Postman/Codex: permitir al usuario crear múltiples "proyectos" (ej. `API Backend`, `Odoo Staging`, `urgemy-dev`), cada uno con su propio set de 7 variables. Al cambiar de proyecto activo, el panel de variables se actualiza automáticamente. Los valores persisten en `localStorage`.

### 2.2 Infraestructura — Despliegue en producción GCP
Publicar el sitio en `https://prompts.lionsystems.com.mx` — dominio propio, certificado TLS, servidor Nginx en GCP (`34.51.112.6:2288`).

---

## 3. Análisis

### 3.1 Hechos confirmados

| Hecho | Evidencia |
|---|---|
| `build.py` genera `index.html` self-contained (sin CDN) | `python build.py` → 145 KB inicial |
| JS embebido en `JS = """..."""` (Python triple-quoted string) | Grep en `build.py` |
| `getVarValues()` leía directamente del DOM | Línea ~637 de `build.py` |
| `clearVars()` limpiaba inputs del DOM por ID | Línea ~691 de `build.py` |
| DNS `prompts.lionsystems.com.mx` ya apuntaba a `34.51.112.6` | `host prompts.lionsystems.com.mx` |
| Certbot v2.1.0 disponible en servidor | `which certbot` |
| Nginx v1.22.1 activo | `systemctl status nginx` |
| Puerto 80/443 abiertos en UFW | `ufw status` |

### 3.2 Hallazgos

- El bloque `JS = """..."""` es un Python triple-quoted string. Los `\'` dentro de él son consumidos por Python, resultando en `'` en el output → colisión de comillas en el JS generado → `SyntaxError` crítico.
- Disco raíz del servidor al **77%** (25G/35G).
- Sin script de re-deploy documentado — proceso manual no reproducible.

### 3.3 Supuestos

- `localStorage` disponible en todos los navegadores objetivo (Chrome, Firefox, Edge modernos).
- Los IDs de proyectos son suficientemente únicos con `Math.random().toString(36)`.
- El `index.html` es completamente estático — no requiere proceso Node/Python en producción.

---

## 4. Causa raíz — SyntaxError JS (Bug crítico)

**Defecto:** El bloque `JS = """..."""` en `build.py` es un Python triple-quoted string. Dentro de `renderProjectsModal()`, se generaban onclicks con IDs de proyecto:

```python
# Python source BUGGY
+ ' onclick="deleteProject(\'' + p.id + '\');...>'
```

Python interpreta `\'` como secuencia de escape → emite `'` en el output → el JS generado contiene `''` (comillas adyacentes) → `SyntaxError: Unexpected string` en línea 151 del script embebido → **ninguna función JS se registra** → todos los botones del sitio dejan de funcionar.

**Fix:** `\'` → `\\'` en las 5 líneas afectadas dentro de `renderProjectsModal()`.

```python
# Python source CORREGIDO
+ ' onclick="deleteProject(\\'' + p.id + '\\');...>'
```

---

## 5. Solución implementada

### 5.1 Arquitectura del feature Proyectos

```
localStorage
  AI_SDLC_v1_projects: [{ id, name, isDefault, vars: {7 campos} }]
  AI_SDLC_v1_active:   "proj_xxxxxxx"
        │
        ▼
  getActiveProject()  ←──  getVarValues()  ←──  applyVars()  ←──  copyPrompt()
        │
        ▼
  syncPanelToProject()  ──→  Panel DOM (7 inputs/selects)
        ↑
  syncProjectFromPanel()  ←──  oninput de cada campo
```

### 5.2 Componentes modificados en `build.py`

| Componente | Cambio | Tipo |
|---|---|---|
| `CSS` block | +100 líneas: `.proj-selector-row`, `.proj-select`, `.proj-mgr-btn`, `#proj-modal`, `.proj-*` | Nuevo |
| `JS` block — antes de `VAR_MAP` | 16 funciones nuevas: `genId`, `loadProjects`, `saveProjects`, `getActiveProject`, `createProject`, `deleteProject`, `duplicateProject`, `setDefaultProject`, `switchProject`, `syncPanelToProject`, `syncProjectFromPanel`, `renderProjectSelector`, `renderProjectsModal`, `renameProject`, `openProjectsModal`, `closeProjectsModal` | Nuevo |
| `getVarValues()` línea ~637 | Lee de `getActiveProject().vars` en lugar del DOM | Modificado |
| `clearVars()` línea ~691 | Limpia `project.vars` y llama `syncPanelToProject()` | Modificado |
| `DOMContentLoaded` handler | Inicializa proyecto Default + `renderProjectSelector()` + `syncPanelToProject()` | Extendido |
| `build()` HTML var-panel | Añade `<div class="proj-selector-row">` con `<select id="proj-selector">` y botón ⚙ | Nuevo |
| `build()` HTML var-panel — 7 campos | `oninput` cambia de `updateVarsBadge()` a `syncProjectFromPanel();updateVarsBadge();` | Modificado |
| `build()` HTML antes de `<script>` | Añade `<div id="proj-modal">` con lista y botón "+ Nuevo proyecto" | Nuevo |
| `renderProjectsModal()` — fix | `\'` → `\\'` en 5 líneas de onclick/onblur | Corregido |

### 5.3 Arquitectura de despliegue GCP

```
Desarrollador (local)
    │
    │  python build.py         → index.html (168 KB)
    │  bash deploy-to-gcp.sh
    │
    ▼  SCP :2288
GCP 34.51.112.6
    /var/www/prompts/index.html
        │
        ▼
    Nginx v1.22.1
    /etc/nginx/sites-enabled/prompts.lionsystems.com.mx
        │ SSL: Let's Encrypt (certbot)
        │ TLS 1.2/1.3
        ▼
    https://prompts.lionsystems.com.mx
```

---

## 6. Pruebas ejecutadas

| ID | Prueba | Resultado | Evidencia |
|---|---|---|---|
| P-01 | `python build.py` sin errores | ✅ | `OK → index.html, 155.4 KB` |
| P-02 | JS sin errores de sintaxis | ✅ | `node --check → JS OK` |
| P-03 | `python verify_clean.py` | ✅ | `0 contaminados, 31 info buttons` |
| P-04 | HTTP 301 → HTTPS redirect | ✅ | `curl -I http://prompts... → 301` |
| P-05 | HTTPS 200 + tamaño correcto | ✅ | `HTTPS:200 Size:168541 TLS:0` |
| P-06 | Headers de seguridad | ✅ | `X-Frame-Options: SAMEORIGIN, X-Content-Type-Options: nosniff` |
| P-07 | Certbot dry-run | ✅ | Renovación automática configurada |
| P-08 | Validación externa (Invoke-WebRequest) | ✅ | `HTTP: 200, 168541 bytes` |

---

## 7. Riesgos

| Riesgo | Prob. | Impacto | Estado |
|---|---|---|---|
| `localStorage` bloqueado (modo privado Safari) | Baja | Medio | Aceptado — falla silenciosa, panel vacío |
| Disco GCP al 77% | Media | Bajo | Monitorear — logs rotan 3 días |
| `index.html` GCP desactualizado si se olvida `deploy-to-gcp.sh` | Media | Medio | Mitigado con script documentado |
| Cert expira 2026-07-10 | N/A | Alto | Mitigado — Certbot cron activo |
| Colisión de IDs de proyecto (`genId` = 7 chars random) | Muy baja | Bajo | Aceptado |

---

## 8. Resultados

| Métrica | Antes | Después |
|---|---|---|
| Variables persistentes en reload | ❌ | ✅ `localStorage` |
| Multi-proyecto | ❌ | ✅ N proyectos con vars independientes |
| URL de producción propia | ❌ | ✅ `https://prompts.lionsystems.com.mx` |
| TLS / HTTPS | ❌ | ✅ Let's Encrypt, auto-renew |
| Script de re-deploy documentado | ❌ | ✅ `deploy-to-gcp.sh` |
| Nginx config en repo | ❌ | ✅ `nginx_prompts.conf` |
| `index.html` tamaño | 145 KB | 168 KB (+23 KB) |
| JS sin SyntaxError | ❌ (bug crítico) | ✅ `node --check` OK |

---

## 9. Puntos pendientes

| ID | Pendiente | Prioridad |
|---|---|---|
| PP-01 | Pruebas manuales funcionales en navegador (T-01 a T-10 del checklist) | Alta |
| PP-02 | CI/CD automático a GCP (actualmente manual con `deploy-to-gcp.sh`) | Media |
| PP-03 | Monitorear disco GCP — alertar si supera 85% | Media |
| PP-04 | `safari-private` fallback para `localStorage` bloqueado | Baja |
| PP-05 | Tests unitarios automatizados para funciones JS de proyectos | Baja |

---

## 10. Trazabilidad de commits

| Commit | Descripción |
|---|---|
| `513891d` | feat: initial commit — AI-SDLC Pro + GitHub Pages CI/CD |
| `ac074bb` | feat(ux): project quick-switcher + sidebar collapsible + responsive design |
| `2d84005` | feat(framework): bloque 00-B scaffolding repo y 00-C gobernanza multi-agente |
| `568a40b` | ops(gcp): deploy prompts.lionsystems.com.mx to GCP production |

---

*Firmado: Agente Copilot / AI-SDLC Enterprise — 2026-04-10*
