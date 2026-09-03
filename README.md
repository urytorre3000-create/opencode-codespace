# OpenCode en GitHub Codespaces (Linux)

Plantilla lista para usar: inicia un Codespace con **OpenCode ya instalado y configurado automáticamente**.

## Es lo único que tienes que hacer

1. Sube esta carpeta a un repositorio de GitHub (incluye `.devcontainer`).
2. En GitHub: **Settings → Secrets and variables → Codespaces → Actions secrets → New repository secret**:
   - Nombre: `DEEPSEEK_API_KEY`  ·  Valor: tu clave real (ej. `sk-...`)
   - *(Cambia el nombre si usas otro proveedor).*
3. En GitHub: **Code → Codespaces → New codespace**.
4. Espera (unos segundos). OpenCode se instala solo (`postCreateCommand`) y crea `opencode.json` si no está.

## Primera ejecución

En la terminal del Codespace:

```bash
opencode
```

`opencode.json` ya define el modelo `deepseek-chat`. La clave la lee de la variable/secreto `DEEPSEEK_API_KEY`. Si prefieres autenticarte interactivamente, escribe `/connect` y pega tu clave.

## 🧗 Agente: Entrenador Personal de Calistenia

Este repositorio incluye un **agente entrenador de calistenia** que te asesora todos
los días y te envía un **recordatorio por correo** diario.

- `AGENTS.md` — El "agente": instrucciones para que la IA actúe como tu coach
  personal de calistenia (nivel, rotación, progresiones, motivación).
- `entrenador_calistenia.py` — Genera el **plan del día** (calentamiento + rutina +
  foco) según tu nivel y objetivo, y guarda el historial.
- `enviar_recordatorio_diario.py` — Arma el plan y lo **envía por correo (SMTP)**.
- `programar_recordatorio.sh` — Instala un **cron local** para el envío automático.
- `.github/workflows/recordatorio-diario.yml` — Envío automático **en la nube**
  (GitHub Actions) aunque el Codespace esté apagado.
- `calistenia_config.example.json` — Tus preferencias: nivel, días/semana, objetivo.

### Uso diario

```bash
python3 entrenador_calistenia.py             # ¿qué toca hoy?
python3 entrenador_calistenia.py --completado # registrar que ya entrenaste
python3 enviar_recordatorio_diario.py --preview # ver el correo sin enviarlo
python3 enviar_recordatorio_diario.py        # enviar el correo de hoy
```

### Ponerlo automático (elige una opción)

**Opción A — GitHub Actions (recomendada):** sube el repo a GitHub y crea estos
**secrets** en `Settings → Secrets and variables → Actions`:
`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_TO`. El workflow
corre cada día a las 12:30 UTC (ajusta la hora en el archivo `.yml`).

**Opción B — cron local:** edita la hora en `programar_recordatorio.sh` y ejecuta
`./programar_recordatorio.sh install`. Requiere `.env` configurado.

### Configuración del correo

Copia `.env.example` a `.env` y completa `SMTP_HOST`, `SMTP_USER`,
`SMTP_PASSWORD` (en Gmail: contraseña de aplicación) y `EMAIL_TO`.

> Nota: `calistenia_config.json` y `calistenia_log.json` (tus datos) están en
> `.gitignore` y no se suben. La plantilla `calistenia_config.example.json` sí.


| `opencode.example.json` | Plantilla por si quieres versiones alternativas |
| `.env.example` | Lista de variables/secrets a definir (copia a `.env` para local) |

## Comandos útiles

| Comando | Descripción |
| --- | --- |
| `opencode` | Abre la interfaz de terminal (TUI) |
| `/init` | Genera `AGENTS.md` con la estructura del repo |
| `/connect` | Configura el proveedor / API key |
| `/models` | Lista y cambia de modelo |
| `/undo` / `/redo` | Deshacer / rehacer cambios |

## Seguridad

- La clave **nunca** va al repositorio; se guarda como Secret de Codespaces.
- `DEEPSEEK_API_KEY` y `.env` están en `.gitignore`. No los agregues a un commit.

## Comandos útiles

| Comando            | Descripción                                     |
| ------------------ | ----------------------------------------------- |
| `opencode`         | Abre la interfaz de terminal (TUI)              |
| `/init`            | Genera `AGENTS.md` con la estructura del repo  |
| `/connect`         | Configura el proveedor / API key               |
| `/models`          | Lista y cambia de modelo                       |
| `/undo` / `/redo`  | Deshacer / rehacer cambios                      |

## Requisitos del proyecto

- El Codespace usa la imagen base Ubuntu + Node LTS (traída automáticamente).
- Puerto `4096` reenviado para OpenCode server (buffer de la TUI / IDE).
- Todo se configura en `.devcontainer/devcontainer.json`.

## Detenerlo

Cierra el Codespace desde GitHub (o `Ctrl+C` en la terminal). El contenedor se destruye; la instalación se repite automáticamente al volver a abrirlo.

> Nota: cambios hechos con `/init` quedan en `AGENTS.md` (rebautizado en español como "agente" en el sistema). Haz commit.
