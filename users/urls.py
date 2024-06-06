from django.urls import path, include
from .views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("list/", UserListView.as_view(), name="users"),
    path("add/", UserCreateView.as_view(), name="user_add"),
    path("profile/", UserUpdateView.as_view(), name="profile"),

    path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_change"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    ]