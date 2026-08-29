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

## Archivos incluidos

| Archivo | Rol |
| --- | --- |
| `.devcontainer/devcontainer.json` | Crea el Codespace (Ubuntu + Node LTS), instala opencode y ejecuta `setup.sh` |
| `.devcontainer/setup.sh` | Crea `opencode.json` desde la plantilla y verifica la instalación |
| `opencode.json` | Config del modelo (`deepseek-chat`) |
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
