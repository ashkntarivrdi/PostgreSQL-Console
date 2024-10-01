from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class App(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    state = models.CharField(max_length=50, default='Pending')
    size = models.PositiveIntegerField()

    def __str__(self):
        return self.name
