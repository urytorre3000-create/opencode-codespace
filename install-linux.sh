#!/usr/bin/env bash
set -e

echo "==> Instalando OpenCode en Linux"

# 1. Instalar opencode (detecta arquitectura automáticamente)
if ! command -v opencode >/dev/null 2>&1; then
  curl -fsSL https://opencode.ai/install | bash
else
  echo "    opencode ya está instalado: $(opencode --version)"
fi

# 2. Asegurar que opencode esté en el PATH para la sesión
export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"

# 3. Verificación
echo "==> Versión de opencode:"
opencode --version

# 4. (Opcional) instalar/verificar GitHub CLI para autenticar el snippet de GitHub
if ! command -v gh >/dev/null 2>&1; then
  echo "    gh no encontrado. Instálalo con:  sudo apt install gh  (o brew)."
else
  gh auth status || echo "    Ejecuta 'gh auth login' para autenticar tu cuenta."
fi

echo ""
echo "==> Listo. Siguiente paso:"
echo "    opencode"
echo "    /connect        # añade tu API key / proveedor"
echo "    (o define DEEPSEEK_API_KEY y usa opencode.json)"
