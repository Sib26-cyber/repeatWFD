from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):

    shipping_full_name = forms.CharField(label="Full Name",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'full name'}), required=False)
    shipping_email = forms.CharField(label="Email",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}), required=False)
    shipping_address_line1 = forms.CharField(label="shipping address line 1",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address line 1'}), required=False)
    shipping_address_line2 = forms.CharField(label="shipping address line 2",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address line 2'}), required=False) 
    shipping_city = forms.CharField(label="City",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    shipping_state = forms.CharField(label="State",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    shipping_postal_code = forms.CharField(label="postal Code",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'postal code'}), required=False)
    shipping_country = forms.CharField(label="Country",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'country'}), required=False)




    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address_line1', 'shipping_address_line2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']

        exclude = ['user',]
        
    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="Full Name",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}), required=False)
    card_number = forms.CharField(label="Card Number",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=False)
    card_expiry_date =forms.CharField(label="Expiry Date",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'MM/YY'}), required=False)
    card_cvv_number = forms.CharField(label="CVV",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV'}), required=False)  
    card_address_line1 = forms.CharField(label="shipping address line 1",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address line 1'}), required=False)
    card_address_line2 = forms.CharField(label="shipping address line 2",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address line 2'}), required=False)    
    card_city = forms.CharField(label="City",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)  
    card_state = forms.CharField(label="State",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    card_postal_code = forms.CharField(label="postal Code",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'postal code'}), required=False)
    card_country =forms.CharField(label="Country",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'country'}), required=False)