from hermes.core.source import Message
from hermes.notifiers.decorators.base import NotifierDecorator

class SanitizingNotifierDecorator(NotifierDecorator):
    """Decorator that sanitizes message content before sending."""

    def __init__(self, inner_notifier, max_length: int = 4000):
        super().__init__(inner_notifier)
        self.max_length = max_length

    def _sanitize_string(self, text: str) -> str:
        if not text:
            return ""
        # Remove null bytes
        text = text.replace('\x00', '')
        # Truncate
        if len(text) > self.max_length:
            text = text[:self.max_length] + "..."
        return text.strip()

    def send(self, keywords: list[str], message: Message) -> None:
        """Sanitizes message fields before sending."""
        sanitized_msg = Message(
            id=message.id,
            sender=self._sanitize_string(message.sender),
            subject=self._sanitize_string(message.subject),
            body=self._sanitize_string(message.body)
        )
        self._wrapped.send(keywords, sanitized_msg)

    def send_similar_batch(self, batch: list[tuple[Message, list[str]]]) -> None:
        sanitized_batch = []
        for msg, kws in batch:
            sanitized_msg = Message(
                id=msg.id,
                sender=self._sanitize_string(msg.sender),
                subject=self._sanitize_string(msg.subject),
                body=self._sanitize_string(msg.body)
            )
            sanitized_batch.append((sanitized_msg, kws))
        self._wrapped.send_similar_batch(sanitized_batch)

    def notify_text(self, text: str) -> None:
        self._wrapped.notify_text(self._sanitize_string(text))
