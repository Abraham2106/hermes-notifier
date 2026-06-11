import json
import os
import tempfile
from hermes.core.storage import Storage
from hermes.logger import logger

class JsonFileStorage(Storage):
    """Implementacion de persistencia basada en un archivo plano en formato JSON.

    Soporta la carga, guardado y la migracion automatica desde formatos antiguos.
    """

    def __init__(self, file_path: str) -> None:
        """Inicializa la ruta del archivo persistente.

        Args:
            file_path (str): Ruta al archivo JSON.
        """
        self._path = file_path

    def load(self) -> dict[str, set[str]]:
        """Carga y procesa el registro persistente.

        Realiza migracion automatica de listas planas (versiones legacy)
        a un diccionario categorizado por palabras clave.

        Returns:
            dict[str, set[str]]: Diccionario que asocia palabras clave a conjuntos de IDs.
        """
        if not os.path.exists(self._path):
            return {}

        try:
            with open(self._path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                data = json.loads(content)
            
            # Gestionar formatos antiguos (lista plana de IDs).
            if isinstance(data, list):
                return {}
            
            if isinstance(data, dict):
                return {k: set(v) for k, v in data.items() if isinstance(v, list)}
            
            return {}
        except (json.JSONDecodeError, PermissionError) as e:
            logger.error(f"Error al leer/parsear el archivo de persistencia {self._path}: {e}")
            return {}

    def save(self, seen: dict[str, set[str]]) -> None:
        """Guarda el estado del monitor en formato JSON de forma atomica.

        Evita la corrupcion de datos escribiendo primero en un archivo temporal
        y reemplazando el archivo destino de forma atomica.

        Args:
            seen (dict[str, set[str]]): Diccionario con IDs a persistir.
        """
        serializable = {k: list(v) for k, v in seen.items()}
        
        # Obtener el directorio del archivo final
        dir_name = os.path.dirname(os.path.abspath(self._path))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Usar escritura atomica
        temp_fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix="seen_ids_", suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2)
            
            # Establecer permisos restringidos si el OS lo permite (0600: lectura/escritura solo dueño)
            try:
                os.chmod(temp_path, 0o600)
            except AttributeError:
                pass # Ignorar en sistemas que no soporten chmod de estilo Unix completamente (como Windows nativo)

            # Reemplazo atomico
            os.replace(temp_path, self._path)
        except Exception as e:
            logger.error(f"No se pudo guardar atomicamente el archivo de persistencia {self._path}: {e}")
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

