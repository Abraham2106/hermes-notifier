import time
from hermes.core.source import Source
from hermes.core.notifier import Notifier
from hermes.core.filter import Filter
from hermes.core.storage import Storage
from hermes.logger import logger

class Monitor:
    """Clase principal (Orquestador) que acopla las abstracciones de Hermes.

    Controla el bucle de ejecucion, la deteccion de nuevos mensajes y
    la persistencia del historial para evitar duplicar notificaciones.
    """

    def __init__(
         self,
         source: Source,
         notifiers: list[Notifier],
         filters: list[Filter],
         storage: Storage,
         poll_interval: int,
    ) -> None:
        """Inicializa el monitor con sus componentes y estrategias desacopladas.

        Args:
            source (Source): Fuente de donde se obtienen los mensajes.
            notifiers (list[Notifier]): Destinos de las alertas.
            filters (list[Filter]): Criterios de filtrado a aplicar.
            storage (Storage): Mecanismo de persistencia.
            poll_interval (int): Frecuencia de chequeo en segundos.
        """
        self._source = source
        self._notifiers = notifiers
        self._filters = filters
        self._storage = storage
        self._poll_interval = poll_interval

    def _initialize_seen(self, seen: dict[str, set[str]]) -> None:
        """Pre-carga el historico de los filtros para no disparar alertas masivas al iniciar.

        Args:
            seen (dict[str, set[str]]): Registro en memoria a inicializar.
        """
        total = 0
        for f in self._filters:
            kw = f.keyword
            # Evita duplicados en caso de que ya existan datos.
            if kw not in seen:
                seen[kw] = set()
            
            try:
                # Busca y marca correos preexistentes (maximo 50 por palabra clave).
                messages = list(self._source.fetch(query=kw, max_results=50))
                seen[kw] = {msg.id for msg in messages}
                total += len(seen[kw])
                logger.info(f"  [{kw}] -> {len(seen[kw])} correos existentes marcados como vistos.")
            except Exception as e:
                logger.error(f"No se pudo inicializar la palabra clave '{kw}': {e}")
        
        logger.info(f"Inicializado: {total} correos totales.")

    def run(self) -> None:
        """Inicia el ciclo continuo de ejecucion y monitoreo."""
        logger.info("=" * 50)
        logger.info("  Hermes Notifier - arrancando...")
        logger.info("=" * 50)

        seen = self._storage.load()

        # Asegurar inicializacion de keywords nuevas si el historial esta vacio.
        # O si el almacenamiento no tenia datos de ningun keyword.
        if not seen or all(len(ids) == 0 for ids in seen.values()):
            self._initialize_seen(seen)
            self._storage.save(seen)
            
            # Enviar aviso inicial al canal correspondiente.
            keywords_list = "\n".join(f"  - {f.keyword}" for f in self._filters)
            first_msg = (
                f"[OK] Hermes Notifier iniciado.\n"
                f"Monitoreando {len(self._filters)} keyword(s):\n{keywords_list}"
            )
            for notifier in self._notifiers:
                try:
                    # Enviar el aviso inicial de forma segura sin acceder a campos privados
                    notifier.notify_text(first_msg)
                except Exception as e:
                    logger.error(f"Error al enviar notificacion de inicio: {e}")

        logger.info(f"Keywords activos ({len(self._filters)}):")
        for f in self._filters:
            logger.info(f"  - {f.keyword}")
        logger.info(f"Revisando cada {self._poll_interval}s. Ctrl+C para detener.")

        while True:
            try:
                self._tick(seen)
                self._storage.save(seen)
            except Exception as e:
                logger.error(f"Error durante el escaneo: {e}")
            time.sleep(self._poll_interval)

    def _tick(self, seen: dict[str, set[str]]) -> None:
        """Realiza una iteracion de busqueda sobre todos los filtros.

        Args:
            seen (dict[str, set[str]]): Historial acumulado de IDs vistos.
        """
        for f in self._filters:
            kw = f.keyword
            if kw not in seen:
                seen[kw] = set()

            # Obtener nuevos mensajes desde la fuente.
            for msg in self._source.fetch(query=kw, max_results=10):
                if msg.id not in seen[kw]:
                    # Verificar si coincide y notificar.
                    if f.matches(msg):
                        for notifier in self._notifiers:
                            try:
                                notifier.send(keyword=kw, message=msg)
                            except Exception as e:
                                logger.error(f"Error al enviar notificacion de coincidencia: {e}")
                        seen[kw].add(msg.id)

