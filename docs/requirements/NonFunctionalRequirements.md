# Requerimientos No Funcionales
## AI-SDLC Pro — Atributos de Calidad y Restricciones

---

**Fecha:** 2026-04-12  
**Versión:** 1.0  
**Estándar:** ISO/IEC 25010 (SQuaRE) / RUP Supplementary Specifications  
**Categorías:** Performance, Security, Reliability, Usability, Maintainability, Portability

---

## 1. Requerimientos de Performance (Eficiencia)

### 1.1 Tiempo de Comportamiento

| ID | Requerimiento | Métrica | Prioridad | Estado |
|----|---------------|---------|-----------|--------|
| **NFR-PER-01** | Tiempo de carga inicial < 3 segundos en conexión 4G | TTI < 3s | Must | ✅ |
| **NFR-PER-02** | First Contentful Paint < 1.5 segundos | FCP < 1.5s | Should | ✅ |
| **NFR-PER-03** | Largest Contentful Paint < 2.5 segundos | LCP < 2.5s | Should | 🟡 |
| **NFR-PER-04** | Interacción con botón copiar < 100ms | TBT < 100ms | Must | ✅ |
| **NFR-PER-05** | Búsqueda en tiempo real con debounce 150ms | - | Should | ✅ |
| **NFR-PER-06** | Cambio de idioma < 300ms (sin recarga) | - | Should | ✅ |
| **NFR-PER-07** | Scroll fluido 60fps | - | Should | ✅ |

### 1.2 Utilización de Recursos

| ID | Requerimiento | Métrica | Prioridad | Estado |
|----|---------------|---------|-----------|--------|
| **NFR-PER-08** | Tamaño de `index.html` < 1MB (con i18n dual) | < 1,024 KB | Should | 🟡 |
| **NFR-PER-09** | Uso de memoria RAM < 100MB en desktop | < 100MB | Should | ✅ |
| **NFR-PER-10** | Sin leaks de memoria en uso prolongado (1h+) | 0 leaks | Should | 🟡 |
| **NFR-PER-11** | localStorage < 5MB por usuario | < 5MB | Must | ✅ |

---

## 2. Requerimientos de Seguridad (Confidencialidad, Integridad)

### 2.1 Confidencialidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-SEC-01** | Datos de proyecto almacenados localmente (no servidor) | Must | ✅ |
| **NFR-SEC-02** | Sin transmisión de datos de proyecto a terceros | Must | ✅ |
| **NFR-SEC-03** | Analytics solo eventos agregados (no contenido de prompts) | Must | ✅ |
| **NFR-SEC-04** | No almacenar credenciales, tokens, o secrets en variables | Must | ✅ |

### 2.2 Integridad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-SEC-05** | QA gate debe validar prompts antes de deploy | Must | ✅ |
| **NFR-SEC-06** | Build determinístico: mismo input → mismo output | Should | ✅ |
| **NFR-SEC-07** | Protección contra XSS: escaping de HTML en contenido Markdown | Must | ✅ |

### 2.3 Disponibilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-SEC-08** | 99.9% uptime en GitHub Pages | Must | ✅ |
| **NFR-SEC-09** | Dual deploy: failover de GCP si GitHub Pages cae | Should | 🟡 |

---

## 3. Requerimientos de Confiabilidad (Reliability)

### 3.1 Madurez

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-REL-01** | Copia a clipboard debe funcionar en 100% de intentos | Must | ✅ |
| **NFR-REL-02** | Degradación graceful si `navigator.clipboard` no disponible | Should | 🔶 |
| **NFR-REL-03** | Funcionamiento básico si JavaScript deshabilitado (solo ver prompts) | Won't | ❌ |

### 3.2 Tolerancia a Fallos

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-REL-04** | Si localStorage lleno, mostrar error amigable al usuario | Should | 🟡 |
| **NFR-REL-05** | Si analytics falla, no bloquear funcionalidad core | Must | ✅ |
| **NFR-REL-06** | Recuperación de localStorage corrupto (reset a default) | Should | 🟡 |

### 3.3 Recuperabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-REL-07** | Export/Import de proyectos para backup manual | Could | ✅ |
| **NFR-REL-08** | Auto-backup no requerido (client-side only) | Won't | ❌ |

---

## 4. Requerimientos de Usabilidad (Usability)

### 4.1 Comprensibilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-USE-01** | Onboarding tutorial para nuevos usuarios | Must | ✅ |
| **NFR-USE-02** | Tooltips explicativos en botones principales | Should | ✅ |
| **NFR-USE-03** | Documentación de uso embebida en cada prompt (fórmula) | Must | ✅ |
| **NFR-USE-04** | Glosario de términos técnicos disponible | Could | 🔶 |

### 4.2 Aprendibilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-USE-05** | Time to first copy < 2 minutos para nuevo usuario | Should | 🟡 |
| **NFR-USE-06** | Consistencia de UI (mismo patrón en todas las cards) | Must | ✅ |
| **NFR-USE-07** | Feedback visual inmediato en todas las acciones | Must | ✅ |

### 4.3 Operabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-USE-08** | Atajos de teclado: Escape (cerrar modales), Ctrl+F (buscar) | Should | ✅ |
| **NFR-USE-09** | Navegación por teclado accesible (Tab, Enter, Space) | Should | 🟡 |
| **NFR-USE-10** | Persistencia de preferencias de UI (sidebar, framework) | Should | ✅ |

### 4.4 Atractivo

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-USE-11** | Diseño oscuro (dark mode) profesional, coherente | Must | ✅ |
| **NFR-USE-12** | Animaciones sutiles (transiciones < 300ms) | Should | ✅ |
| **NFR-USE-13** | Iconografía consistente (lucide/similar) | Should | ✅ |

