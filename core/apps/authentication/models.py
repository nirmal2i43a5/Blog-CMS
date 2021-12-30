

from django.db import models

# Create your models here.
class Subscription(models.Model):
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.email} on {self.created_at}'