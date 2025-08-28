from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product

class CartViewTests(TestCase):
    def setUp(self):
        # Uniform test user
        self.user = User.objects.create_user(
            username="user1",
            email="user1@user.com",
            password="Password123",
        )
        self.client.login(username="user1", password="Password123")

        # Minimal product
        self.cat = Category.objects.create(name="Shoes")
        self.product = Product.objects.create(
            name="Runner Shoe",
            description="Lightweight",
            size="9",
            color="Black",
            price=Decimal("50.00"),
            category=self.cat,
            stock=10,
        )

    def test_cart_summary_renders(self):
        resp = self.client.get(reverse("cart_summary"))
        self.assertEqual(resp.status_code, 200)

    def test_cart_add_returns_qty_json(self):
        resp = self.client.post(
            reverse("cart_add"),
            data={"action": "post", "product_id": self.product.id, "product_qty": 1},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("qty", resp.json())
        self.assertGreaterEqual(int(resp.json()["qty"]), 1)

    def test_cart_update_changes_quantity_json(self):
        self.client.post(
            reverse("cart_add"),
            data={"action": "post", "product_id": self.product.id, "product_qty": 1},
        )
        resp = self.client.post(
            reverse("cart_update"),
            data={"action": "post", "product_id": self.product.id, "product_qty": 3},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp.json()["qty"]), 3)

    def test_cart_delete_returns_product_id_json(self):
        self.client.post(
            reverse("cart_add"),
            data={"action": "post", "product_id": self.product.id, "product_qty": 1},
        )
        resp = self.client.post(
            reverse("cart_delete"),
            data={"action": "post", "product_id": self.product.id},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.json()["product_id"]), str(self.product.id))
# Create your tests here.
