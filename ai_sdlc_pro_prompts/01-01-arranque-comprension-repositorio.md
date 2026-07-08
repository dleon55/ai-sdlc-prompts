# 1.1 — Inventario técnico del repositorio

## Descripción

Prompt de arranque para construir un inventario técnico inicial del repositorio: estructura, workspaces/sub-módulos, tecnologías detectadas, artefactos del ciclo de ingeniería y vacíos relevantes. Es el primer paso recomendado antes de cualquier análisis o implementación sobre un repositorio nuevo o desconocido.

**Cuándo usarlo:** al arrancar trabajo sobre un repositorio del que no se tiene contexto previo, o para refrescar el inventario después de cambios estructurales significativos.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Quiero que analices integralmente este repositorio y construyas un inventario técnico inicial del proyecto.

Actividades:
1. Revisa la estructura completa del repositorio (detectando si es un monorrepositorio o proyecto modular).
2. Identifica:
   - workspaces / subproyectos / sub-módulos,
   - dependencias y fronteras entre paquetes internos,
   - componentes,
   - módulos,
   - capas,
   - servicios,
   - librerías internas,
   - scripts,
   - pipelines,
   - pruebas,
   - documentación,
   - archivos de configuración,
   - contenedores,
   - migraciones,
   - variables de entorno.
3. Detecta tecnologías utilizadas:
   - frontend,
   - backend,
   - base de datos,
   - infraestructura,
   - mensajería,
   - autenticación,
   - observabilidad.
4. Ubica los artefactos del ciclo de ingeniería y alineación con estándares (PSP, ISO, etc.):
   - análisis,
   - diseño,
   - casos de uso,
   - diagramas,
   - implementación,
   - pruebas,
   - CI/CD,
   - documentación.
5. Detecta vacíos o ausencias relevantes.

Formato de salida:
1. Resumen ejecutivo
2. Inventario de carpetas y propósito
3. Arquitectura detectada
4. Tecnologías y versiones encontradas
5. Procesos/documentación localizados
6. Riesgos o vacíos
7. Recomendación de orden de revisión
```

---

## Uso con fórmula estándar

```text
Usa el prompt de inventario técnico del repositorio y adáptalo a:
- repositorio: [NOMBRE O URL]
- rama: [RAMA PRINCIPAL]
- documentos a revisar: código fuente completo, configuración, documentación existente
- objetivo puntual de salida: inventario técnico inicial con riesgos y vacíos detectados
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Resumen ejecutivo | Panorama general del repositorio en pocas líneas |
| Inventario de carpetas | Estructura y propósito de cada carpeta principal |
| Arquitectura detectada | Monorepo/modular, capas, componentes y servicios identificados |
| Tecnologías | Stack de frontend, backend, BD, infraestructura, mensajería, auth, observabilidad |
| Procesos/documentación | Artefactos del ciclo de ingeniería ya presentes |
| Riesgos o vacíos | Ausencias relevantes detectadas |
| Orden de revisión | Recomendación de por dónde continuar el análisis |
