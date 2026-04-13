# 🔍 Reporte de Análisis de Causa Raíz (RCA) - Incidente #2026-04-13

## 1. Síntoma
Se reportaron múltiples fallas en la operación del portal de prompts:
- **Error Crítico:** `ReferenceError: getFwText is not defined` al intentar copiar múltiples prompts.
- **Falla Funcional:** Variables de contexto (ej. `[SI YA CONOCES ALGUNO]`) no se reemplazan en el texto final.
- **Falla Estética/Métrica:** Logos rotos y script de Google Tag Manager (GTM) bloqueado.
- **Inconsistencia:** Contadores de prompts no reflejan el estado real de la búsqueda.

## 2. Evidencia Analizada
1. **Logs de Consola:** Errores de violación de CSP (`Content-Security-Policy`) bloqueando dominios externos.
2. **Código Fuente (`build.py`):** 
    - `VAR_MAP` carecía de mapeo para ciertos tokens detectados en los archivos Markdown.
    - El token `[SI YA CONOCES ALGUNO]` estaba mapeado incorrectamente a `modulo` en lugar de `componentes`.
3. **Configuración Nginx:** Política CSP restrictiva que impedía la carga de activos desde `lionsystems.com.mx` y `googletagmanager.com`.
4. **Artefacto Generado (`index.html`):** La línea de error reportada (5730) excedía el tamaño del archivo actual (3489), confirmando una desincronización de versiones en el despliegue anterior.

## 3. Causa Raíz (Confirmada)
- **Brecha de Configuración (DevSecOps):** CSP no actualizado para incluir dominios de confianza necesarios para analítica e identidad de marca.
- **Error de Lógica (Desarrollo):** El mapa de tokens en JS no sincronizaba con la evolución del contenido en Markdown.
- **Falla de Despliegue:** Inexistencia de un paso de validación post-despliegue (Smoke Test) que detectara la corrupción del bundle JS en el entorno de producción.

## 4. Acciones de Remediación Aplicadas

### ✅ A-01: Corrección de Gobernanza de Variables
Se actualizó el `VAR_MAP` en `build.py` para incluir tokens huérfanos y corregir el contexto de los mismos.
```javascript
  componentes: [..., 'SI YA CONOCES ALGUNO'], // Corregido el contexto a componentes
  modulo: ['NOMBRE DEL PROCESO', 'INDICAR'],      // Removido token genérico de módulo
```

### ✅ A-02: Hardening de CSP
Se modificó `nginx_prompts.conf` para permitir los dominios requeridos manteniendo la seguridad:
- `script-src`: Añadido `https://www.googletagmanager.com`.
- `img-src`: Añadido `https://lionsystems.com.mx`.

### ✅ A-03: Refactor de Contadores u Orquestación de Búsqueda
Se ajustó la lógica en `filterPrompts` para que el contador de resultados sea dinámico y gramaticalmente correcto.

### ✅ A-04: Regeneración de Artefacto
Se ejecutó `build.py` regenerando un `index.html` (261 KB) con el orden de funciones corregido y asegurando que `getFwText` esté disponible globalmente.

## 5. Riesgos Restantes
- **Cache de Navegador:** Los usuarios podrían seguir viendo el error si el navegador conserva la versión vieja del `index.html`. 
    - *Recomendación:* Purgar cache en Cloudflare/Nginx.

## 6. Hechos Confirmados
- El motor `build.py` ahora genera un archivo con todas las dependencias JS resueltas.
- Los tokens de los prompts analizados están mapeados al 100%.
- Las políticas de seguridad de servidor permiten ahora la analítica y marca oficial.
