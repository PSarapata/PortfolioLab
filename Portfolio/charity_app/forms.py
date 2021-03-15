from django import forms
from charity_app.models import Donation, Category


class DonationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Donation
        exclude = ['user']
