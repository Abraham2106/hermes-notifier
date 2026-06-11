from hermes.core.notifier import Notifier
from hermes.config import Config
from hermes.notifiers.telegram import TelegramNotifier
from hermes.notifiers.decorators import (
    RetryNotifierDecorator,
    SanitizingNotifierDecorator,
    LoggingNotifierDecorator
)

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
                notifier = klass(config)
                
                # Aplicar decoradores segun configuracion
                if getattr(config, "use_sanitizing", True):
                    max_len = getattr(config, "sanitizing_max_length", 4000)
                    notifier = SanitizingNotifierDecorator(notifier, max_length=max_len)
                    
                if getattr(config, "use_retry", True):
                    attempts = getattr(config, "retry_max_attempts", 3)
                    delay = getattr(config, "retry_delay", 5)
                    notifier = RetryNotifierDecorator(notifier, max_attempts=attempts, base_delay=delay)
                    
                if getattr(config, "use_logging", True):
                    notifier = LoggingNotifierDecorator(notifier)
                    
                notifiers.append(notifier)
        return notifiers

# Auto-registro inicial de notificadores.
NotifierFactory.register("telegram", TelegramNotifier)
