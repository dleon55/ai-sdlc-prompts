#!/usr/bin/env bash
# deploy-to-gcp.sh
# Uso: bash deploy-to-gcp.sh
# Requiere: build.py ejecutado previamente (python build.py)
# Servidor: GCP 34.51.112.6:2288
# Destino : https://prompts.lionsystems.com.mx

set -e

SSH_KEY="$HOME/.ssh/google_compute_engine"
REMOTE="dleon5555@34.51.112.6"
PORT=2288
REMOTE_PATH="/var/www/prompts/index.html"
LOCAL_PATH="$(dirname "$0")/index.html"

if [ ! -f "$LOCAL_PATH" ]; then
  echo "ERROR: index.html no encontrado. Ejecuta primero: python build.py"
  exit 1
fi

echo "==> Subiendo index.html al servidor GCP..."
scp -P $PORT -i "$SSH_KEY" -o StrictHostKeyChecking=no \
  "$LOCAL_PATH" "$REMOTE:$REMOTE_PATH"

echo "==> Ajustando permisos..."
ssh -p $PORT -i "$SSH_KEY" -o StrictHostKeyChecking=no "$REMOTE" \
  "sudo chown www-data:www-data $REMOTE_PATH && sudo chmod 644 $REMOTE_PATH"

echo "==> Verificando sitio..."
RESULT=$(ssh -p $PORT -i "$SSH_KEY" -o StrictHostKeyChecking=no "$REMOTE" \
  "curl -s -o /dev/null -w '%{http_code}' https://prompts.lionsystems.com.mx/")

if [ "$RESULT" = "200" ]; then
  echo "==> OK: https://prompts.lionsystems.com.mx — HTTP $RESULT"
else
  echo "ERROR: respuesta inesperada HTTP $RESULT"
  exit 1
fi
