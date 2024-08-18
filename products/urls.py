"""Urls for products app"""

from django.urls import URLPattern, URLResolver, path

from products.views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    CategoryDetailView,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path("categories", CategoryListView.as_view(), name="categories-list"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("", ProductListView.as_view(), name="products-list"),
    path("<int:pk>", ProductDetailView.as_view(), name="product-detail"),
]
