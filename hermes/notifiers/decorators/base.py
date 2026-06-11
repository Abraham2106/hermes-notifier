from abc import ABC, abstractmethod
from hermes.core.notifier import Notifier
from hermes.core.source import Message

class NotifierDecorator(Notifier, ABC):
    """Clase base para decoradores de Notifier.

    Envuelve un Notifier (concreto o decorado) y delega la llamada
    final a send(), permitiendo insertar comportamiento adicional
    antes y/o despues de la delegacion.
    """

    def __init__(self, wrapped: Notifier) -> None:
        self._wrapped = wrapped

    def send(self, keyword: str, message: Message) -> None:
        self._wrapped.send(keyword, message)

    def send_similar_batch(self, keyword: str, messages: list[Message]) -> None:
        self._wrapped.send_similar_batch(keyword, messages)

    def notify_text(self, text: str) -> None:
        self._wrapped.notify_text(text)
