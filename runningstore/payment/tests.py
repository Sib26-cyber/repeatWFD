from django.test import TestCase
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from payment.models import ShippingAddress, Order, OrderItem  # <- singular 'payment'
from store.models import Category, Product

class PaymentFlowTests(TestCase):
    def setUp(self):
        # Uniform test user
        self.user = User.objects.create_user(
            username="user1",
            email="user1@user.com",
            password="Password123",
        )
        self.client.login(username="user1", password="Password123")

        # Product
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

        # Add to cart via cart view
        self.client.post(
            reverse("cart_add"),
            data={"action": "post", "product_id": self.product.id, "product_qty": 1},
        )

        # Shipping payload used by billing_info -> stored in session
        self.shipping_post = {
            "shipping_full_name": "Test User",
            "shipping_email": "user1@user.com",
            "shipping_address_line1": "123 Test St",
            "shipping_address_line2": "",
            "shipping_city": "Dublin",
            "shipping_state": "",
            "shipping_postal_code": "D01",
            "shipping_country": "Ireland",
        }

    def test_payment_success_renders(self):
        resp = self.client.get(reverse("payment_success"))
        self.assertEqual(resp.status_code, 200)

    def test_billing_info_sets_session_and_renders(self):
        resp = self.client.post(reverse("billing_info"), data=self.shipping_post)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("my_shipping", self.client.session)
        self.assertEqual(self.client.session["my_shipping"]["shipping_full_name"], "Test User")

    def test_checkout_renders_with_user_shipping(self):
        # Ensure a ShippingAddress exists (signal may create one; this guarantees it)
        ShippingAddress.objects.get_or_create(
            shipping_user=self.user,
            defaults={
                "shipping_full_name": "Test User",
                "shipping_email": "user1@user.com",
                "shipping_address_line1": "123 Test St",
                "shipping_city": "Dublin",
                "shipping_country": "Ireland",
            },
        )
        resp = self.client.get(reverse("checkout"))
        self.assertEqual(resp.status_code, 200)

    def test_process_order_creates_order_and_items(self):
        # Ensure billing_info populated session
        self.client.post(reverse("billing_info"), data=self.shipping_post)

        # Process order (your view redirects to 'home')
        resp = self.client.post(reverse("process_order"), data={"action": "post"})
        self.assertEqual(resp.status_code, 302)

        # Verify Order + OrderItem created for this user
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.filter(user=self.user).latest("id")
        self.assertTrue(OrderItem.objects.filter(order=order).exists())

        oi = OrderItem.objects.filter(order=order).first()
        self.assertEqual(oi.product, self.product)
        self.assertEqual(int(oi.quantity), 1)