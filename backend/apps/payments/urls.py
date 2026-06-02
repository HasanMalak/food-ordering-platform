from django.urls import path

from .views import PaymentCreateView

urlpatterns = [
    path(
        "pay/",
        PaymentCreateView.as_view(),
    ),
]