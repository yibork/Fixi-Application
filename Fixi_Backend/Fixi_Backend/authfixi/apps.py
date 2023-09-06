from django.apps import AppConfig


class AuthfixiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Fixi_Backend.authfixi'
    verbose_name = ("Auth")
    def ready(self):
        try:
            import Fixi_Backend.users.signals  # noqa: F401
        except ImportError:
            pass


