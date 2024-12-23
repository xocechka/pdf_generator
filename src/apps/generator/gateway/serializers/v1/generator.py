import html5lib
from lxml import etree
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions


class HTMLValidator:
    message = _('Invalid HTML document.')
    code = 'invalid_html_document'

    def __call__(self, value):
        try:
            document = html5lib.parse(value, treebuilder="lxml")
            serialized_html = etree.tostring(
                document, pretty_print=True, encoding="unicode"
            )
            parser = etree.HTMLParser()
            etree.fromstring(serialized_html, parser)
        except Exception as e:
            raise exceptions.ValidationError(self.message, code=self.code) from e


class PdfGenerationPostSerializerV1(serializers.Serializer):
    html = serializers.CharField(validators=[HTMLValidator()])
    context = serializers.JSONField(required=False)