from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.created_at = timezone.now()
        self.save()
        return self.code

    def __str__(self):
        return f"{self.user.username} - {self.code}"
