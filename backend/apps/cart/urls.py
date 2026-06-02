from django.urls import path

from .views import (
    AddToCartView,
    CartDetailView,
)

urlpatterns = [
    path(
        "add/",
        AddToCartView.as_view(),
        name="add-to-cart",
    ),

    path(
        "",
        CartDetailView.as_view(),
        name="cart-detail",
    ),
]