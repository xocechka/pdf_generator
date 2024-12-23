import uuid

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from apps.generator.gateway.serializers import PdfGenerationSerializer


class PDFRenderer(renderers.BaseRenderer):
    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Retrieve HTML content from the data
        html_content = data.get("html", "")
        # Generate PDF from HTML content using WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf()
        return pdf_file



class GeneratorAPIView(APIView):
    renderer_classes = [PDFRenderer]

    @extend_schema(
        tags=["Generation"],
        description="Generate a pdf file",
        summary="Generate a pdf file",
        responses={
            200: OpenApiResponse(response=OpenApiTypes.BINARY, description="PDF file")
        },
    )
    def post(self, request, *args, **kwargs):

        serializer = PdfGenerationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK,
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": f'inline; filename="{uuid.uuid4()}.pdf"',
            },
        )
