from rest_framework import serializers


class PdfGenerationPostSerializerV1(serializers.Serializer):
    html = serializers.CharField()