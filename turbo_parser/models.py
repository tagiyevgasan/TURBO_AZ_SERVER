from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.

class Order(models.Model):
    threshold = models.FloatField()
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(default=timezone.now)
    ordered_link = models.URLField(max_length=3000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Order Object (id=' + str(self.id) + ')'


class SendedLink(models.Model):
    sended_link = models.CharField(max_length=300)
    sended_at = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return 'SendedLink Object (id=' + str(self.id)+')'
