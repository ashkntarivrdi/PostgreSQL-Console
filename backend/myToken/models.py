from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(hours=1)

    def __str__(self):
        return f"Token for {self.user.username}"
    
    def generate_token(user):
        token, _ = Token.objects.get_or_create(user=user)
        token.key = str(uuid.uuid4())
        token.created_at = timezone.now()
        token.save()
        return token