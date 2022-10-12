from django import forms

from web.models import Product
from web.validators import phone_validator


class AuthorizationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(AuthorizationForm):
    name = forms.CharField()
    phone = forms.CharField(validators=[phone_validator])
    birthdate = forms.DateField(widget=forms.SelectDateWidget())


class ProductForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        return super().save(*args, **kwargs)

    class Meta:
        model = Product
        fields = ('name', 'description', 'photo', 'price')
        labels = {'name': 'Название товара',
                  'description': 'Описание',
                  'photo': 'Изображение',
                  'price': 'Цена',
                  }
        widgets = {
            'price': forms.NumberInput(),
        }



