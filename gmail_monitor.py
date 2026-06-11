from hermes.config import Config
from hermes.factories.source_factory import SourceFactory
from hermes.factories.notifier_factory import NotifierFactory
from hermes.factories.filter_factory import FilterFactory
from hermes.storage.json_file import JsonFileStorage
from hermes.monitor import Monitor

def main() -> None:
    """Punto de entrada principal para ejecutar el monitor Hermes."""
    # Cargar y validar configuracion.
    config = Config.from_env()

    # Construir componentes modulares mediante fabricas.
    source = SourceFactory.create(config)
    notifiers = NotifierFactory.create(config)
    filters = FilterFactory.create(config)
    storage = JsonFileStorage(config.seen_file)

    # Orquestar ejecucion.
    monitor = Monitor(
        source=source,
        notifiers=notifiers,
        filters=filters,
        storage=storage,
        poll_interval=config.poll_interval,
    )
    monitor.run()


if __name__ == "__main__":
    main()
