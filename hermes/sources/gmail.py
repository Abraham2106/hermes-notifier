import re
from typing import Iterator
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from hermes.core.source import Source, Message
from hermes.config import Config
from hermes.logger import logger

class GmailSource(Source):
    """Implementacion de la fuente de mensajes basada en Gmail API.

    Usa OAuth2 con refresh token para mantener activa la sesion
    y realiza consultas de busqueda utilizando la sintaxis de Gmail.
    """

    def __init__(self, config: Config) -> None:
        """Inicializa la fuente de Gmail con la configuracion provista.

        Args:
            config (Config): Objeto de configuracion del sistema.
        """
        self._client_id = config.gmail_client_id
        self._client_secret = config.gmail_client_secret
        self._refresh_token = config.gmail_refresh_token
        self._service = self._get_gmail_service()

    def _mask_credential(self, cred: str) -> str:
        """Enmascara parte de un token o credencial secreta para logging seguro.

        Args:
            cred (str): Credencial a enmascarar.

        Returns:
            str: Credencial enmascarada.
        """
        if not cred:
            return ""
        if len(cred) <= 8:
            return "****"
        return f"{cred[:4]}...{cred[-4:]}"

    def _get_gmail_service(self):
        """Inicializa y refresca las credenciales del servicio Gmail.

        Returns:
            Resource: Instancia del servicio de Google API Client para Gmail.
        """
        try:
            creds = Credentials(
                token=None,
                refresh_token=self._refresh_token,
                client_id=self._client_id,
                client_secret=self._client_secret,
                token_uri="https://oauth2.googleapis.com/token",
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            )
            creds.refresh(Request())
            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            masked_client_id = self._mask_credential(self._client_id)
            logger.error(f"Error al autenticar u obtener el servicio de Gmail (Client ID: {masked_client_id}): {e}")
            raise

    def fetch(self, query: str, max_results: int = 10) -> Iterator[Message]:
        """Consulta el buzon de correo de Gmail y retorna mensajes coincidentes.

        Args:
            query (str): Criterio de busqueda de Gmail.
            max_results (int): Limite de mensajes a consultar.

        Returns:
            Iterator[Message]: Iterador conteniendo los mensajes encontrados.
        """
        # Sanitizar entrada del query eliminando caracteres sospechosos que alteren la consulta
        clean_query = re.sub(r'["\\]', '', query).strip()
        if not clean_query:
            return

        try:
            results = self._service.users().messages().list(
                userId="me", q=clean_query, maxResults=max_results
            ).execute()
        except Exception as e:
            logger.error(f"Error al consultar la API de Gmail para la consulta '{clean_query}': {e}")
            return

        messages = results.get("messages", [])
        for msg in messages:
            try:
                full = self._service.users().messages().get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["Subject", "From"],
                ).execute()
                
                headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
                subject = headers.get("Subject", "(sin asunto)")
                sender = headers.get("From", "(desconocido)")
                
                yield Message(id=msg["id"], sender=sender, subject=subject)
            except Exception as e:
                logger.error(f"Error al obtener detalles del mensaje {msg.get('id')}: {e}")

    def name(self) -> str:
        """Retorna el nombre identificador de esta fuente.

        Returns:
            str: Identificador 'gmail'.
        """
        return "gmail"

