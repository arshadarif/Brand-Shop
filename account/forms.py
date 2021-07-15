from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Customer,Address

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ('username','email','password')

    def clean_email(self):

        email = self.cleaned_data['email']
        if len(User.objects.filter(email=email))>0:
            raise forms.ValidationError('Email already exist')
    
        return email

    def clean_password(self):

        password = self.cleaned_data['password']
        if len(password)<8:
            raise forms.ValidationError('Your password must contain atleast 8 characters')
        
        return password

class PasswordForm(forms.Form):

    password = forms.CharField(widget=PasswordInput)

    def clean_password(self):

        password = self.cleaned_data['password']
        if len(password)<8:
            raise forms.ValidationError('Your password must contain atleast 8 characters')
        
        return password

class AcDetailsForm(forms.ModelForm):

    current_password = forms.CharField(widget=PasswordInput, required=False)
    new_password = forms.CharField(widget=PasswordInput, required=False)
    confirm_password = forms.CharField(max_length=255, required=False)
    
    class Meta:

        model = Customer
        fields = ('first_name','last_name')

    def clean(self):

        cleaned_data = super().clean()
        current_pass = self.cleaned_data.get('current_password')
        new_pass = self.cleaned_data.get('new_password')
        confirm_pass = cleaned_data.get('confirm_password')
        if current_pass and new_pass:
            if len(new_pass)<8:
                raise forms.ValidationError('Password must contain atleast 8 characters')
            elif new_pass != confirm_pass:
                print("password mismatch")
                raise forms.ValidationError('Password Mismatch')
        elif not new_pass and confirm_pass:
            raise forms.ValidationError('Password Mismatch')


        return self.cleaned_data

class AddressForm(forms.ModelForm):

    class Meta:

        model = Address
        fields = ('first_name','last_name','state','street1','street2',
        'city','post_code','phone','email')

    
