from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    gender = models.BooleanField(
        choices=[(1, 'MALE'), (0, 'FEMALE')], null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(
        default='', null=True, blank=True, max_length=15)
    address = models.CharField(
        max_length=200, default='', null=True, blank=True)

    class Meta:
        db_table = 'user'
