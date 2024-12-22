import html5lib
from lxml import etree
from rest_framework import serializers


class HTMLCharField(serializers.CharField):
    def validate_html(self, value):
        """
        Validate the given HTML content.

        Args:
            value (str): The HTML content to validate.

        Returns:
            list: A list of validation errors, if any. An empty list means the HTML is valid.
        """
        errors = []

        # Parse the HTML content using html5lib
        try:
            document = html5lib.parse(value, treebuilder="lxml")
        except Exception as e:
            errors.append(f"HTML parsing error: {e}")
            return errors

        # Convert the parsed document to a string
        serialized_html = etree.tostring(
            document, pretty_print=True, encoding="unicode"
        )

        # Validate the serialized HTML with lxml's HTML parser
        parser = etree.HTMLParser()
        try:
            etree.fromstring(serialized_html, parser)
        except etree.XMLSyntaxError as e:
            errors.append(f"XML syntax error: {e}")

        return errors

    def to_internal_value(self, data):
        """
        Override the to_internal_value method to include HTML validation.
        """
        errors = self.validate_html(data)
        if errors:
            raise serializers.ValidationError(errors)
        return super().to_internal_value(data)


class PdfGenerationPostSerializerV1(serializers.Serializer):
    html = HTMLCharField()
    filename = serializers.CharField(required=False, allow_null=False)
