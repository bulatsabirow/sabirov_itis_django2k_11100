from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from web.enums import StatusEnum, Role, Category


# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    role = models.CharField(choices=Role.choices, max_length=15, default=Role.user)
    name = models.CharField(max_length=500, null=True, blank=True)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)

    @property
    def is_staff(self):
        return self.role in (Role.staff, Role.admin)

    @property
    def is_superuser(self):
        return self.role == Role.admin

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class PickupPoint(models.Model):
    address = models.CharField(max_length=500)
    locality = models.CharField(max_length=500)

    class Meta:
        unique_together = ('address', 'locality',)


class Product(AbstractModel):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(null=True, max_length=100, choices=Category.choices)


class Order(AbstractModel):
    status = models.CharField(max_length=15, choices=StatusEnum.choices,
                              default=StatusEnum.in_warehouse)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL,
                                     null=True)
    updated_at = None
