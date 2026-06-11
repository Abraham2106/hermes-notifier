from hermes.core.notifier import Notifier
from hermes.config import Config
from hermes.notifiers.telegram import TelegramNotifier

class NotifierFactory:
    """Fabrica encargada de instanciar y retornar los canales de notificacion activos."""

    _registry: dict[str, type[Notifier]] = {}

    @classmethod
    def register(cls, name: str, klass: type[Notifier]) -> None:
        """Registra un notificador asociado a un canal especifico.

        Args:
            name (str): Canal de notificacion.
            klass (type[Notifier]): Clase notificador.
        """
        cls._registry[name.lower()] = klass

    @classmethod
    def create(cls, config: Config) -> list[Notifier]:
        """Crea e inicializa la lista de notificadores basados en la configuracion.

        Args:
            config (Config): Objeto de configuracion.

        Returns:
            list[Notifier]: Lista de notificadores listos para operar.
        """
        # Actualmente por defecto se inicializa Telegram.
        active_channels = ["telegram"]
        notifiers = []
        for channel in active_channels:
            klass = cls._registry.get(channel)
            if klass:
                notifiers.append(klass(config))
        return notifiers

# Auto-registro inicial de notificadores.
NotifierFactory.register("telegram", TelegramNotifier)
