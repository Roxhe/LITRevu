from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, fields, Case, When
from django.urls import reverse
from authentication.models import User

from . import forms, models


@login_required
def my_blog(request):
    user = request.user
    photos = models.Photo.objects.all()
    tickets = models.Ticket.objects.filter(user=user)
    reviews = models.Review.objects.filter(user=user)

    context = {'photos': photos, 'tickets': tickets, 'user_name': user.username, 'reviews': reviews}
    return render(request, 'blog/my_blog.html', context)


@login_required
def home(request):
    user = request.user
    following_users = user.follows.all()
    tickets = models.Ticket.objects.filter(user__in=following_users).annotate(
        review_date=ExpressionWrapper(
            Case(
                When(review__isnull=False, then=F('review__date')),
                default=F('date'),
                output_field=fields.DateTimeField(),
            ),
            output_field=fields.DateTimeField()
        )
    ).order_by('-review_date')
    context = {'tickets': tickets}
    return render(request, 'blog/home.html', context)



@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})


@login_required
def ticket_and_photo_upload(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.photo = photo
            ticket.save()
            return redirect('home')

    return render(request, 'blog/create_ticket.html', context={'ticket_form': ticket_form, 'photo_form': photo_form,})


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'blog/view_ticket.html', {'ticket': ticket})


@login_required
def edit_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(pk=ticket_id)
    ticket_form = forms.TicketForm(instance=ticket)
    photo_form = forms.PhotoForm(instance=ticket.photo)

    if request.user == ticket.user:
        if request.method == 'POST':
            ticket_form = forms.TicketForm(request.POST, instance=ticket)
            photo_form = forms.PhotoForm(request.POST, request.FILES, instance=ticket.photo)
            if ticket_form.is_valid():
                if all([ticket_form.is_valid(), photo_form.is_valid()]):
                    photo = photo_form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
                    ticket = ticket_form.save(commit=False)
                    ticket.user = request.user
                    ticket.photo = photo
                    ticket.save()
    else:
        return redirect('home')

    return render(request, 'blog/edit_ticket.html', context={'ticket_form': ticket_form, 'photo_form': photo_form, 'ticket': ticket})


@login_required
def delete_ticket(request, ticket_id):
    ticket = models.Ticket.objects.get(pk=ticket_id)
    if request.user == ticket.user:
        if request.method == 'POST':
            ticket.delete()
            return redirect('home')
    else:
        return redirect('home')

    return render(request, 'blog/delete_ticket.html', {'ticket': ticket})


@login_required
def create_review(request, ticket_id):
    ticket = models.Ticket.objects.get(pk=ticket_id)
    if models.Review.objects.filter(ticket=ticket).exists():
        return redirect('view_ticket', ticket_id=ticket_id)
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.has_review = True
            ticket.save()
            return redirect('view_ticket', ticket_id=ticket_id)

    return render(request, 'blog/create_review.html', context={'review_form': review_form, 'ticket': ticket, })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.user == review.user:
        if request.method == 'POST':
            review.ticket.has_review = False
            review.ticket.save()
            review.delete()

            return redirect('home')
    else:
        return redirect('home')

    return render(request, 'blog/delete_review.html', {'review': review})


@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'blog/view_review.html', {'review': review})


@login_required
def create_ticket_review(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.photo = photo
            ticket.save()

            return redirect(reverse('create_review', kwargs={'ticket_id': ticket.id}))

    return render(request, 'blog/create_ticket_review.html', context={'ticket_form': ticket_form, 'photo_form': photo_form})


@login_required
def follow_users(request):
    following = request.user.follows.all()
    if request.method == 'POST':
        follow_user_form = forms.FollowUserForm(request.POST)
        if follow_user_form.is_valid():
            username = follow_user_form.cleaned_data['username']
            user_to_follow = User.objects.get(username=username)
            request.user.follows.add(user_to_follow)
            return redirect('home')

    if 'unfollow' in request.GET:
        user_to_unfollow_id = request.GET['unfollow']
        user_to_unfollow = User.objects.get(id=user_to_unfollow_id)
        request.user.follows.remove(user_to_unfollow)
        return redirect('home')

    follow_user_form = forms.FollowUserForm()
    return render(request, 'blog/follow_users_form.html', {'follow_user_form': follow_user_form, 'following': following,})
