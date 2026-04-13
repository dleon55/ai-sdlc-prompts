# Documentación de Requerimientos
## AI-SDLC Pro — Especificación de Requerimientos del Sistema

---

**Estándar:** RUP (Rational Unified Process) + PSP (Personal Software Process)  
**Metodología:** Use-Case Driven Development  
**Fecha de Creación:** 2026-04-12  
**Versión:** 1.0

---

## 📋 Estructura de Documentación

Esta carpeta contiene la especificación completa de requerimientos del sistema AI-SDLC Pro, organizada según estándares de ingeniería de software.

### Documentos Principales

| Documento | Descripción | Estándar | Tamaño Est. |
|-----------|-------------|----------|-------------|
| **[Vision.md](Vision.md)** | Documento de visión del producto, stakeholders, alcance | RUP Vision | 140 líneas |
| **[BusinessRules.md](BusinessRules.md)** | 64 reglas de negocio organizadas por dominio | RUP Business Model | 300 líneas |
| **[UseCases.md](UseCases.md)** | 21 casos de uso detallados con diagramas UML | UML 2.5 / RUP | 400 líneas |
| **[FunctionalRequirements.md](FunctionalRequirements.md)** | 54 requerimientos funcionales (MoSCoW) | IEEE 830-1998 | 350 líneas |
| **[NonFunctionalRequirements.md](NonFunctionalRequirements.md)** | 48 atributos de calidad + restricciones | ISO/IEC 25010 | 300 líneas |

---

## 🎯 Resumen Ejecutivo

### Cobertura de Requerimientos

```
Total Especificación:
├── Funcionales (FR):     54 requerimientos
├── No Funcionales (NFR): 48 requerimientos
├── Reglas de Negocio:    64 reglas
├── Casos de Uso:         21 casos
└── Documento de Visión:  1 documento estratégico

Estado de Implementación:
✅ Implementados:    ~75% (42 FR, 36 NFR)
🔶 Parciales:       ~15% (8 FR, 8 NFR)
❌ Pendientes:      ~10% (4 FR, 4 NFR - monetización)
```

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTACIÓN                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Landing   │  │   App SPA   │  │   Modales   │     │
│  │   (HTML)    │  │  (JS/CSS)   │  │ (UI/UX)     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                    LÓGICA DE NEGOCIO                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Prompts   │  │  Proyectos  │  │    i18n     │     │
│  │  (44 items) │  │ (12 vars)   │  │  (ES/EN)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                   PERSISTENCIA                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ localStorage│  │   Export    │  │   Import    │     │
│  │  (cliente)  │  │   (JSON)    │  │   (JSON)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                   GENERACIÓN                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  build.py   │  │ verify_clean│  │   i18n_     │     │
│  │  (Python)   │  │    .py      │  │  strings.py │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 📖 Guía de Uso

### Para Desarrolladores

1. **Entender el alcance:** Leer [Vision.md](Vision.md) Sección 1-2
2. **Implementar feature:** Consultar [UseCases.md](UseCases.md) para flujos
3. **Validar calidad:** Verificar contra [NonFunctionalRequirements.md](NonFunctionalRequirements.md)
4. **Completar:** Asegurar trazabilidad en [FunctionalRequirements.md](FunctionalRequirements.md)

### Para QA/Testers

1. **Plan de pruebas:** Basarse en casos de uso en [UseCases.md](UseCases.md)
2. **Criterios de aceptación:** Usar métricas en [NonFunctionalRequirements.md](NonFunctionalRequirements.md)
3. **Validación de negocio:** Verificar [BusinessRules.md](BusinessRules.md)

### Para Product Owners

1. **Roadmap:** Priorizar usando [Vision.md](Vision.md) Sección 7 (Roadmap)
2. **Decisiones:** Consultar [BusinessRules.md](BusinessRules.md) para restricciones
3. **Stakeholders:** Revisar [Vision.md](Vision.md) Sección 3 (Personas)

---

## 🔗 Trazabilidad

### Matriz de Trazabilidad Requerimientos ↔ Código

