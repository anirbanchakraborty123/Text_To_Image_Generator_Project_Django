from rest_framework import serializers

class ImageRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=255)
    image  = serializers.URLField()