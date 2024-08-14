""" This file contains the URL patterns for the users app. """

from django.urls import URLPattern, URLResolver, path

from users.views import (
    UserListView,
    UserDetailView,
    SignupView,
    LoginView,
    AddressListView,
    AddressDetailView,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("address/", AddressListView.as_view(), name="address-list"),
    path("address/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
]
