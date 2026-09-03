#!/usr/bin/env python3
"""
📧 Recordatorio diario de calistenia — envía por correo (SMTP) el plan del día.

Genera el plan con `entrenador_calistenia.py` y lo envía como correo HTML/plano
usando la cuenta configurada en las variables de entorno.

Configuración (archivo `.env`, ver `.env.example`):
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=tu_correo@gmail.com
  SMTP_PASSWORD=tu_app_password        # contraseña de aplicación, NO la normal
  EMAIL_TO=destinatario@gmail.com      # si se omite, usa SMTP_USER
  EMAIL_FROM=opcional                  # si se omite, usa SMTP_USER

  # Si quieres cambiar la hora del envío automático (no hace falta para
  # ejecución manual).

Uso:
  python3 enviar_recordatorio_diario.py          # envía el plan de HOY
  python3 enviar_recordatorio_diario.py --fecha 2026-09-02
  python3 enviar_recordatorio_diario.py --preview  # muestra el correo sin enviar
"""

import argparse
import os
import smtplib
import sys
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv no es obligatorio si las variables ya existen
    pass

# Reutilizar el generador del plan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entrenador_calistenia import cargar_config, construir_plan, texto_plan  # noqa: E402

# --------------------------------------------------------------------------- #
# Estilo del correo (HTML)
# --------------------------------------------------------------------------- #

CSS = """
    body { font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
           background: #f4f6f8; color: #22303c; margin: 0; padding: 0; }
    .wrap { max-width: 620px; margin: 24px auto; background: #fff;
            border-radius: 12px; overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,.08); }
    .head { background: linear-gradient(135deg,#ff6b35,#ff3d3d);
            color: #fff; padding: 22px 26px; }
    .head h1 { margin: 0; font-size: 20px; }
    .head p { margin: 6px 0 0; opacity: .92; font-size: 13px; }
    .body { padding: 20px 26px; font-size: 14px; line-height: 1.55; }
    h2 { color: #ff6b35; font-size: 15px; text-transform: uppercase;
         letter-spacing: .4px; margin: 22px 0 8px; }
    h2:first-child { margin-top: 0; }
    ol, ul { margin: 4px 0 10px 22px; padding: 0; }
    li { margin: 4px 0; }
    .meta { background: #fff5ee; border: 1px solid #ffdcc3; border-radius: 8px;
            padding: 10px 14px; margin: 0 0 4px; font-size: 13px; }
    .tip { background: #eef7ff; border-left: 4px solid #1e90ff; border-radius: 6px;
           padding: 10px 14px; margin-top: 18px; font-size: 13px; }
    .foot { background: #f8fafb; color: #6b7a88; font-size: 12px;
            padding: 14px 26px; text-align: center; }
"""


