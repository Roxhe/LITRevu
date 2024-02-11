"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('follow-users/', blog.views.follow_users, name='follow_users'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('my_blog/', blog.views.my_blog, name='my_blog'),
    path('home/', blog.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('create_ticket_review/', blog.views.create_ticket_review, name='create_ticket_review'),
    path('ticket/create/', blog.views.ticket_and_photo_upload, name='ticket_create'),
    path('ticket/<int:ticket_id>', blog.views.view_ticket, name='view_ticket'),
    path('ticket/<int:ticket_id>/delete_ticket/', blog.views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/edit_ticket/', blog.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/create_review/', blog.views.create_review, name='create_review'),
    path('ticket/delete_review/', blog.views.delete_review, name='delete_review'),
    path('review/<int:review_id>', blog.views.view_review, name='view_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
