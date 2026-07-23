# Configuración de registro de usuarios (Supabase Auth + GitHub)

> **Estado: configurado.** `build.py` ya tiene el `SUPABASE_URL` y la
> `anon`/`publishable key` reales (no el centinela) y el proyecto de
> Supabase tiene el proveedor de GitHub, los dominios permitidos y la
> tabla `projects` con RLS habilitado. Esta página queda como referencia
> de los pasos ya ejecutados — útil si necesitas rotar la clave, agregar
> un dominio nuevo, o recrear el proyecto desde cero.

El código de registro de usuarios está implementado en `build.py` (ver
sección `AUTENTICACIÓN (Supabase + GitHub)` en el JS embebido). Ninguno de
los pasos de configuración puede hacerse desde este repositorio, porque
requieren una cuenta humana (Supabase, GitHub) con permisos de
administración — por eso quedan documentados aquí en vez de automatizados.

Mientras **no** esté configurado (p. ej. tras clonar el repo con los
valores centinela por defecto, o si se revierte a ellos):
- El botón "Iniciar sesión" es visible pero muestra un aviso de que falta
  configuración, en vez de intentar hablar con un backend inexistente.
- No se descarga ningún script externo nuevo (el SDK de Supabase solo se
  carga una vez configurado — ver el comentario junto a `SUPABASE_URL` en
  `build.py`).
- El uso anónimo (sin cuenta) sigue funcionando exactamente igual que hoy.

## 1. Crear el proyecto de Supabase

1. Crear una cuenta/organización en [supabase.com](https://supabase.com) si
   no existe una ya.
2. Crear un nuevo proyecto. Anotar la **Project URL** y la **anon public
   key** (Settings → API) — se necesitan en el paso 5.
3. **Nunca** copiar la `service_role key` a ningún archivo de este
   repositorio: esa clave tiene acceso total sin RLS.

## 2. Registrar la GitHub OAuth App

Se registra **una sola vez**, sin importar cuántos dominios sirvan el sitio
(GitHub Pages y GCP comparten esta misma app):

1. En GitHub: Settings → Developer settings → OAuth Apps → New OAuth App.
2. **Authorization callback URL**: `https://<tu-proyecto>.supabase.co/auth/v1/callback`
   (no la URL de tu sitio — Supabase es quien recibe el callback de GitHub).
3. Copiar el **Client ID** y generar un **Client Secret**.
4. En el panel de Supabase: Authentication → Providers → GitHub, pegar
   ambos valores y habilitar el proveedor.

## 3. Configurar los dominios permitidos

En Supabase: Authentication → URL Configuration.

| Campo | Valor |
|---|---|
| Site URL | `https://prompts.lionsystems.com.mx` (producción) |
| Redirect URLs (adicional) | la URL de GitHub Pages de este repositorio |

Como GitHub Pages está marcado como *staging* en `.github/workflows/deploy.yml`,
considera usar un proyecto de Supabase separado para pruebas, o al menos no
anunciar el login ahí, para no mezclar cuentas de prueba con datos reales.

## 4. Crear la tabla y su política de seguridad

Ejecutar `supabase/schema.sql` completo en el SQL Editor del proyecto de
Supabase (Database → SQL Editor → pegar y ejecutar). Verificar después que
Row Level Security aparece como **habilitado** en la tabla `projects`
(Database → Tables) — sin eso, el `anon key` público expondría los
proyectos de todos los usuarios entre sí.

## 5. Completar los valores en build.py

Buscar en `build.py` (dentro de la sección `AUTENTICACIÓN (Supabase + GitHub)`):

```js
var SUPABASE_URL = 'PENDIENTE_CONFIGURAR';
var SUPABASE_ANON_KEY = 'PENDIENTE_CONFIGURAR';
```

Reemplazar ambos valores por la Project URL y la anon key del paso 1, correr
`python build.py` para regenerar `index.html`, y desplegar como de
costumbre. El `anon key` es seguro de exponer en el HTML público — está
diseñado para vivir en el cliente; la protección real la da la política RLS
del paso 4, no el secreto de esta clave.

## Verificación tras configurar

1. Abrir el sitio, hacer clic en "Iniciar sesión" → debe redirigir a GitHub,
   no mostrar el aviso de "no configurado".
2. Con sesión iniciada, crear un proyecto y confirmar que aparece la fila
   correspondiente en la tabla `projects` de Supabase.
3. Cerrar sesión y volver a iniciar sesión (o desde otro navegador) →
   el proyecto creado debe seguir ahí.
4. Repetir la verificación en **ambos** dominios (GitHub Pages y
   `prompts.lionsystems.com.mx`) — comparten el mismo proyecto de Supabase,
   pero cada uno es un origen distinto en el navegador.
