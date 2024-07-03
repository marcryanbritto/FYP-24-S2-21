from django.db import models
import uuid

# Create your models here.

# Account Class to identify account
class Account (models.Model):
    # Fields to be saved in Account
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=240)
    username = models.CharField(max_length=240)
    password = models.CharField(max_length=240)
    role = models.CharField(max_length=240)
    isDeactivated = models.BooleanField(default=False, null=False)
    email = models.EmailField(unique=True, null=False)
    registrationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name