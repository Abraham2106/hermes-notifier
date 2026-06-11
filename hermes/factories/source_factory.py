from hermes.core.source import Source
from hermes.config import Config
from hermes.sources.gmail import GmailSource

class SourceFactory:
    """Fabrica encargada de crear instancias concretas de la interfaz Source."""

    _registry: dict[str, type[Source]] = {}

    @classmethod
    def register(cls, name: str, klass: type[Source]) -> None:
        """Registra una clase Source bajo un nombre identificador.

        Args:
            name (str): Nombre clave para el registro.
            klass (type[Source]): Clase a registrar.
        """
        cls._registry[name.lower()] = klass

    @classmethod
    def create(cls, config: Config) -> Source:
        """Instancia y retorna la fuente configurada.

        Actualmente por defecto retorna GmailSource, permitiendo
        extensiones futuras basadas en variables de entorno.

        Args:
            config (Config): Objeto de configuracion.

        Returns:
            Source: Instancia concreta que implementa Source.
        """
        # Por defecto implementa 'gmail'.
        source_type = "gmail"
        klass = cls._registry.get(source_type)
        if not klass:
            raise ValueError(f"Fuente no soportada o registrada: {source_type}")
        return klass(config)

# Auto-registro inicial de las fuentes del sistema.
SourceFactory.register("gmail", GmailSource)
