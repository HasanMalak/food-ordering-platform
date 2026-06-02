from django.urls import path

from .views import (
    SellerOrdersView,
    SellerOrderStatusView,
    SellerSummaryView,
)

urlpatterns = [
    path(
        "seller/orders/",
        SellerOrdersView.as_view(),
    ),

    path(
        "seller/orders/<int:pk>/status/",
        SellerOrderStatusView.as_view(),
    ),

    path(
        "seller/summary/",
        SellerSummaryView.as_view(),
    ),
]