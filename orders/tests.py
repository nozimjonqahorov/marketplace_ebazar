from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Category, Product
from orders.models import Order


class OrderTotalsTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.buyer = User.objects.create_user(
            username="buyer1",
            password="pass",
            role="buyer",
            email="buyer1@example.com",
        )
        self.seller = User.objects.create_user(
            username="seller1",
            password="pass",
            role="seller",
            email="seller1@example.com",
        )

        self.category = Category.objects.create(name="cat")

        self.product = Product.objects.create(
            author=self.seller,
            category=self.category,
            title="Product 1",
            description="desc",
            price=Decimal("50000.00"),
            quantity=10,
            address="addr",
            condition="new",
            is_active=True,
        )

    def test_buyer_total_expense_completed_only(self):
        # completed should count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=1,
            total_price=Decimal("1000.00"),
            status="completed",
        )
        # accepted should NOT count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=2,
            total_price=Decimal("2000.00"),
            status="accepted",
        )
        # canceled should NOT count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=3,
            total_price=Decimal("3000.00"),
            status="canceled",
        )

        self.client.force_login(self.buyer)
        response = self.client.get(reverse("my_orders"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_expense"], 1000)

    def test_my_orders_can_be_filtered_by_status(self):
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=1,
            total_price=Decimal("1000.00"),
            status="new",
        )
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=2,
            total_price=Decimal("2000.00"),
            status="accepted",
        )
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=3,
            total_price=Decimal("3000.00"),
            status="completed",
        )

        self.client.force_login(self.buyer)
        response = self.client.get(reverse("my_orders"), {"status": "accepted"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_status"], "accepted")
        self.assertEqual(response.context["filtered_orders_count"], 1)
        self.assertEqual(list(response.context["orders"].values_list("status", flat=True)), ["accepted"])
        self.assertEqual(response.context["total_orders"], 3)

    def test_seller_total_income_completed_only(self):
        # completed should count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=1,
            total_price=Decimal("111.00"),
            status="completed",
        )
        # accepted should NOT count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=1,
            total_price=Decimal("222.00"),
            status="accepted",
        )
        # canceled should NOT count
        Order.objects.create(
            product=self.product,
            buyer=self.buyer,
            seller=self.seller,
            quantity=1,
            total_price=Decimal("333.00"),
            status="canceled",
        )

        self.client.force_login(self.seller)
        response = self.client.get(reverse("seller_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_income"], 111)
