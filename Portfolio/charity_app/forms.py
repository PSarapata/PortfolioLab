from django import forms
from charity_app.models import Donation


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        exclude = ['user']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'quantity': forms.IntegerField(),
            'institution': forms.IntegerField(),
            'address': forms.TextInput(),
            'phone_number': forms.TextInput(),
            'city': forms.TextInput(),
            'zip_code': forms.TextInput(),
            'pick_up_date': forms.DateField(),
            'pick_up_time': forms.TimeField(),
            'pick_up_comment': forms.Textarea(),
        }
