# 📄 Análisis y Diseño - AI-SDLC Pro

## 1. Visión General
**AI-SDLC Pro** es una biblioteca interactiva de prompts diseñada para estandarizar la dirección de agentes IA durante el Ciclo de Vida de Desarrollo de Software (SDLC). El proyecto resuelve la inconsistencia en los resultados de la IA mediante un framework de contexto multi-agente y un sistema de variables dinámicas.

## 2. Requerimientos Funcionales
- **RF-01: Framework Auto-Prepend:** El sistema debe garantizar que el bloque de contexto base (00-framework) se anteponga o se entregue como paso obligatorio antes de usar cualquier prompt específico.
- **RF-02: Gestión de Proyectos:** Los usuarios deben poder definir múltiples perfiles de proyecto (Repositorio, Stack, Metodología, Agentes) almacenados localmente.
- **RF-03: Sustitución de Variables:** Los prompts en Markdown usan marcadores `{{VARIABLE}}` que el motor de la página debe sustituir en tiempo real antes de copiar al portapapeles.
- **RF-04: Selección Múltiple (Multi-Select):** Capacidad de seleccionar varios prompts y copiarlos como un único bloque estructurado.
- **RF-05: Generación Estática:** La solución debe compilarse en un único archivo `index.html` autogestionado para facilitar el despliegue.

## 3. Diseño de la Solución
### 3.1 Arquitectura del Compilador (build.py)
El compilador actúa como un generador de sitios estáticos (SSG) simplificado:
1. **Source Discovery:** Escanea el directorio `ai_sdlc_pro_prompts/`.
2. **Markdown Parsing:** Segmenta el contenido en:
   - **Prompt:** El texto puro para la IA.
   - **Instrucción:** Metadata sobre cuándo y cómo usar el prompt.
   - **Variables:** Identificación de placeholders para la UI.
3. **Template Injection:** Inyecta la metadata en una estructura de datos JSON dentro del JS del sitio.
4. **Bundle Generation:** Consolida CSS, JS y el contenido en un `index.html` final.

### 3.2 Diseño de Interacción (UX)
- **Panel de Variables:** Sidebar derecho para la entrada de datos persistente via `localStorage`.
- **Modo Proyecto:** Selector rápido en la barra de búsqueda para cambiar el contexto global de las variables.
- **Modal Informativo (ⓘ):** Desglose de "Fórmulas de uso" para que el humano sepa qué comandos enviar a la IA (ej. "Usa el prompt de análisis del issue X").

## 4. Casos de Uso
1. **Estandarización de Equipo:** Un Tech Lead define el proyecto en el Panel de Variables y comparte los valores con el equipo para que todos usen los mismos prompts con el mismo contexto.
2. **Flujo Multi-Agente:** El desarrollador usa el prompt `00-C-01` para configurar GitHub Copilot y luego `00-C-02` para Claude, asegurando que ambos agentes entiendan sus roles respectivos en el repositorio.
3. **Auditoría de Calidad:** Uso de los prompts de la sección `08` para que la IA revise el código contra los estándares del proyecto antes de un PR.
