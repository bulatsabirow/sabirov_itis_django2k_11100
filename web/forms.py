from django import forms

from web.validators import phone_validator


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField()
    phone = forms.CharField(validators=[phone_validator])
    birthdate = forms.DateField(widget=forms.SelectDateWidget())

