from hermes.core.filter import Filter
from hermes.core.source import Message

class KeywordFilter(Filter):
    """Filtro basado en coincidencias por palabras clave.

    Evalua si el titulo, remitente o cuerpo contienen la hilera buscada.
    """

    def __init__(self, key: str) -> None:
        """Inicializa el filtro con una palabra clave especifica.

        Args:
            key (str): Palabra clave a buscar.
        """
        self._key = key

    @property
    def keyword(self) -> str:
        """Retorna la palabra clave asociada a este filtro.

        Returns:
            str: Palabra clave.
        """
        return self._key

    def matches(self, message: Message) -> bool:
        """Valida si el mensaje contiene la palabra clave.

        La busqueda no distingue entre mayusculas y minusculas.

        Args:
            message (Message): Mensaje a analizar.

        Returns:
            bool: True si coincide, False en caso contrario.
        """
        key_lower = self._key.lower()
        
        # Realizar busquedas insensibles a mayusculas.
        in_subject = key_lower in message.subject.lower()
        in_sender = key_lower in message.sender.lower()
        in_body = key_lower in message.body.lower()
        
        return in_subject or in_sender or in_body
