from django.db import models

class LoginSchema(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Password storage should be hashed, though this is just a sample.

    def __str__(self):
        return self.username
