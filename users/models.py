from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)
    telegram_chat_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    max_num_of_orders = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.username

