import aio_pika
from hydromill.message.message import Message

TRACEPARENT = "traceparent"


class Marshaler:
    def __init__(
        self,
        not_persistent_delivery_mode: bool = False,
    ):
        self.not_persistent_delivery_mode = not_persistent_delivery_mode

    def marshal(self, msg: Message) -> aio_pika.Message:
        """ """
        publishing = aio_pika.Message(
            body=msg.payload,
            headers=msg.metadata,
        )

        if not self.not_persistent_delivery_mode:
            publishing.delivery_mode = aio_pika.DeliveryMode.PERSISTENT

        self.postprocess_publishing(publishing)

        return publishing

    def unmarshal(self, msg: aio_pika.IncomingMessage) -> Message:
        """ """
        message = Message(
            payload=msg.body,
            metadata=msg.headers,
        )

        return message

    def postprocess_publishing(
        self,
        publishing: aio_pika.Message,
    ) -> aio_pika.Message:
        """ """
        publishing.app_id = publishing.headers.pop("app_id", publishing.app_id)
        publishing.content_encoding = publishing.headers.pop(
            "content_encoding", publishing.content_encoding
        )
        publishing.content_type = publishing.headers.pop(
            "content_type", publishing.content_type
        )
        publishing.expiration = publishing.headers.pop(
            "expiration", publishing.expiration
        )
        publishing.correlation_id = publishing.headers.pop(
            "correlation_id", publishing.correlation_id
        )
        publishing.message_id = publishing.headers.pop(
            "message_id", publishing.message_id
        )
        publishing.priority = publishing.headers.pop("priority", publishing.priority)
        publishing.reply_to = publishing.headers.pop("reply_to", publishing.reply_to)
        publishing.timestamp = publishing.headers.pop("timestamp", publishing.timestamp)
        publishing.type = publishing.headers.pop("type", publishing.type)
        publishing.user_id = publishing.headers.pop("user_id", publishing.user_id)

        try:
            import elasticapm
        except ModuleNotFoundError:
            return publishing

        if TRACEPARENT not in publishing.headers:
            traceparent = elasticapm.get_trace_parent_header()
            if traceparent is not None:
                publishing.headers[TRACEPARENT] = traceparent

        return publishing
