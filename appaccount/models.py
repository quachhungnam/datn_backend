from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = [(0, 'Nữ'), (1, 'Nam')]
    birthday = models.DateField(null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    gender = models.BooleanField(
        null=True, blank=True, choices=GENDER_CHOICES,)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        default='', null=True, blank=True, max_length=15)
    address = models.CharField(
        default='', null=True, blank=True, max_length=200)

    # avatar = models.CharField(default='', null=True,
    #                           blank=True, max_length=255)
    avatar = models.ImageField(upload_to='images/%Y/%m/%d/', default='images/avatar_default.png')

    class Meta:
        db_table = 'user'
