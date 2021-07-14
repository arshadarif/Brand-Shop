from django import forms
from .models import CheckOut

class CheckOutForm(forms.ModelForm):

    class Meta:

        model = CheckOut
        fields = ('first_name','last_name','state','street1','street2',
        'city','post_code','phone','email')