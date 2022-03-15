from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    user_type=models.CharField(max_length=2,choices=(('1','staff'),('2','user')),default=2)

class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=30)
    def __str__(self):
        return self.name