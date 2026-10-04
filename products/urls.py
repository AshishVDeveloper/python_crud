from django.urls import path

from .views import (
    ProductDetailAPIView,
    ProductListCreateAPIView,
    product_add_page,
    product_edit_page,
    product_list_page,
    login_page,
)

urlpatterns = [
    # Login page
    path("login/", login_page, name="login"),

    # Browser pages
    path("products/", product_list_page, name="product-list-page"),
    path("products/add/", product_add_page, name="product-add-page"),
    path("products/<int:pk>/edit/", product_edit_page, name="product-edit-page"),

    # REST API
    path(
        "api/products/",
        ProductListCreateAPIView.as_view(),
        name="product-list-create-api",
    ),
    path(
        "api/products/<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="product-detail-api",
    ),
]