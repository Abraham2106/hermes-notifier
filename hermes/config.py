import os
import re
from dotenv import load_dotenv
from hermes.logger import logger

# Cargar .env si existe en entorno local.
load_dotenv()

class Config:
    """Clase encargada de cargar, validar y exponer la configuracion del sistema.

    Atributos:
        gmail_client_id (str): ID de cliente para la API de Google.
        gmail_client_secret (str): Secreto de cliente para la API de Google.
        gmail_refresh_token (str): Refresh token para autorizar la lectura de Gmail.
        telegram_bot_token (str): Token de acceso para el bot de Telegram.
        telegram_chat_id (str): ID del chat de Telegram para notificaciones.
        keywords (list[str]): Lista de palabras clave a monitorear.
        poll_interval (int): Intervalo de actualizacion en segundos.
        seen_file (str): Ruta al archivo donde se almacenan los IDs procesados.
    """

    def __init__(self) -> None:
        self.gmail_client_id = os.environ["GMAIL_CLIENT_ID"].strip()
        self.gmail_client_secret = os.environ["GMAIL_CLIENT_SECRET"].strip()
        self.gmail_refresh_token = os.environ["GMAIL_REFRESH_TOKEN"].strip()
        self.telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"].strip()
        self.telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"].strip()
        
        # Procesamiento seguro de palabras clave.
        raw_keywords = os.environ.get("GMAIL_KEYWORDS", "Quantathon")
        # Filtrar keywords vacias o con caracteres invalidos basicos.
        self.keywords = []
        for k in raw_keywords.split(","):
            clean_k = k.strip()
            if clean_k:
                # Sanitizar keyword para evitar inyecciones basicas o patrones maliciosos en busquedas.
                clean_k = re.sub(r'["\\]', '', clean_k)
                if clean_k:
                    self.keywords.append(clean_k)

        if not self.keywords:
            self.keywords = ["Quantathon"]
        
        # Intervalo y persistencia con validaciones de rangos seguros.
        try:
            interval_seconds = int(os.environ.get("POLL_INTERVAL_SECONDS", "120"))
        except ValueError:
            logger.warning("POLL_INTERVAL_SECONDS no es un entero valido. Usando default de 120 segundos.")
            interval_seconds = 120

        # Rango de seguridad minimo para evitar rate limits excesivos o bloqueos de API.
        if interval_seconds < 10:
            logger.warning("POLL_INTERVAL_SECONDS es inferior a 10s. Forzando minimo de 10s por seguridad.")
            interval_seconds = 10

        self.poll_interval = interval_seconds
        self.seen_file = "/data/seen_ids.json" if os.path.isdir("/data") else "seen_ids.json"

        # Opciones para Notifiers (Decoradores)
        self.use_retry = os.environ.get("NOTIFIER_USE_RETRY", "true").lower() == "true"
        self.use_sanitizing = os.environ.get("NOTIFIER_USE_SANITIZING", "true").lower() == "true"
        self.use_logging = os.environ.get("NOTIFIER_USE_LOGGING", "true").lower() == "true"
        
        try:
            self.retry_max_attempts = int(os.environ.get("NOTIFIER_RETRY_ATTEMPTS", "3"))
        except ValueError:
            self.retry_max_attempts = 3
            
        try:
            self.retry_delay = int(os.environ.get("NOTIFIER_RETRY_DELAY", "5"))
        except ValueError:
            self.retry_delay = 5
            
        try:
            self.sanitizing_max_length = int(os.environ.get("NOTIFIER_SANITIZING_MAX_LENGTH", "4000"))
        except ValueError:
            self.sanitizing_max_length = 4000

    @classmethod
    def from_env(cls) -> "Config":
        """Instancia la configuracion realizando validacion basica del entorno.

        Returns:
            Config: Objeto de configuracion inicializado.

        Raises:
            KeyError: Si alguna variable de entorno requerida no esta definida.
            ValueError: Si algun valor obligatorio contiene marcadores de posicion o esta vacio.
        """
        required = [
            "GMAIL_CLIENT_ID",
            "GMAIL_CLIENT_SECRET",
            "GMAIL_REFRESH_TOKEN",
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID"
        ]
        missing = [var for var in required if var not in os.environ]
        if missing:
            raise KeyError(
                f"Variables de entorno requeridas faltantes: {', '.join(missing)}"
            )

        # Validacion adicional para evitar placeholders.
        placeholders = ["TU_CLIENT_ID", "TU_CLIENT_SECRET", "TU_REFRESH_TOKEN", "123456789:AAxx", "TU_CHAT_ID"]
        for var in required:
            val = os.environ[var]
            if not val.strip():
                raise ValueError(f"La variable de entorno {var} esta vacia.")
            if any(p in val for p in placeholders):
                raise ValueError(f"La variable de entorno {var} conserva el valor de ejemplo predeterminado.")

        return cls()

