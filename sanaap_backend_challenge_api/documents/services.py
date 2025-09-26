from sanaap_backend_challenge_api.documents import exceptions


class DocumentService:
    def __init__(self, document_model):
        self.document_model = document_model

    def create_document(self, title, content):
        try:
            document = self.document_model.objects.create(title=title, content=content)
            return document
        except Exception as e:
            print(f"Error creating document: {e}")
            raise exceptions.FailedToCreateDocument() from e
