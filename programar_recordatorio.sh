#!/usr/bin/env bash
# 🗓️ Programador del recordatorio diario de calistenia (cron local, Linux/macOS).
#
# Envía el recordatorio por correo CADA DÍA a la hora indicada en HORA.
# Se apoya en cron. Instalación (una sola vez):
#
#   ./programar_recordatorio.sh install   # añade la entrada a crontab
#
# Para cambiar la hora o el correo, edita HORA y el archivo .env.
#
# Desinstalar:
#   ./programar_recordatorio.sh uninstall

set -e

# ---------- Configuración ----------
HORA="07:30"            # hora del recordatorio (formato HH:MM, 24 h)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENVIAR="$SCRIPT_DIR/enviar_recordatorio_diario.py"
CRON_LINE="$(printf '%s %s * * * cd %s && /usr/bin/python3 %s >> %s/recordatorio.log 2>&1' \
  "${HORA#*:}" "${HORA%:*}" "$SCRIPT_DIR" "$ENVIAR" "$SCRIPT_DIR")"

install_cron() {
  echo "==> Configurando cron para el recordatorio diario a las $HORA"
  if command -v crontab >/dev/null 2>&1; then
    # Evitar duplicados: elimina líneas que ya apunten a este script
    ( crontab -l 2>/dev/null | grep -v "$ENVIAR" ; echo "$CRON_LINE" ) | crontab -
    echo "    ✅ Cron instalado. Revisa con: crontab -l"
    echo "    Log: $SCRIPT_DIR/recordatorio.log"
  else
    echo "    ⚠️  No se encontró 'crontab'. Añade manualmente esta línea:"
    echo "       $CRON_LINE"
  fi
}

uninstall_cron() {
  echo "==> Eliminando cron del recordatorio"
  if command -v crontab >/dev/null 2>&1; then
    ( crontab -l 2>/dev/null | grep -v "$ENVIAR" ) | crontab - || true
    echo "    ✅ Cron eliminado."
  else
    echo "    No hay crontab disponible."
  fi
}

case "${1:-install}" in
  install)   install_cron ;;
  uninstall) uninstall_cron ;;
  *) echo "Uso: $0 [install|uninstall]"; exit 1 ;;
esac
