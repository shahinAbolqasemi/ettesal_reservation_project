from django.apps import AppConfig


class ReservationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation_app'

    def ready(self):
        import reservation_app.signals
