from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    follows = models.ManyToManyField('self', symmetrical=False, verbose_name='suit')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.follows.add(self)
