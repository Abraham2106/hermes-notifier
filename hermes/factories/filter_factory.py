from hermes.core.filter import Filter
from hermes.config import Config
from hermes.filters.keyword import KeywordFilter

class FilterFactory:
    """Fabrica encargada de mapear y construir los filtros de busqueda asignados."""

    @classmethod
    def create(cls, config: Config) -> list[Filter]:
        """Construye una coleccion de filtros basados en las palabras clave configuradas.

        Args:
            config (Config): Objeto de configuracion.

        Returns:
            list[Filter]: Lista de filtros instanciados.
        """
        return [KeywordFilter(keyword) for keyword in config.keywords]
