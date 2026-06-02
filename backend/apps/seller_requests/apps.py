from django.apps import AppConfig


class SellerRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.seller_requests"

    def ready(self):
        import apps.seller_requests.signals