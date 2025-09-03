from django.db import models
from django.conf import settings

from payment.models import Order, OrderItem

class ReturnStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    APPROVED  = "APPROVED",  "Approved"
    RECEIVED  = "RECEIVED",  "Item(s) received"
    REFUNDED  = "REFUNDED",  "Refunded"
    REJECTED  = "REJECTED",  "Rejected"

class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="return_requests")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="return_requests")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ReturnStatus.choices, default=ReturnStatus.REQUESTED)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Return {self.pk} • Order {self.order_id} • {self.status}"# Create your models here.


class Refund(models.Model):
    """Mock refund record — no payment gateway involved."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refunds")
    return_request = models.OneToOneField(ReturnRequest, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True)
    refund_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund {self.pk} • Order {self.order_id} • €{self.amount}"