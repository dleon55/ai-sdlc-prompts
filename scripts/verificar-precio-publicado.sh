#!/usr/bin/env bash
# Verifica que el precio PUBLICADO coincide con el precio COBRADO.
#
# Descarga /precios.html, /terminos.html y /reembolsos.html del sitio y
# falla si alguna declara un precio mensual distinto de
# PADDLE_PRICE_AMOUNT_USD, o un anual distinto de PADDLE_PRICE_AMOUNT_ANNUAL_USD
# (vacia = sin plan anual) (issue #232, T4; anual en las tres desde #236). Lo corre deploy.yml como smoke
# test despues de desplegar a GCP, y se puede correr a mano:
#
#   PADDLE_PRICE_AMOUNT_USD=9 scripts/verificar-precio-publicado.sh
#   PADDLE_PRICE_AMOUNT_USD=9 PADDLE_PRICE_AMOUNT_ANNUAL_USD=90 scripts/verificar-precio-publicado.sh
#   PADDLE_PRICE_AMOUNT_USD=9 SITIO_URL=file://$PWD scripts/verificar-precio-publicado.sh
#
# Por que existe: build.py ya ata el precio de las tres paginas a la misma
# variable, pero eso solo garantiza coherencia en el ARTEFACTO. Lo que ve el
# cliente es lo que sirve nginx, y ahi un deploy a medias (una pagina
# copiada y otra no), una cache o una variable cambiada entre builds puede
# dejar terminos.html prometiendo un precio y el checkout cobrando otro.
# Esa discrepancia es la que ya ocurrio con el $499 de Gumroad.
#
# Lee la meta <meta name="precio-mensual-usd"> que emite build.py en las
# tres paginas (buscar el numero en la prosa es fragil: el ancla "antes
# $19 USD" tambien contiene "9 USD"), y ademas exige que el numero aparezca
# en el texto visible, porque la meta podria quedar bien y el copy mal.
set -euo pipefail

: "${PADDLE_PRICE_AMOUNT_USD:?Define PADDLE_PRICE_AMOUNT_USD con el precio mensual esperado (ej. 9)}"
BASE="${SITIO_URL:-https://prompts.lionsystems.com.mx}"
BASE="${BASE%/}"
# Sin espacios: build.py recorta las variables al leerlas, y una variable
# de GitHub con un espacio de mas haria fallar un deploy correcto.
ESPERADO="$(printf '%s' "$PADDLE_PRICE_AMOUNT_USD" | tr -d '[:space:]')"
# Plan anual: opcional, como en build.py. Vacio = no se vende anual y
# ninguna pagina debe declararlo.
ESPERADO_ANUAL="$(printf '%s' "${PADDLE_PRICE_AMOUNT_ANNUAL_USD:-}" | tr -d '[:space:]')"
# El punto decimal es literal en la expresion regular.
ESPERADO_RE="${ESPERADO//./\\.}"
ESPERADO_ANUAL_RE="${ESPERADO_ANUAL//./\\.}"

fallos=0
for pagina in precios terminos reembolsos; do
  url="$BASE/$pagina.html"
  if ! html=$(curl -sS --fail --max-time 20 "$url"); then
    echo "ERROR: no se pudo descargar $url"
    fallos=$((fallos + 1))
    continue
  fi

  meta=$(printf '%s' "$html" \
    | grep -o '<meta name="precio-mensual-usd" content="[^"]*"' \
    | sed 's/.*content="\([^"]*\)".*/\1/' | head -n 1 || true)

  if [ -z "$meta" ]; then
    echo "ERROR: $url no declara <meta name=\"precio-mensual-usd\">; ¿se desplego un build viejo?"
    fallos=$((fallos + 1))
    continue
  fi
  if [ "$meta" != "$ESPERADO" ]; then
    echo "ERROR: $url publica $meta USD y el checkout cobra $ESPERADO USD"
    fallos=$((fallos + 1))
    continue
  fi
  if ! printf '%s' "$html" | grep -Eq "(^|[^0-9.])${ESPERADO_RE} USD"; then
    echo "ERROR: $url declara $meta en la meta pero el texto visible no dice '$ESPERADO USD'"
    fallos=$((fallos + 1))
    continue
  fi
  echo "OK: $url publica $meta USD"

  # El anual lo citan las tres paginas cuando se vende (meta
  # precio-anual-usd, ver build.py; terminos y reembolsos desde #236). Se
  # compara en ambos sentidos: una pagina no puede ofrecer un anual que no
  # se cobra ni callar uno que si.
  anual=$(printf '%s' "$html" \
    | grep -o '<meta name="precio-anual-usd" content="[^"]*"' \
    | sed 's/.*content="\([^"]*\)".*/\1/' | head -n 1 || true)
  if [ "$anual" != "$ESPERADO_ANUAL" ]; then
    echo "ERROR: $url publica precio-anual-usd=${anual:-(ninguno)} y el checkout anual cobra ${ESPERADO_ANUAL:-(sin anual)} USD"
    fallos=$((fallos + 1))
  elif [ -n "$ESPERADO_ANUAL" ] && ! printf '%s' "$html" | grep -Eq "(^|[^0-9.])${ESPERADO_ANUAL_RE} USD"; then
    echo "ERROR: $url declara $anual anual en la meta pero el texto visible no dice '$ESPERADO_ANUAL USD'"
    fallos=$((fallos + 1))
  elif [ -n "$ESPERADO_ANUAL" ]; then
    echo "OK: $url publica $anual USD anual"
  fi
done

if [ "$fallos" -ne 0 ]; then
  echo "PRECIO_ERROR: $fallos discrepancia(s) con PADDLE_PRICE_AMOUNT_USD=$ESPERADO / PADDLE_PRICE_AMOUNT_ANNUAL_USD=${ESPERADO_ANUAL:-(sin anual)}"
  exit 1
fi
echo "PRECIO_OK: precios, terminos y reembolsos publican $ESPERADO USD"
