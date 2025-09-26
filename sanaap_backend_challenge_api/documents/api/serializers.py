from rest_framework import serializers


class DocumentRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.ImageField(use_url=False, write_only=True)


class DocumentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    content_url = serializers.CharField(source="content.url")
