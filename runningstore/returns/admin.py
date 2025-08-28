from django.contrib import admin
from .models import ReturnRequest, Refund

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ("id","order","order_item","requested_by","status","requested_amount","approved_amount","refunded_amount","created_at")
    list_filter = ("status","created_at")
    search_fields = ("order__id","order_item__id","requested_by__username")

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("id","order","return_request","amount","processed","refund_date")
    list_filter = ("processed","refund_date")
    search_fields = ("order__id",)

# Register your models here.
