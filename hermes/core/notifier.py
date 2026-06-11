from abc import ABC, abstractmethod
from hermes.core.source import Message

class Notifier(ABC):
    """Interfaz abstracta para el envio de notificaciones."""

    @abstractmethod
    def send(self, keywords: list[str], message: Message) -> None:
        """Envia una notificacion para un mensaje que coincidio con criterios exactos.

        Args:
            keywords (list[str]): Palabras clave que originaron la alerta.
            message (Message): Mensaje detectado.
        """
        pass

    @abstractmethod
    def send_similar_batch(self, batch: list[tuple[Message, list[str]]]) -> None:
        """Envia una notificacion agrupada para mensajes que coinciden de forma difusa.

        Args:
            batch (list[tuple[Message, list[str]]]): Lista de tuplas (Mensaje, Lista de Keywords).
        """
        pass

    @abstractmethod
    def notify_text(self, text: str) -> None:
        """Envia un mensaje de texto directo al canal de notificacion.

        Args:
            text (str): Texto a enviar.
        """
        pass

