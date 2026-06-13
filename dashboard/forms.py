from django import forms
from events.models import RaffleEvent


class SMSForm(forms.Form):

    event = forms.ModelChoiceField(
        queryset=RaffleEvent.objects.filter(status="ACTIVE")
    )

    phone_number = forms.CharField(max_length=20)

    sms_text = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 6,
            "placeholder": "Paste M-Pesa SMS here..."
        })
    )