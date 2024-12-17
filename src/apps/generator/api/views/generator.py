from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.generator.gateway.serializers.v1.generator import PdfGenerationPostSerializerV1


@extend_schema_view(
    generate = extend_schema(
        tags="Generator",
        description="Generate a pdf file",
        summary="Generate a pdf file",
        responses={
            200: {
                "type": "object",
            }
        },
    )
)
class GeneratorView(GenericViewSet):
    queryset = None
    pagination_class = None

    serializer_class = PdfGenerationPostSerializerV1

    def list(self, request, *args, **kwargs):
        return Response("Hello World")

    @decorators.action(
        detail=False,
        methods=['post'],
        url_path='generate',
        url_name='generate',
    )
    def generate(self, request, *args, **kwargs):
        pass