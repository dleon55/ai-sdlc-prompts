#!/usr/bin/env bash
#
# Aplica nginx_prompts.conf en el servidor de producción, validando antes y
# revirtiendo si algo sale mal. Lo ejecuta el deploy (ver deploy.yml); se
# copia al servidor y se corre allí.
#
# ── Por qué existe ────────────────────────────────────────────────────
#
# El deploy copiaba HTML pero NUNCA aplicaba nginx_prompts.conf, así que el
# archivo del repositorio y el del servidor llevaban meses divergiendo sin
# que nada avisara. Se descubrió por dos síntomas que parecían no tener
# relación:
#
#   - la CSP del servidor bloqueaba el favicon del propio sitio (PR #206);
#   - la compresión era nivel 1 en vez de 6, porque al servidor le faltaba
#     `gzip_comp_level` -- por eso index.html pesaba 284 KB en la red y no
#     los 222 KB que daba el cálculo local.
#
# ── Por qué es tan defensivo ──────────────────────────────────────────
#
# ESTE NGINX SIRVE 8 SITIOS, entre ellos un Odoo de producción y una API.
# Un `reload` con configuración inválida los tumba TODOS, no solo este.
#
# De ahí el orden de las operaciones:
#
#   1. si el archivo no cambió, no se toca nada (el caso normal)
#   2. se respalda el actual con marca de tiempo
#   3. se instala el nuevo y se corre `nginx -t`
#   4. si NO valida, se restaura y se sale con error SIN recargar. nginx
#      sigue con la configuración vieja en memoria: los otros 7 sitios ni
#      se enteran
#   5. solo si valida, `reload` -- recarga en caliente, sin cortar
#      conexiones. Nunca `restart`
#   6. se comprueba que el sitio responde 200; si no, se restaura el
#      respaldo y se recarga otra vez
#
# La invariante: nginx NUNCA se recarga con una configuración que no pasó
# `nginx -t`.

set -euo pipefail

DEST="${NGINX_DEST:-/etc/nginx/sites-available/prompts.lionsystems.com.mx}"
NUEVO="${NGINX_NUEVO:-$HOME/nginx_prompts.conf.new}"
RESPALDOS="${NGINX_RESPALDOS:-$HOME/nginx-backups}"
HOST_SITIO="${NGINX_HOST_SITIO:-prompts.lionsystems.com.mx}"

sudo -n true 2>/dev/null || {
  echo "::error::el usuario del deploy no tiene sudo sin contraseña; no se puede aplicar la configuración"
  exit 1
}

[ -f "$NUEVO" ] || { echo "::error::no llegó $NUEVO"; exit 1; }

# Solo se ACTUALIZA un sitio que ya existe. Crear uno nuevo desde el deploy
# implicaría además el symlink en sites-enabled y el certificado TLS: eso se
# hace a mano, una vez, no en cada push.
[ -f "$DEST" ] || {
  echo "::error::no existe $DEST -- este script actualiza un sitio existente, no crea uno"
  exit 1
}

if sudo cmp -s "$NUEVO" "$DEST"; then
  echo "nginx: la configuración ya está al día; no se toca nada"
  rm -f "$NUEVO"
  exit 0
fi

mkdir -p "$RESPALDOS"
RESPALDO="$RESPALDOS/prompts.$(date +%Y%m%d-%H%M%S).conf"
sudo cp -p "$DEST" "$RESPALDO"
echo "nginx: respaldo en $RESPALDO"

echo "nginx: cambios a aplicar"
sudo diff -u "$DEST" "$NUEVO" || true

sudo install -o root -g root -m 644 "$NUEVO" "$DEST"

if ! sudo nginx -t; then
  sudo cp -p "$RESPALDO" "$DEST"
  echo "::error::nginx -t falló con la configuración nueva. Restaurada; NO se recargó nginx, los demás sitios siguen intactos."
  exit 1
fi

sudo systemctl reload nginx
sleep 3

# Se consulta por HTTPS contra el loopback, forzando la resolución del
# nombre real con --resolve: así se ejercita el server block de este sitio y
# su certificado, sin depender de DNS ni de la red externa.
#
# NO sirve consultar por HTTP: el sitio responde 301 hacia HTTPS, y una
# comprobación que espere 200 revertiría en CADA despliegue aunque la
# configuración fuera correcta. Se detectó probando este script contra el
# servidor antes de conectarlo al deploy.
CODIGO=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 \
         --resolve "${HOST_SITIO}:443:127.0.0.1" "https://${HOST_SITIO}/" || echo 000)

if [ "$CODIGO" != "200" ]; then
  sudo cp -p "$RESPALDO" "$DEST"
  if sudo nginx -t; then
    sudo systemctl reload nginx
    echo "::error::tras recargar, el sitio respondió $CODIGO. Configuración restaurada y nginx recargado."
  else
    # No debería ocurrir: el respaldo ya validaba. Si pasa, se avisa fuerte
    # en vez de dejarlo en silencio, porque afecta a los 8 sitios.
    echo "::error::el respaldo tampoco valida. nginx sigue corriendo con la configuración anterior en memoria. REVISAR A MANO: $RESPALDO"
  fi
  exit 1
fi

rm -f "$NUEVO"
echo "nginx: configuración aplicada y verificada (HTTP $CODIGO)"
