from django.urls import path

from .views import SellerRequestListCreateView

urlpatterns = [
    path(
        "",
        SellerRequestListCreateView.as_view(),
        name="seller-request-list-create",
    ),
]