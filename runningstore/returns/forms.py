from django import forms
from .models import ReturnRequest

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ["order_item", "reason", "requested_amount"]

class StaffDecisionForm(forms.ModelForm):
    approve = forms.BooleanField(required=False, help_text="Tick to approve, untick to reject.")
    class Meta:
        model = ReturnRequest
        fields = ["approved_amount"]