# Configuración del muro de registro + prueba Pro de 1 semana + feedback

Este feature se apoya en el registro de usuarios ya configurado (ver
[`docs/auth-setup.md`](auth-setup.md)) — si ese feature todavía muestra el
aviso de "no configurado", completa esos pasos primero.

El código está implementado en `build.py` (sección `MURO DE REGISTRO /
PRUEBA / FEEDBACK`), pero **queda inerte hasta ejecutar el SQL de este
archivo** en el proyecto de Supabase — igual que con `schema.sql`, ningún
paso de este documento puede hacerse desde este repositorio.

Mientras no se ejecute `supabase/trial_gate.sql`, cada llamada a las
funciones nuevas falla (no existen todavía) y el diseño está pensado para
ese caso: **fail-open** — cualquier error de red o de función faltante
permite la acción en vez de bloquearla.

## Rediseño (issue #7, Opción B) — qué cambió y por qué

El repositorio de este proyecto es **público**: el texto completo de los
115 prompts ya es legible por cualquiera en GitHub o vía el servidor MCP,
sin autenticación. Gatear la **copia** de prompts (el diseño original de
este muro, "10 copias anónimas") solo agregaba fricción sin proteger nada
real — cualquier usuario técnico podía evadirlo leyendo el repo.

El muro ahora gatea la **plataforma**, no el texto:
- **Copiar cualquier prompt es siempre gratis e ilimitado**, con o sin
  sesión. `copyResolvedText()` ya no llama a ningún gate.
- **Gestionar más de 1 proyecto** (crear un 2do proyecto o duplicar uno
  existente) requiere sesión + prueba Pro activa o suscripción —
  `requestNewProject()`/`requestDuplicateProject()` llaman a
  `checkProFeatureGate()`.
- **Guardar personalización (`custom_additions`) o resultados de IA
  (`ai_output`)** con contenido no vacío requiere lo mismo —
  `saveGatedPromptField()` llama al mismo gate.
- El proyecto #1 (variables, checklist de progreso, modo guiado) sigue
  siendo gratis para siempre, sin sesión.

`check_trial_status()` (usuario con sesión) no cambió: sigue decidiendo si
hay prueba activa o suscripción. Lo que cambió es **desde dónde se llama**
(antes: antes de copiar; ahora: antes de crear el 2do proyecto o guardar
personalización/IA).

`check_anon_usage()`/la tabla `anon_usage` quedan **sin uso**: el límite de
"1 proyecto gratis" en modo anónimo se calcula del lado del cliente
(`loadProjects().length`), sin necesidad de rastrear IPs, porque el conteo
de proyectos ya vive en `localStorage` de forma visible. No se borran de la
base de datos por si ya hay datos históricos, pero ningún código del
cliente los llama ya.

## 1. Ejecutar el SQL

En el SQL Editor del mismo proyecto de Supabase ya configurado (`Database →
SQL Editor`), pega y ejecuta el contenido completo de
[`supabase/trial_gate.sql`](../supabase/trial_gate.sql), y después el de
[`supabase/prompt_copy_stats.sql`](../supabase/prompt_copy_stats.sql) (indicador
de "prompts más copiados" para el administrador — sigue funcionando igual,
no cambió con este rediseño).

## 2. Verificar la regla de seguridad crítica

Antes de dar esto por terminado, confirma en **Database → Tables** que:
- `anon_usage`, `user_trial` y `feedback` aparecen con **RLS habilitado**.
- `user_trial` tiene **una sola política**, de tipo `SELECT` — si ves
  alguna de `UPDATE`/`INSERT`/`ALL`, algo salió mal: cualquiera podría
  auto-extender su propia prueba desde la consola del navegador con el
  `anon key` público. El test `tests/test_trial_gate_schema.py` ya bloquea
  esto a nivel de repositorio, pero vale la pena confirmarlo también en el
  proyecto real.

## 3. Verificación funcional (manual, no automatizable desde aquí)

1. Abre el sitio en una ventana de incógnito (sin sesión).
2. Copia varios prompts distintos, sin límite — deben copiar normal siempre
   (ya no hay gate de copia).
3. Con 1 proyecto ya creado, intenta crear un 2do proyecto (botón "+ Nuevo"
   o "duplicar") — debe aparecer el muro de registro en vez de crearlo.
4. Intenta escribir algo en "Adiciones personalizadas" o "Resultado de la
   IA" en el modal ⓘ de un prompt — debe aparecer el muro de registro al
   primer carácter no vacío, y el campo debe quedar vacío de nuevo.
5. Inicia sesión con GitHub. Crear un 2do proyecto y guardar
   personalización/IA deben funcionar sin límite mientras la prueba esté
   activa.
6. Para simular el vencimiento sin esperar 1 semana real, en el SQL Editor:
   ```sql
   update user_trial set trial_expires_at = now() - interval '1 day'
   where user_id = (select id from auth.users where email = 'tu-email-de-prueba@ejemplo.com');
   ```
7. Recarga el sitio (con la misma sesión) e intenta crear un 2do proyecto —
   debe aparecer el muro de feedback en vez de crearlo (copiar prompts
   sigue funcionando normal, sin verse afectado).
8. Envía el formulario (calificación + comentario) — debe cerrarse el
   modal y crear el 2do proyecto/guardar personalización debe volver a
   funcionar de inmediato.
9. Confirma en **Table Editor → feedback** que la fila quedó registrada, y
   en **user_trial** que `trial_expires_at` avanzó ~1 semana desde el envío.
10. En **Table Editor → prompt_copy_stats**, confirma que aparece una fila
    por cada prompt copiado durante esta prueba, con `copy_count` correcto
    (esto sigue registrándose siempre, gratis o Pro, gate o no).

## Notas de diseño (por qué quedó así, no un olvido)

- **Copiar prompts nunca se gatea** — el repositorio es público, así que
  proteger el texto no tiene efecto real; el muro protege la plataforma
  (proyectos múltiples, personalización, resultados de IA), no el
  contenido. Ver `docs/STRATEGY.md`.
- **El límite de 1 proyecto gratis anónimo se evade abriendo varias
  ventanas de incógnito** (cada una con su propio `localStorage` vacío) —
  trade-off aceptado explícitamente: sin contenido real que proteger, el
  costo de hacerlo no vale la pena para la mayoría de usuarios, y los
  compradores objetivo (equipos, agencias) valoran la conveniencia de
  sincronizar entre dispositivos más que evadir un límite de conveniencia.
- **`user_trial` nunca es editable directo por el cliente** — la única vía
  de extender `trial_expires_at` es `submit_feedback_and_renew()`, que
  corre con privilegios de servidor (`security definer`).
- **Fail-open ante errores de red** — una caída transitoria de Supabase
  nunca bloquea a un usuario real.
- **El servidor MCP (`mcp-server/`) no está cubierto por este muro** — es
  un canal de distribución completamente separado, sin ninguna dependencia
  de Supabase; dado que copiar prompts ya es gratis en el sitio también,
  esto ya no representa una brecha del modelo de negocio.
