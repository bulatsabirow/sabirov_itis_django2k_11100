from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from web.enums import StatusEnum, Role


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
    is_seller = models.BooleanField(default=False)
    birthdate = models.DateTimeField()
    phone = models.CharField(max_length=20, unique=True)

    @property
    def is_staff(self):
        return self.role in (Role.staff, Role.admin)

    @property
    def is_superuser(self):
        return self.role == Role.admin

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Category(models.Model):
    category = models.CharField(max_length=100)


class Seller(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User)


class Product(AbstractModel):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Order(AbstractModel):
    status = models.CharField(max_length=15, choices=StatusEnum.choices,
                              default=StatusEnum.in_warehouse)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = None


