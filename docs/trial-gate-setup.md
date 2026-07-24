# Configuración del muro de registro + prueba de 1 mes + feedback

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
permite la copia en vez de bloquearla, así que un visitante anónimo no
pierde acceso por un despliegue a medias.

## 1. Ejecutar el SQL

En el SQL Editor del mismo proyecto de Supabase ya configurado (`Database →
SQL Editor`), pega y ejecuta el contenido completo de
[`supabase/trial_gate.sql`](../supabase/trial_gate.sql).

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
2. Copia 2 prompts distintos — deben copiar normal.
3. Intenta copiar un 3er prompt — debe aparecer el muro de registro en vez
   de copiar.
4. Inicia sesión con GitHub. Copia debe funcionar sin límite mientras la
   prueba esté activa.
5. Para simular el vencimiento sin esperar 1 mes real, en el SQL Editor:
   ```sql
   update user_trial set trial_expires_at = now() - interval '1 day'
   where user_id = (select id from auth.users where email = 'tu-email-de-prueba@ejemplo.com');
   ```
6. Recarga el sitio (con la misma sesión) e intenta copiar — debe aparecer
   el muro de feedback en vez de copiar.
7. Envía el formulario (calificación + comentario) — debe cerrarse el
   modal y la copia debe volver a funcionar de inmediato.
8. Confirma en **Table Editor → feedback** que la fila quedó registrada, y
   en **user_trial** que `trial_expires_at` avanzó ~1 mes desde el envío.

## Notas de diseño (por qué quedó así, no un olvido)

- **El límite anónimo es por IP, no por navegador** — borrar `localStorage`
  o usar incógnito no lo evade. Una IP compartida (oficina, universidad)
  cuenta como un solo visitante; se acepta como fricción del pilotaje, no
  como un defecto a corregir.
- **`user_trial` nunca es editable directo por el cliente** — la única vía
  de extender `trial_expires_at` es `submit_feedback_and_renew()`, que
  corre con privilegios de servidor (`security definer`).
- **Fail-open ante errores de red** — una caída transitoria de Supabase
  nunca bloquea a un usuario real; el tradeoff aceptado es que un
  bloqueador de anuncios agresivo podría anular el límite igual que ya se
  acepta la fricción de IP compartida.
- **El servidor MCP (`mcp-server/`) no está cubierto por este muro** — es
  un canal de distribución completamente separado, sin ninguna dependencia
  de Supabase; gatearlo sería un requerimiento nuevo, no una extensión de
  este.
