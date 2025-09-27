from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class DocumentPublisher:
    def __init__(self):
        self.channel_layer = get_channel_layer()
        self.group_name = "documents"

    def publish_document_created(self, document_id, document_title):
        message = {
            "type": "document_created",
            "data": {
                "message": f"Document '{document_title}' created with ID {document_id}."
            },
        }
        async_to_sync(self.channel_layer.group_send)(self.group_name, message)
