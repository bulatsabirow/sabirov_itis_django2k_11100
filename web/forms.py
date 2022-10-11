from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField()
    phone = forms.CharField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget())

