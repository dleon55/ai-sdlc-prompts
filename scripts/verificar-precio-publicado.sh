#!/usr/bin/env bash
# Verifica que el precio PUBLICADO coincide con el precio COBRADO.
#
# Descarga /precios.html, /terminos.html y /reembolsos.html del sitio y
# falla si alguna declara un precio mensual distinto de
# PADDLE_PRICE_AMOUNT_USD (issue #232, T4). Lo corre deploy.yml como smoke
# test despues de desplegar a GCP, y se puede correr a mano:
#
#   PADDLE_PRICE_AMOUNT_USD=9 scripts/verificar-precio-publicado.sh
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
ESPERADO="$PADDLE_PRICE_AMOUNT_USD"
# El punto decimal es literal en la expresion regular.
ESPERADO_RE="${ESPERADO//./\\.}"

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
done

if [ "$fallos" -ne 0 ]; then
  echo "PRECIO_ERROR: $fallos pagina(s) no coinciden con PADDLE_PRICE_AMOUNT_USD=$ESPERADO"
  exit 1
fi
echo "PRECIO_OK: precios, terminos y reembolsos publican $ESPERADO USD"
