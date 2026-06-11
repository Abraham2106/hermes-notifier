from abc import ABC, abstractmethod
from typing import Iterator

class Message:
    """Clase que representa un mensaje generico independiente de la fuente.

    Atributos:
        id (str): Identificador unico del mensaje.
        sender (str): Remitente del mensaje.
        subject (str): Asunto o titulo del mensaje.
        body (str): Cuerpo o contenido del mensaje (opcional).
    """

    def __init__(self, id: str, sender: str, subject: str, body: str = ""):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.body = body


class Source(ABC):
    """Interfaz abstracta para fuentes de mensajes."""

    @abstractmethod
    def fetch(self, query: str, max_results: int = 10) -> Iterator[Message]:
        """Obtiene mensajes desde la fuente externa.

        Args:
            query (str): Criterio de busqueda.
            max_results (int): Cantidad maxima de resultados a retornar.

        Returns:
            Iterator[Message]: Un iterador de objetos Message.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """Retorna el nombre identificador de la fuente.

        Returns:
            str: Nombre de la fuente (ej. 'gmail').
        """
        pass
