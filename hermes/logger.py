import logging
import sys

def setup_logger() -> logging.Logger:
    """Configura el sistema de logging para la aplicacion.

    Returns:
        logging.Logger: Objeto logger configurado para el sistema.
    """
    logger = logging.getLogger("hermes")
    
    # Evitar duplicar handlers en inicializaciones consecutivas.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    
    # Handler para la salida estandar limpia y formateada.
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Instancia global para ser utilizada en todo el paquete.
logger = setup_logger()
