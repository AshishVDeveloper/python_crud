from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product",
            description="Initial product",
            price=Decimal("100.00"),
            quantity=10,
        )

    def test_list_products_is_paginated(self):
        response = self.client.get(reverse("product-list-create-api"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)

    def test_create_product(self):
        response = self.client.post(
            reverse("product-list-create-api"),
            {
                "name": "New Product",
                "description": "Created using API",
                "price": "250.50",
                "quantity": 5,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="New Product").exists())

    def test_duplicate_product_name_is_rejected_case_insensitively(self):
        response = self.client.post(
            reverse("product-list-create-api"),
            {
                "name": "test product",
                "description": "Duplicate",
                "price": "10.00",
                "quantity": 1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_update_product(self):
        response = self.client.put(
            reverse("product-detail-api", kwargs={"pk": self.product.pk}),
            {
                "name": "Updated Product",
                "description": "Updated",
                "price": "150.00",
                "quantity": 20,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_delete_product(self):
        response = self.client.delete(
            reverse("product-detail-api", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_negative_values_are_rejected(self):
        response = self.client.post(
            reverse("product-list-create-api"),
            {
                "name": "Invalid Product",
                "description": "Invalid",
                "price": "-1.00",
                "quantity": -1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)
        self.assertIn("quantity", response.data)
