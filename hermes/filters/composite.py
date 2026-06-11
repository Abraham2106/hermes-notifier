from hermes.core.filter import Filter
from hermes.core.source import Message

class CompositeFilter(Filter):
    """Filtro compuesto que agrupa una coleccion de filtros individuales.

    Permite evaluar de forma conjunta usando logica AND u OR.
    """

    def __init__(self, filters: list[Filter], mode: str = "OR") -> None:
        """Inicializa el filtro compuesto.

        Args:
            filters (list[Filter]): Lista de filtros hijos a evaluar.
            mode (str): Modo de evaluacion ('AND' u 'OR').
        """
        self._filters = filters
        self._mode = mode.upper()

    @property
    def keyword(self) -> str:
        """Retorna una representacion de las palabras clave unidas.

        Returns:
            str: Hileras unidas por coma.
        """
        return ", ".join(f.keyword for f in self._filters)

    def matches(self, message: Message) -> bool:
        """Aplica la logica compuesta sobre los filtros hijos.

        Args:
            message (Message): Mensaje a evaluar.

        Returns:
            bool: True si cumple la condicion logica de grupo, False de lo contrario.
        """
        if not self._filters:
            return False

        if self._mode == "AND":
            return all(f.matches(message) for f in self._filters)
        
        # Modo por defecto: OR.
        return any(f.matches(message) for f in self._filters)
