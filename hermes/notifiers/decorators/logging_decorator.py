import time
from hermes.core.source import Message
from hermes.notifiers.decorators.base import NotifierDecorator
from hermes.logger import logger

class LoggingNotifierDecorator(NotifierDecorator):
    """Decorator that logs detailed information about notification sending."""

    def send(self, keywords: list[str], message: Message) -> None:
        start_time = time.time()
        logger.debug(f"[{self._wrapped.__class__.__name__}] Sending message '{message.id}' for keywords '{', '.join(keywords)}'")
        try:
            self._wrapped.send(keywords, message)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"[{self._wrapped.__class__.__name__}] Successfully sent message '{message.id}' in {elapsed:.2f}ms")
        except Exception as e:
            logger.error(f"[{self._wrapped.__class__.__name__}] Failed to send message '{message.id}': {e}", exc_info=True)
            raise

    def send_similar_batch(self, batch: list[tuple[Message, list[str]]]) -> None:
        start_time = time.time()
        logger.debug(f"[{self._wrapped.__class__.__name__}] Sending batch of {len(batch)} similar messages")
        try:
            self._wrapped.send_similar_batch(batch)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"[{self._wrapped.__class__.__name__}] Successfully sent similar batch in {elapsed:.2f}ms")
        except Exception as e:
            logger.error(f"[{self._wrapped.__class__.__name__}] Failed to send similar batch: {e}", exc_info=True)
            raise

    def notify_text(self, text: str) -> None:
        logger.debug(f"[{self._wrapped.__class__.__name__}] Sending text notification: '{text[:50]}...'")
        try:
            self._wrapped.notify_text(text)
        except Exception as e:
            logger.error(f"[{self._wrapped.__class__.__name__}] Failed to send text notification: {e}", exc_info=True)
            raise
