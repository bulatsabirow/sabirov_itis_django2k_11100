from datetime import date

from django import forms

from web.models import Product, Category
from web.validators import phone_validator


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.category



class AuthorizationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(AuthorizationForm):
    name = forms.CharField()
    phone = forms.CharField(validators=[phone_validator])
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year+1)))


class ProductForm(forms.ModelForm):
    category_id = CategoryChoiceField(queryset=Category.objects.all(),
                                      to_field_name='category',
                                      label='Категория')

    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        return super().save(*args, **kwargs)

    class Meta:
        model = Product
        fields = ('name', 'description', 'photo', 'price', 'count')
        labels = {'name': 'Название товара',
                  'description': 'Описание',
                  'photo': 'Изображение',
                  'price': 'Цена',
                  'count': 'Количество',
                  'category': 'Категория',
                  }
        widgets = {
            'price': forms.NumberInput(),
            'photo': forms.FileInput(),
            'count': forms.NumberInput(),
        }



