from django.apps import AppConfig


class AppAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests.app'
    app_label = "app"