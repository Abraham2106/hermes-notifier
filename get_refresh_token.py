"""
Ejecuta esto UNA SOLA VEZ en tu computadora para obtener el GMAIL_REFRESH_TOKEN.

Pasos:
  1. Rellena tu .env con GMAIL_CLIENT_ID y GMAIL_CLIENT_SECRET
     (o edita las constantes abajo directamente).
  2. Corre:  python get_refresh_token.py
  3. Se abre el navegador → inicia sesión → acepta permisos.
  4. La consola imprime el REFRESH_TOKEN → cópialo a tu .env.
"""

import os
import re
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CLIENT_ID     = os.environ.get("GMAIL_CLIENT_ID", "TU_CLIENT_ID.apps.googleusercontent.com")
CLIENT_SECRET = os.environ.get("GMAIL_CLIENT_SECRET", "TU_CLIENT_SECRET")

if "TU_CLIENT" in CLIENT_ID or "TU_CLIENT" in CLIENT_SECRET:
    print("⚠️  Pon GMAIL_CLIENT_ID y GMAIL_CLIENT_SECRET en tu .env antes de correr esto.")
    raise SystemExit(1)

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    },
    SCOPES,
)

creds = flow.run_local_server(port=0)

# Escribir directamente al archivo .env para evitar leak de credenciales en la consola.
env_path = ".env"
try:
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            env_content = f.read()

    # Actualizar o insertar GMAIL_REFRESH_TOKEN en el archivo .env
    token_line = f"GMAIL_REFRESH_TOKEN={creds.refresh_token}"
    if "GMAIL_REFRESH_TOKEN=" in env_content:
        env_content = re.sub(
            r"GMAIL_REFRESH_TOKEN=.*",
            token_line,
            env_content
        )
    else:
        # Si no existe, agregarlo al final.
        if env_content and not env_content.endswith("\n"):
            env_content += "\n"
        env_content += token_line + "\n"

    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    print("\n" + "=" * 55)
    print("  [OK] Autenticacion exitosa y guardada en .env.")
    print("  El token se ha guardado de forma segura.")
    print("=" * 55)
except Exception as e:
    print(f"\n❌ Error al guardar en .env: {e}")
    # Solo en caso de error de escritura se muestra de forma restringida si es necesario.

