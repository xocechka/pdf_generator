from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

swagger = [
    # Swagger drf-spectacular
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

api = [
    path("", include(swagger)),
    path("", include("apps.generator.api.urls"), name="generator"),
]

urlpatterns = [swagger + api]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path("", include(swagger))]
