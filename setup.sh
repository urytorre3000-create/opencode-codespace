#!/usr/bin/env bash
set -e

echo "==> Configurando OpenCode en el Codespace"

if [ ! -f "opencode.json" ] && [ -f "opencode.example.json" ]; then
  cp "opencode.example.json" "opencode.json"
  echo "    creado opencode.json a partir de la plantilla"
fi

opencode --version
echo "==> Listo. Ejecuta:  opencode"
echo "    Si no configuraste el proveedor, escribe /connect o define la variable DEEPSEEK_API_KEY en los secrets del Codespace."
