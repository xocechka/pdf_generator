from django.apps import AppConfig


class GeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.generator'
    app_label = 'generator'