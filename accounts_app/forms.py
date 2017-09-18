from django import forms
from .models import Transaction

class PaymentForm(forms.ModelForm):
    """
    A form for a Transaction
    """
    class Meta:
        model = Transaction
        fields = ['from_account', 'to_account', 'amount_transferred']