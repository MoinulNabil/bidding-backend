from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=13)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone', ]

    class Meta:
        ordering = ['email']

    def __str__(self) -> str:
        return self.email
    
    @property
    def products(self):
        return self.products.all()

    @property
    def spent_money(self):
        ...

    @property
    def earned_money(self):
        ...

    @property
    def bids(self):
        return self.bids.all()