| Requerimiento | Archivo Código | Función/Clase | Estado |
|---------------|---------------|---------------|--------|
| FR-COPY-01 | build.py | `copyPrompt()` | ✅ |
| FR-PRJ-01 | JS inline | `createProject()` | ✅ |
| FR-I18N-01 | build.py | `initLanguageDetection()` | ✅ |
| FR-MON-01 | build.py | (pendiente) | 🔶 |

### Convención de IDs

| Prefijo | Significado | Ejemplo |
|---------|-------------|---------|
| `FR-` | Functional Requirement | FR-COPY-01 |
| `NFR-` | Non-Functional Requirement | NFR-PER-01 |
| `BR-` | Business Rule | BR-01 |
| `UC-` | Use Case | UC-07 |

---

## 📊 Métricas PSP (Personal Software Process)

| Métrica | Valor | Notas |
|---------|-------|-------|
| **Tiempo estimado documentación** | 16 horas | 4 docs × 4h promedio |
| **Tamaño total** | ~1,500 líneas | Markdown |
| **Defectos inyectados** | 0 | Primera versión |
| **Defectos removidos** | 0 | No revisión formal aún |
| **Reusabilidad** | Alta | Plantilla para otros proyectos |
| **Tiempo de consulta** | < 5 min | Índice y enlaces directos |

---

## 🎓 Referencias y Estándares

### Estándares Aplicados

1. **RUP (Rational Unified Process)**
   - Vision Document
   - Supplementary Specifications
   - Use-Case Specifications

2. **PSP (Personal Software Process) v3.0**
   - Size Estimation
   - Time Tracking
   - Defect Recording

3. **IEEE 830-1998**
   - Recommended Practice for Software Requirements Specifications

4. **ISO/IEC 25010:2011 (SQuaRE)**
   - System and Software Quality Models

5. **UML 2.5**
   - Use Case Diagrams
   - Activity Diagrams

### Herramientas Recomendadas

| Propósito | Herramienta | Uso |
|-----------|-------------|-----|
| Edición Markdown | VS Code + Markdown All in One | Documentación |
| Diagramas UML | PlantUML / draw.io | Casos de uso |
| Métricas PSP | Excel/Google Sheets | Tracking tiempo/defectos |
| Revisión | GitHub PR + Reviewers | Validación cambios |

---

## 🔄 Proceso de Mantenimiento

### Cuándo Actualizar

- ✅ Nuevo caso de uso implementado
- ✅ Cambio en reglas de negocio
- ✅ Nuevo idioma agregado (i18n)
- ✅ Feature de monetización implementada
- 🔶 Cambio en arquitectura técnica

### Versionado

Usar Semantic Versioning para documentos:
```
MAJOR.MINOR.PATCH
1.0.0  → Versión inicial
1.1.0  → Nuevos requerimientos agregados
1.1.1  → Correcciones menores
2.0.0  → Cambio mayor de arquitectura
```

---

## 📞 Contacto y Responsabilidades

| Rol | Responsabilidad | Documento Principal |
|-----|-----------------|---------------------|
| **Product Owner** | Priorización, alcance, visión | Vision.md |
| **Arquitecto** | Reglas técnicas, NFRs | NonFunctionalRequirements.md |
| **Desarrolladores** | Implementación, FRs | FunctionalRequirements.md |
| **QA** | Casos de prueba | UseCases.md |
| **Business Analyst** | Reglas de negocio | BusinessRules.md |

---

## ✅ Checklist de Calidad

- [x] Todos los documentos tienen versión y fecha
- [x] IDs únicos para requerimientos y casos de uso
- [x] Trazabilidad FR ↔ UC ↔ Código
- [x] Priorización MoSCoW aplicada
- [x] Métricas PSP estimadas
- [x] Glosario de términos incluido
- [x] Historial de cambios mantenido
- [ ] Revisión formal por stakeholders (pendiente)
- [ ] Aprobación escrita por PO (pendiente)

---

**Última actualización:** 2026-04-12  
**Próxima revisión programada:** 2026-05-12 (mensual)  
**Propietario:** LionSystems — dleon55

