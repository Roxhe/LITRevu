from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    title = models.CharField(max_length=128)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    description = models.CharField(max_length=4096, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
