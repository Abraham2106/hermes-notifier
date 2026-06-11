import time
from hermes.core.notifier import Notifier
from hermes.core.source import Message
from hermes.notifiers.decorators.base import NotifierDecorator
from hermes.logger import logger

class RetryNotifierDecorator(NotifierDecorator):
    """Reintenta el envio de notificaciones ante fallos temporales."""

    def __init__(self, wrapped: Notifier, max_attempts: int = 3, base_delay: float = 1.0) -> None:
        super().__init__(wrapped)
        self._max_attempts = max_attempts
        self._base_delay = base_delay

    def send(self, keyword: str, message: Message) -> None:
        last_error = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                self._wrapped.send(keyword, message)
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Intento {attempt}/{self._max_attempts} fallido al enviar notificacion con '{keyword}': {e}"
                )
                if attempt < self._max_attempts:
                    time.sleep(self._base_delay * (2 ** (attempt - 1)))
        
        logger.error(f"Notificacion descartada permanentemente tras {self._max_attempts} intentos: {last_error}")
        raise last_error

    def notify_text(self, text: str) -> None:
        last_error = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                self._wrapped.notify_text(text)
                return
            except Exception as e:
                last_error = e
                logger.warning(f"Intento {attempt}/{self._max_attempts} fallido al enviar texto: {e}")
                if attempt < self._max_attempts:
                    time.sleep(self._base_delay * (2 ** (attempt - 1)))
        
        logger.error(f"Notificacion de texto descartada permanentemente tras {self._max_attempts} intentos: {last_error}")
        raise last_error
