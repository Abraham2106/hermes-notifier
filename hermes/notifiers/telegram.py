import time
import requests
from urllib.parse import quote
from hermes.core.notifier import Notifier
from hermes.core.source import Message
from hermes.config import Config
from hermes.logger import logger

class TelegramNotifier(Notifier):
    """Implementacion de Notifier para canalizar alertas mediante bots de Telegram."""

    def __init__(self, config: Config) -> None:
        """Inicializa el notificador de Telegram con credenciales del sistema.

        Args:
            config (Config): Objeto de configuracion del sistema.
        """
        self._token = config.telegram_bot_token
        self._chat_id = config.telegram_chat_id
        # Mantener la URL base para el envío seguro.
        self._base_url = "https://api.telegram.org/bot"

    def _sanitize_markdown(self, text: str) -> str:
        """Sanitiza caracteres especiales para evitar inyecciones Markdown en Telegram.

        Args:
            text (str): Texto a sanitizar.

        Returns:
            str: Texto sanitizado.
        """
        # Telegram MarkdownV2 exige escapar estos caracteres: _ * [ ] ( ) ~ ` > # + - = | { } . !
        # Para Markdown basico o texto plano HTML, removemos o escapamos los basicos.
        # En este caso, usaremos el modo por defecto de texto de Telegram (sin parse_mode)
        # pero eliminamos caracteres que podrian alterar la visualizacion.
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _post_with_retry(self, text: str) -> None:
        """Realiza una llamada POST a la API de Telegram con logica de reintentos y timeouts.

        Args:
            text (str): Mensaje de texto a enviar.
        """
        url = f"{self._base_url}{self._token}/sendMessage"
        payload = {
            "chat_id": self._chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        max_retries = 3
        backoff = 2.0

        for attempt in range(1, max_retries + 1):
            try:
                # Se establece timeout de 10 segundos de conexion y lectura.
                resp = requests.post(url, json=payload, timeout=(5, 10))
                
                # Manejar Rate Limiting (HTTP 429) de forma inteligente.
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 5))
                    logger.warning(f"Telegram API Rate Limited (429). Esperando {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                if not resp.ok:
                    logger.error(f"Error al enviar Telegram {resp.status_code}: {resp.text}")
                    # No reintentar en errores de cliente 4xx a menos que sea 429.
                    if 400 <= resp.status_code < 500:
                        break
                else:
                    return
            except requests.exceptions.RequestException as e:
                logger.warning(f"Intento {attempt}/{max_retries} fallido al conectar con Telegram: {e}")
                if attempt == max_retries:
                    logger.error("Se agotaron los intentos de conexion con la API de Telegram.")
                    break
                time.sleep(backoff * attempt)

    def send(self, keywords: list[str], message: Message) -> None:
        """Envia un mensaje formateado a Telegram notificando coincidencias exactas.

        Args:
            keywords (list[str]): Palabras clave que originaron la alerta.
            message (Message): Datos del mensaje recibido.
        """
        clean_keywords = [self._sanitize_markdown(k) for k in keywords]
        clean_sender = self._sanitize_markdown(message.sender)
        clean_subject = self._sanitize_markdown(message.subject)

        text = (
            f"<b>[NUEVO CORREO]</b>\n"
            f"<b>Keywords:</b> {', '.join(clean_keywords)}\n"
            f"<b>De:</b> {clean_sender}\n"
            f"<b>Asunto:</b> {clean_subject}"
        )
        self._post_with_retry(text)
        logger.info(f"Telegram enviado para keywords '{', '.join(keywords)}': {message.subject[:40]}")

    def send_similar_batch(self, batch: list[tuple[Message, list[str]]]) -> None:
        """Envia un mensaje agrupado con coincidencias similares a Telegram.

        Args:
            batch (list[tuple[Message, list[str]]]): Lista de correos y sus keywords similares.
        """
        if not batch:
            return
            
        text_lines = [
            f"<b>[SIMILARES DETECTADOS]</b>",
            ""
        ]
        
        for msg, kws in batch:
            clean_kws = [self._sanitize_markdown(k) for k in kws]
            clean_sender = self._sanitize_markdown(msg.sender)
            clean_subject = self._sanitize_markdown(msg.subject)
            text_lines.append(f"• De: {clean_sender} | Asunto: {clean_subject}")
            text_lines.append(f"  Keywords: {', '.join(clean_kws)}")
            
        text = "\n".join(text_lines)
        self._post_with_retry(text)
        logger.info(f"Telegram enviado lote de {len(batch)} correos similares")

    def notify_text(self, text: str) -> None:
        """Envia un mensaje de texto directo al chat de Telegram.

        Args:
            text (str): Texto a enviar.
        """
        clean_text = self._sanitize_markdown(text)
        self._post_with_retry(clean_text)

