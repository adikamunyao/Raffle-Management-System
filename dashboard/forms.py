from django import forms
from events.models import RaffleEvent


class SMSForm(forms.Form):

    event = forms.ModelChoiceField(
        queryset=RaffleEvent.objects.none(),
        empty_label="-- Select Event --"
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "e.g. 0712345678"})
    )

    sms_text = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 6,
            "placeholder": "Paste M-Pesa SMS here..."
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event"].queryset = RaffleEvent.objects.filter(status=RaffleEvent.ACTIVE)