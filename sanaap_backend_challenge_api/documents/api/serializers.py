from rest_framework import serializers


class DocumentRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.ImageField(use_url=False, write_only=True)


class DocumentUpdateRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)


class DocumentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    uploaded_at = serializers.DateTimeField()
