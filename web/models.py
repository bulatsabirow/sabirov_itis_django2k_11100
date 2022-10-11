from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(AbstractModel):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    count = models.IntegerField()
    price = models.DecimalField(decimal_places=2)


class Status(models.Model):
    status = models.CharField(max_length=20)
