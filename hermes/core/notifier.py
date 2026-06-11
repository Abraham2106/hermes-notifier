from abc import ABC, abstractmethod
from hermes.core.source import Message

class Notifier(ABC):
    """Interfaz abstracta para el envio de notificaciones."""

    @abstractmethod
    def send(self, keyword: str, message: Message) -> None:
        """Envia una notificacion para un mensaje que coincidio con un criterio.

        Args:
            keyword (str): Palabra clave que origino la alerta.
            message (Message): Mensaje detectado.
        """
        pass

    @abstractmethod
    def send_similar_batch(self, keyword: str, messages: list[Message]) -> None:
        """Envia una notificacion agrupada para mensajes que coinciden de forma difusa.

        Args:
            keyword (str): Palabra clave que origino la alerta.
            messages (list[Message]): Lista de mensajes similares detectados.
        """
        pass

    @abstractmethod
    def notify_text(self, text: str) -> None:
        """Envia un mensaje de texto directo al canal de notificacion.

        Args:
            text (str): Texto a enviar.
        """
        pass

