from abc import ABC, abstractmethod
from hermes.core.source import Message

class Filter(ABC):
    """Interfaz abstracta para aplicar filtros de coincidencia en mensajes."""

    @property
    @abstractmethod
    def keyword(self) -> str:
        """Retorna la palabra clave asociada al filtro.

        Returns:
            str: Palabra clave o expresion de busqueda.
        """
        pass

    @abstractmethod
    def matches(self, message: Message) -> str:
        """Determina si un mensaje cumple con los criterios del filtro y su tipo.

        Args:
            message (Message): Mensaje a evaluar.

        Returns:
            str: "EXACT", "SIMILAR" o "NONE".
        """
        pass
