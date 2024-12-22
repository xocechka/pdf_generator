import uuid

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import renderers, status, viewsets, decorators
from rest_framework.response import Response
from weasyprint import HTML

from apps.generator.gateway.serializers.v1.generator import (
    PdfGenerationPostSerializerV1,
)


class PDFRenderer(renderers.BaseRenderer):
    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Retrieve HTML content from the data
        html_content = data.get("html", "")
        # Generate PDF from HTML content using WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf()
        return pdf_file


@extend_schema_view(
    generate=extend_schema(
        tags=["Generation"],
        description="Generate a pdf file",
        summary="Generate a pdf file",
        responses={
            200: OpenApiResponse(response=OpenApiTypes.BINARY, description="PDF file")
        },
    )
)
class GeneratorViewV1(viewsets.GenericViewSet):
    queryset = None
    pagination_class = None
    renderer_classes = [PDFRenderer]
    serializer_class = PdfGenerationPostSerializerV1

    @decorators.action(
        url_path="generate",
        methods=("post",),
        detail=False,
        description="Generate a pdf file",
        url_name="generator",
    )
    def generate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename = serializer.validated_data.get("filename", uuid.uuid4())

        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK,
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": f'inline; filename="{filename}.pdf"',
            },
        )
