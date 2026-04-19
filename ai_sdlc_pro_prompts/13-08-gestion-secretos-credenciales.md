# 13.8 — Gestión de Secretos y Credenciales

## Descripción

Prompt para auditar, clasificar y remediar la gestión de secretos en el código fuente, infraestructura, pipelines CI/CD y entornos de ejecución: detecta credenciales hardcoded, tokens expuestos, configuraciones inseguras y establece prácticas de gestión de secretos segura con rotación y almacenamiento centralizado.

**Cuándo usarlo:** como revisión preventiva antes de un PR, tras recibir alertas de escaneo de secretos (GitHub Secret Scanning, Gitleaks, truffleHog), al incorporarse al proyecto para auditar el estado histórico, o como parte de la revisión Secure SDLC (`13-03`).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Si existe resultado de `13-03` (Secure SDLC review), úsalo para identificar hallazgos previos de gestión de secretos.

---

## Prompt completo

```text
Objetivo:
Auditar, clasificar y remediar la gestión de secretos y credenciales en el código fuente,
historial de Git, infraestructura, pipelines CI/CD y entornos de ejecución;
establecer prácticas seguras de almacenamiento, acceso, rotación y auditoría de secretos.

Pasos:

1. INVENTARIO Y DETECCIÓN DE SECRETOS EXPUESTOS
   Analizar las siguientes superficies de exposición:
   
   a) Código fuente actual:
      - credenciales hardcoded: contraseñas, API keys, tokens, claves privadas
      - cadenas de conexión con credenciales embebidas (DSN, JDBC, MongoDB URI)
      - claves de cifrado o salts fijos en el código
      - certificados o claves privadas (.pem, .key, .pfx) commiteados
      - payloads de prueba con datos reales o secretos reales
   
   b) Historial de Git (commits anteriores):
      - secretos que fueron removidos del código pero permanecen en la historia
      - commits de "remove secret" o "fix credentials" (indicadores de exposición pasada)
      - ramas o tags con secretos que ya no están en main
      ⚠️ Los secretos en historial de Git deben considerarse comprometidos hasta rotar
   
   c) Archivos de configuración:
      - `.env`, `.env.local`, `.env.production` commiteados al repositorio
      - `config.yml`, `settings.json`, `application.properties` con valores reales
      - archivos de Terraform, Ansible, Helm con secretos interpolados directamente
      - `docker-compose.yml` con variables de entorno hardcoded
   
   d) CI/CD y automatización:
      - secretos embebidos en archivos de workflow (GitHub Actions, GitLab CI, Jenkins)
      - variables de entorno visibles en logs de CI/CD
      - scripts de despliegue con credenciales inline
   
   e) Dependencias y paquetes:
      - paquetes npm/pip/composer que incluyen claves en su configuración por defecto
      - archivos `package.json`, `composer.json` con tokens de registro privado

2. CLASIFICACIÓN Y CRITICIDAD
   Para cada secreto encontrado, clasificar:
   
   Tipo de secreto:
   - Credencial de base de datos (crítico — acceso a datos)
   - API key de servicio externo (alto — depende del servicio)
   - Token OAuth / JWT secret (alto — puede suplantar usuarios)
   - Clave privada SSH / TLS (crítico — acceso a infraestructura)
   - Clave de cifrado simétrico (crítico — datos descifrados)
   - Webhook secret (medio — depende del alcance)
   - Clave de servicio cloud (crítico — acceso a infraestructura completa)
   
   Estado:
   - ACTIVO: el secreto sigue siendo válido y en uso → rotar inmediatamente
   - EXPIRADO: ya no es válido → documentar y suprimir alerta
   - REVOCADO: fue invalidado tras detección → verificar que rotación sea completa
   - DESCONOCIDO: no se puede determinar validez → asumir activo, rotar

3. EVALUACIÓN DE PRÁCTICAS DE GESTIÓN ACTUALES
   Auditar la infraestructura de gestión de secretos existente:
   
   a) Almacenamiento:
      - ¿se usa un gestor de secretos centralizado? (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, Doppler)
      - ¿los secretos de entorno se inyectan en runtime o están en archivos?
      - ¿los archivos `.env` están en `.gitignore` correctamente?
   
   b) Acceso y control:
      - ¿quién tiene acceso a los secretos de producción?
      - ¿se aplica principio de mínimo privilegio? (cada servicio solo accede a sus secretos)
      - ¿existe auditoría de accesos a secretos?
      - ¿las API keys tienen scope reducido al mínimo necesario?
   
   c) Rotación:
      - ¿existe política de rotación de credenciales? (periodicidad por tipo)
      - ¿la rotación es automatizada o manual?
      - ¿los secretos tienen fecha de expiración configurada?
   
   d) CI/CD:
      - ¿se usan variables de entorno cifradas del proveedor? (GitHub Secrets, GitLab CI Variables, Jenkins Credentials)
      - ¿los logs de CI/CD enmascaran variables de entorno sensibles?
      - ¿los secretos se pasan entre jobs sin exposición innecesaria?

4. VERIFICACIÓN DE DETECCIÓN PREVENTIVA
   Evaluar si los controles preventivos están activos:
   - ¿existe hook pre-commit para detectar secretos? (gitleaks, detect-secrets, git-secrets)
   - ¿está activado GitHub Secret Scanning (si se usa GitHub)?
   - ¿hay escaneo de secretos en el pipeline CI/CD?
   - ¿las alertas de detección de secretos se revisan y cierran de forma sistemática?
   - ¿los desarrolladores saben cómo reportar una exposición accidental?

5. PLAN DE REMEDIACIÓN
   Para cada secreto activo encontrado:
   
   a) Acción inmediata (dentro de las primeras horas):
      - revocar / rotar el secreto en el proveedor del servicio
      - actualizar el secreto en el gestor de secretos o sistema destino
      - verificar que la aplicación funcione con el nuevo secreto
      - si el secreto estuvo expuesto → revisar logs de acceso del servicio afectado para detectar uso no autorizado
   
   b) Limpieza del repositorio:
      - si el secreto solo está en código actual: remover y hacer commit con mensaje claro
      - si el secreto está en historial de Git: usar `git filter-repo` para reescribir historia
        ⚠️ Esto requiere push forzado — coordinar con el equipo, todos deben re-clonar
      - agregar el secreto a `.gitignore` para prevenir re-commit accidental
   
   c) Mejoras estructurales:
      - migrar secretos a gestor centralizado si no existe
      - implementar inyección de secretos en runtime (variables de entorno desde Vault/AWS SSM)
      - instalar hook pre-commit en el repositorio
      - capacitar al equipo en prácticas de manejo de secretos

6. ESTÁNDARES Y MEJORES PRÁCTICAS
   Definir o verificar las políticas de secretos del proyecto:
   
   a) Nomenclatura y documentación:
      - inventario de todos los secretos con: nombre, servicio, owner, fecha de rotación, expiración
      - documentar qué secretos existen aunque no sus valores
   
   b) Política de rotación por tipo:
      - Credenciales de BD: cada 90 días o tras cualquier cambio de personal con acceso
      - API keys de servicios externos: según política del proveedor, mínimo cada 180 días
      - Claves SSH: cada 12 meses o al salir un miembro del equipo
      - Claves de cifrado: política de versioning; rotación implica re-cifrado de datos
      - Tokens de CI/CD: cada 90 días
   
   c) Respuesta ante exposición:
      - procedimiento: detectar → revocar → rotar → auditar logs → documentar
      - tiempo máximo de respuesta: 1 hora para críticos, 24 horas para altos

Herramientas recomendadas:
- Detección en código: gitleaks, truffleHog, detect-secrets, semgrep (reglas de secretos)
- Detección en CI/CD: GitHub Secret Scanning, GitLab Secret Detection, Snyk
- Gestión centralizada: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Doppler
- Limpieza de historial: git-filter-repo (reemplazo de git-filter-branch)
- Hooks pre-commit: pre-commit framework con gitleaks o detect-secrets

Entregables:
- inventario de secretos detectados con clasificación y estado (activo/expirado/revocado),
- plan de remediación priorizado por criticidad con SLA de rotación,
- evaluación del estado actual de prácticas de gestión de secretos (checklist),
- recomendaciones de arquitectura para gestión segura centralizada,
- checklist de controles preventivos a implementar.
```

