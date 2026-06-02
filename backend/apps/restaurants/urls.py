from django.urls import path

from .views import (
    RestaurantCreateView,
    MyRestaurantView,
)

urlpatterns = [
    path(
        "",
        RestaurantCreateView.as_view(),
        name="restaurant-create",
    ),

    path(
        "me/",
        MyRestaurantView.as_view(),
        name="my-restaurant",
    ),
]