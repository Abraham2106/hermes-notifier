from abc import ABC, abstractmethod

class Storage(ABC):
    """Interfaz abstracta para el almacenamiento persistente del estado del monitor."""

    @abstractmethod
    def load(self) -> dict[str, set[str]]:
        """Carga el registro de identificadores ya procesados.

        Returns:
            dict[str, set[str]]: Diccionario que asocia palabras clave
                con conjuntos de identificadores de mensajes ya vistos.
        """
        pass

    @abstractmethod
    def save(self, seen: dict[str, set[str]]) -> None:
        """Guarda el registro de identificadores procesados.

        Args:
            seen (dict[str, set[str]]): Diccionario con los identificadores vistos.
        """
        pass
