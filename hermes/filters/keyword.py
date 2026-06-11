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

    def matches(self, message: Message) -> str:
        """Valida si el mensaje contiene la palabra clave y el nivel de coincidencia.

        La busqueda usa coincidencias exactas o difusas (fuzzy matching).

        Args:
            message (Message): Mensaje a analizar.

        Returns:
            str: "EXACT", "SIMILAR" o "NONE".
        """
        from hermes.utils.matching import categorize_match
        
        # Unir todos los campos en un solo texto para el escaneo
        full_text = f"{message.subject} {message.sender} {message.body}"
        return categorize_match(self._key, full_text)
