from django import forms
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    follows = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ['follows']


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


