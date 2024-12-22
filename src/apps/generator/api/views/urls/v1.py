from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.generator.api import views

router = DefaultRouter()
router.register("", views.GeneratorViewV1, basename="generator")

urlpatterns = router.urls