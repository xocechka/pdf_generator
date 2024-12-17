from rest_framework.routers import DefaultRouter
from apps.generator.api import views


router = DefaultRouter()
router.register("generate", views.GeneratorView, basename="generator")

urlpatterns = router.urls