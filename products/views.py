from django.shortcuts import render
from rest_framework import generics

from .models import Product
from .pagination import ProductPagination
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated


# -----------------------------------------------------------------------------
# Browser pages
# -----------------------------------------------------------------------------
def login_page(request):
    return render(request, "products/login.html")

def product_list_page(request):
    """Render the product list page. Data is loaded from the REST API."""
    return render(request, "products/list.html")


def product_add_page(request):
    """Render the add-product form."""
    return render(
        request,
        "products/form.html",
        {"mode": "add", "product_id": None},
    )


def product_edit_page(request, pk):
    """Render the edit-product form. Existing data is loaded from the REST API."""
    return render(
        request,
        "products/form.html",
        {"mode": "edit", "product_id": pk},
    )


# -----------------------------------------------------------------------------
# REST API
# -----------------------------------------------------------------------------

class ProductListCreateAPIView(generics.ListCreateAPIView):
    
    """
    GET  /api/products/       -> paginated product list
    POST /api/products/       -> create a product
    """
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/products/<id>/ -> retrieve one product
    PUT    /api/products/<id>/ -> full update
    PATCH  /api/products/<id>/ -> partial update
    DELETE /api/products/<id>/ -> delete
    """
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
