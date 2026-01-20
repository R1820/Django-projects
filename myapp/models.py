from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField()
    password = models.CharField(max_length=20)
    uprofile = models.ImageField(default="")
    usertype = models.CharField(max_length=26, default="customer")

    def __str__(self):
        return f"{self.name}"
    
    