def plan_a_html(plan):
    """Convierte el plan (diccionario) en HTML legible."""
    nombre = plan.get("nombre", "Atleta")
    fecha = plan.get("fecha", "")
    dia = plan.get("dia", "")

    if plan["tipo"] == "descanso":
        body = (
            "<h2>✅ Día de descanso</h2>"
            f"<p>{plan.get('mensaje', '')}</p>"
        )
    else:
        etiqueta = plan.get("etiqueta", "ENTRENAMIENTO")
        nivel = plan.get("nivel", "").title()
        duracion = plan.get("duracion", 30)
        objetivo = plan.get("objetivo", "")

        partes = [f'<p class="meta">🏷️ <b>{etiqueta}</b> &nbsp;·&nbsp; '
                  f'Nivel: {nivel} &nbsp;·&nbsp; ⏱ ~{duracion} min &nbsp;·&nbsp; '
                  f'🎯 Objetivo: {objetivo}</p>']

        partes.append("<h2>🔥 Calentamiento (5-8 min)</h2><ol>")
        for ej in plan.get("calentamiento", []):
            partes.append(f"<li>{ej}</li>")
        partes.append("</ol>")

        partes.append("<h2>💪 Entrenamiento principal</h2><ul>")
        for ej, reps, desc in plan.get("rutina", []):
            partes.append(f"<li><b>{ej}</b> — {reps} <span style='color:#6b7a88'>"
                          f"(descanso {desc})</span></li>")
        partes.append("</ul>")

        partes.append("<h2>🎯 Foco / Habilidad (10 min)</h2>")
        partes.append("<ul>")
        for ej in plan.get("foco_ejercicios", []):
            partes.append(f"<li>{ej}</li>")
        partes.append("</ul>")

        partes.append("<h2>🧘 Enfriamiento (5 min)</h2><ol>")
        for ej in plan.get("enfriamiento", []):
            partes.append(f"<li>{ej}</li>")
        partes.append("</ol>")

        partes.append('<div class="tip">💡 <b>Consejo del coach:</b> prioriza la '
                      'técnica sobre el número de repeticiones. Descansa al menos '
                      '48 h antes de repetir el mismo grupo muscular.</div>')
        body = "".join(partes)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="wrap">
  <div class="head">
    <h1>🧗 Tu plan de calistenia de hoy</h1>
    <p>{fecha} · {dia.title()} · Para: {nombre}</p>
  </div>
  <div class="body">{body}
    <div class="tip">¿Entrenaste hoy? Registra tu sesión con:
      <code>python3 entrenador_calistenia.py --completado</code></div>
  </div>
  <div class="foot">Enviado por tu entrenador personal de calistenia 💪</div>
</div></body></html>"""
    return html


# --------------------------------------------------------------------------- #
# Envío SMTP
# --------------------------------------------------------------------------- #

def obtener_env(correo_cfg=None):
    """Devuelve la configuración de SMTP validando lo esencial."""
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if not all([host, user, password]):
        print("❌ Faltan variables de entorno. Revisa tu archivo .env:")
        print("   SMTP_HOST, SMTP_USER, SMTP_PASSWORD (y opcional EMAIL_TO).")
        print("   Copia .env.example a .env y complétalo.")
        sys.exit(1)
    # Destinatario: prioridad EMAIL_TO > correo de la config del atleta > usuario SMTP
    to_addr = os.getenv("EMAIL_TO") or correo_cfg or user
    from_addr = os.getenv("EMAIL_FROM") or user
    return host, port, user, password, to_addr, from_addr


def enviar_correo(plan, preview=False):
    """Envía (o previsualiza) el correo con el plan del día."""
    host, port, user, password, to_addr, from_addr = obtener_env(
        correo_cfg=plan.get("correo")
    )

    asunto = f"🧗 Tu plan de calistenia · {plan['fecha']} ({plan['dia']})"
    cuerpo_texto = texto_plan(plan)
    cuerpo_html = plan_a_html(plan)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(cuerpo_texto, "plain", "utf-8"))
    msg.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    if preview:
        print("=== PREVIEW del correo (no se envía) ===")
        print("De:", from_addr)
        print("Para:", to_addr)
        print("Asunto:", asunto)
        print("-" * 60)
        print(cuerpo_texto)
        return 0

    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        if port == 587:
            server.starttls()
        server.login(user, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print(f"✅ Correo enviado a {to_addr} — {asunto}")
        return 0
    except smtplib.SMTPAuthenticationError:
        print("❌ Autenticación SMTP fallida. Si usas Gmail, genera una "
              "'contraseña de aplicación' (app password) en tu cuenta.")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Error al enviar el correo: {exc}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Envía el recordatorio diario de calistenia por correo.")
    parser.add_argument("--fecha", help="Fecha (YYYY-MM-DD). Por defecto: hoy.")
    parser.add_argument("--preview", action="store_true",
                        help="Muestra el correo sin enviarlo.")
    args = parser.parse_args()

    cfg = cargar_config()
    hoy = datetime.now().date()
    fecha = date.fromisoformat(args.fecha) if args.fecha else hoy
    plan = construir_plan(cfg, fecha)

    return enviar_correo(plan, preview=args.preview)


if __name__ == "__main__":
    sys.exit(main())
