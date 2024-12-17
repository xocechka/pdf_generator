from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

swagger = [
    # Swagger drf-spectacular
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

api = {
    "v1": [
        path("v1/", include(swagger)),
        path("v1/", include("apps.generator.api.views.urls.v1"), name="generator"),
    ]
}

urlpatterns = [path("api/", include((api[k], k))) for k in api]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
