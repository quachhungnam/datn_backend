from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    gender = models.BooleanField(null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(default='', null=True, max_length=15)

    class Meta:
        db_table = 'user'
