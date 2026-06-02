from django.urls import path

from .views import (
    MenuItemDetailView,
    MenuItemListCreateView,
)

urlpatterns = [
    path(
        "",
        MenuItemListCreateView.as_view(),
        name="menu-list-create",
    ),
    path(
        "<int:pk>/",
        MenuItemDetailView.as_view(),
        name="menu-detail",
    ),
]