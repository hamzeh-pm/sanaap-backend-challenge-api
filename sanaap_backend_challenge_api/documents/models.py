from datetime import datetime
import os
import random

from django.db import models


def document_upload_path(instance, filename):
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    today = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%H%M%S")
    random_part = random.randint(100000, 999999)
    return os.path.join("documents", today, f"{timestamp}_{random_part}.{ext}")


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.ImageField(upload_to=document_upload_path)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