---

## 5. Requerimientos de Mantenibilidad (Maintainability)

### 5.1 Modularidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-MAN-01** | Generador `build.py` desacoplado de presentación | Must | ✅ |
| **NFR-MAN-02** | Prompts individuales en archivos `.md` separados | Must | ✅ |
| **NFR-MAN-03** | CSS/JS inline en output (no dependencias externas) | Must | ✅ |
| **NFR-MAN-04** | i18n strings centralizados en módulo separado | Should | ✅ |

### 5.2 Reusabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-MAN-05** | Componente card de prompt reusable para todos los 44 prompts | Must | ✅ |
| **NFR-MAN-06** | Funciones de copia/variables reutilizables | Must | ✅ |

### 5.3 Analizabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-MAN-07** | Logging de errores en consola (no silenciar excepciones) | Should | ✅ |
| **NFR-MAN-08** | QA gate con mensajes claros de fallo | Must | ✅ |
| **NFR-MAN-09** | Scripts de utilidad: `extract_vars.py`, `verify_clean.py` | Should | ✅ |

### 5.4 Capacidad de Modificación

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-MAN-10** | Agregar nuevo prompt: solo crear `.md`, rebuild, deploy | Must | ✅ |
| **NFR-MAN-11** | Agregar idioma: extensión de diccionarios, no refactor | Should | 🟡 |
| **NFR-MAN-12** | Cambiar tema visual: modificación CSS centralizada | Should | ✅ |

### 5.5 Capacidad de Prueba

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-MAN-13** | QA gate automatizado en CI/CD | Must | ✅ |
| **NFR-MAN-14** | Tests de integración para copiado y persistencia | Could | 🔶 |
| **NFR-MAN-15** | Scripts de prueba local (`python build.py && verify_clean.py`) | Should | ✅ |

---

## 6. Requerimientos de Portabilidad (Portability)

### 6.1 Adaptabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-POR-01** | Funcionamiento en Chrome, Firefox, Safari, Edge (últimas 2 versiones) | Must | ✅ |
| **NFR-POR-02** | Responsive: mobile (320px), tablet (768px), desktop (1920px) | Must | ✅ |
| **NFR-POR-03** | PWA-ready: service worker básico para offline (future) | Could | ❌ |

### 6.2 Instalabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-POR-04** | No instalación requerida (web app) | Must | ✅ |
| **NFR-POR-05** | Opción "Add to Home Screen" (PWA manifest) | Could | 🔶 |

### 6.3 Reemplazabilidad

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-POR-06** | Migración de localStorage schema v1 → v2 si es necesario | Could | 🔶 |

---

## 7. Requerimientos de Compatibilidad (Compatibility)

| ID | Requerimiento | Prioridad | Estado |
|----|---------------|-----------|--------|
| **NFR-COM-01** | No dependencias de CDN (fonts, librerías externas) | Must | ✅ |
| **NFR-COM-02** | GitHub Pages 100% compatible (no server-side) | Must | ✅ |
| **NFR-COM-03** | Copiado funciona en HTTP y HTTPS | Must | ✅ |

---

## 8. Restricciones de Diseño

| ID | Restricción | Justificación |
|----|-------------|---------------|
| **RES-01** | Single HTML file output | GitHub Pages optimization, offline capability |
| **RES-02** | No backend database | Costo, complejidad, privacidad |
| **RES-03** | Python 3.8+ para build | Compatibilidad con sistemas CI/CD |
| **RES-04** | Vanilla JavaScript (no React/Vue/Angular) | Performance, tamaño, zero dependencies |
| **RES-05** | UTF-8 encoding obligatorio | i18n ES/EN + caracteres especiales |

---

## 9. Estándares de Cumplimiento

| Estándar | Aplicación | Cumplimiento |
|----------|-----------|--------------|
| **Conventional Commits** | Mensajes de commit | ✅ |
| **IEEE 830-1998** | Especificación de requerimientos | ✅ |
| **ISO/IEC 25010** | Calidad de producto software | 🟡 |
| **WCAG 2.1 AA** | Accesibilidad web | 🟡 |
| **PSP v3.0** | Proceso personal de software | ✅ |

---

## 10. Matriz de Priorización

### Cuadrante de Importancia vs Urgencia

```
                    URGENCIA
              Alta           Baja
         ┌─────────────┬─────────────┐
    Alta │ NFR-PER-01  │ NFR-MAN-10  │
         │ NFR-SEC-01  │ NFR-USE-11  │
         │ NFR-USE-01  │             │
IMP      ├─────────────┼─────────────┤
         │ NFR-COM-01  │ NFR-POR-03  │
    Baja │ NFR-REL-07  │ NFR-USE-04  │
         │             │             │
         └─────────────┴─────────────┘
```

---

## 11. Métricas de Calidad (PSP)

| Atributo | Métrica | Objetivo | Actual |
|----------|---------|----------|--------|
| **Defect Density** | Defectos / KLOC | < 5 | N/A (no contado) |
| **Cyclomatic Complexity** | McCabe index | < 15 por función | ~10 (estimado) |
| **Test Coverage** | % requerimientos probados | > 80% | Manual testing |
| **Build Time** | Segundos | < 5s | ~2s |
| **Page Load** | TTI | < 3s | ~2.5s |

---

## 12. Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-12 | Asistente IA | Documento inicial, 48 NFR + 5 restricciones |

---

**Trázabilidad PSP:**
- **Total NFR:** 48 requerimientos no funcionales
- **Atributos ISO 25010 cubiertos:** 6 de 8 (faltan Safety, Security incompleto)
- **Tiempo estimado documentación:** 3 horas
- **Revisión:** Pendiente validación de métricas reales vs objetivos

