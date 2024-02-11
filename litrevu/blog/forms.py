from django import forms
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur à suivre")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['title', 'description', 'rating']


