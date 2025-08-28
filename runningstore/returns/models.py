from django.db import models
from django.conf import settings
from payment.models import Order, OrderItem

# Create your models here.
class ReturnsStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    APPROVED = "APPROVED","Approved"
    RECEIVED = "RECEIVED","Received"
    REFUNDED = "REFUNDED", "Refunded"
    REJECTED = "REJECTED", "Rejected"
    
    
class ReturnRequest(models.Model):
    order = model.ForeignKey(Order, on_delete=models.Cascade, related_name="return_requests")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="return_requests")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices= ReturnStatus.choices, default= ReturnStatus.REQUESTED)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Return {self.pk} • Order {self.order_id} • {self.status}"