#!/usr/bin/env python3
"""
Bot de Telegram (eco básico) usando python-telegram-bot v21+.

Configuración:
  1. Crea tu bot con @BotFather en Telegram y copia el token.
  2. Guarda el token en la variable de entorno TELEGRAM_BOT_TOKEN
     (por ejemplo, en un archivo .env — NO lo subas a git).
  3. Ejecuta:  python3 telegram_bot.py

Comandos:
  /start  — Mensaje de bienvenida.
  /help   — Ayuda con los comandos disponibles.
  Cualquier otro texto se devuelve como eco.
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configuración básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un mensaje de bienvenida cuando se envía /start."""
    user = update.effective_user
    await update.message.reply_text(
        f"¡Hola, {user.first_name}! 👋\n\n"
        "Soy un bot de ejemplo. Escríbeme cualquier cosa y te la devolveré como eco.\n"
        "Usa /help para ver los comandos disponibles."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra la ayuda con los comandos disponibles."""
    await update.message.reply_text(
        "📋 Comandos disponibles:\n"
        "/start — Mensaje de bienvenida\n"
        "/help  — Esta ayuda\n\n"
        "Cualquier otro mensaje se devuelve como eco. 🔁"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde haciendo eco del mensaje del usuario."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Punto de entrada principal del bot."""
    if not TOKEN:
        logger.error(
            "No se encontró TELEGRAM_BOT_TOKEN. "
            "Configúralo en un archivo .env o como variable de entorno."
        )
        raise SystemExit(1)

    # Crear la aplicación y registrar los manejadores
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot iniciado. Pulsa Ctrl+C para detenerlo.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