---

## Fórmula estándar de uso

```text
Usa el prompt de gestión de secretos y adáptalo a:
- repositorio: [NOMBRE O URL]
- stack tecnológico: [lenguaje, framework, proveedor cloud]
- gestor de secretos actual: [ninguno / .env files / Vault / AWS Secrets Manager / otro]
- CI/CD usado: [GitHub Actions / GitLab CI / Jenkins / otro]
- proveedores de servicio con credenciales: [AWS / GCP / Stripe / SendGrid / etc.]
- profundidad del análisis de historial Git: [solo commits recientes / historial completo]
- documentos a revisar: .env.example, workflows de CI/CD, archivos de infraestructura (Terraform, Helm, docker-compose)
- objetivo de salida específico: inventario de secretos expuestos + plan de remediación + checklist de controles
- nivel de profundidad: alto
```

---

## Resultado esperado

### Inventario de secretos detectados

| ID | Tipo | Ubicación | Estado | Severidad | Acción requerida | SLA |
|---|---|---|---|---|---|---|
| SEC-001 | Credencial BD | `config/database.yml:12` | ACTIVO | CRÍTICO | Rotar + migrar a Vault | 1 hora |
| SEC-002 | API key Stripe | `git log —commit a3f2b1` (historial) | DESCONOCIDO | ALTO | Revocar en dashboard Stripe + limpiar historial | 2 horas |
| SEC-003 | AWS Access Key | `.github/workflows/deploy.yml:34` | ACTIVO | CRÍTICO | Revocar IAM, migrar a GitHub Secrets + OIDC | 1 hora |

### Evaluación de prácticas actuales

| Control | Estado | Recomendación |
|---|---|---|
| Gestor de secretos centralizado | ❌ No implementado | Implementar HashiCorp Vault o AWS Secrets Manager |
| Hook pre-commit de detección | ❌ No implementado | Instalar gitleaks como pre-commit hook |
| GitHub Secret Scanning | ⚠️ No verificado | Activar en configuración del repositorio |
| `.env` en `.gitignore` | ✅ Correcto | Verificar todos los entornos (.env.*) |
| Política de rotación documentada | ❌ No existe | Crear política y asignar owners por secreto |
