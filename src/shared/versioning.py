from dauto.drf.versioning import CustomNamespaceVersioning


class SharpVersioning(CustomNamespaceVersioning):
    separator = "#"
