from django.urls import path

from apps.generator.api import views

urlpatterns = [
    path("generate", views.GeneratorAPIView.as_view(), name="generate"),
]
