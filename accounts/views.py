# request and response
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# forms
# from .forms import RegisterForm
# from .forms import LoginForm
from .forms import UserProfileEditForm

# Super view
from django.contrib.auth.views import LoginView

# restriction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# models
from blog.models import BlogPost, BlogSeries
# from django.contrib.auth.models import User
from accounts.models import User

# decorator
from .decorators import is_owner


# Create your views here.
# def registerView(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             new_user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password1'],
#             )
#             login(request, new_user)

#             return redirect("/")
#     else:
#         form = RegisterForm(request.POST)

#     return render(request, 'registration/register.html', context={'form': form})


# class MyLoginView(LoginView):
#     form_class = LoginForm

def is_visitor(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user.id == user.id:
        _is_visitor = False
    else:
        _is_visitor = True
    return _is_visitor


@login_required
def profileSeriesView(request, pk):
    user    = get_object_or_404(User, pk=pk)
    series_collection  = BlogSeries.objects.filter(user=user)

    context = {
        'user': user,
        'series_collection': series_collection,
        'is_visitor': is_visitor(request, pk),
    }
    return render(request, 'registration/profile_series.html', context)


@login_required
def profileView(request, pk):
    """Display user profile"""
    user    = get_object_or_404(User, pk=pk)
    posts   = BlogPost.objects.filter(user=user)
    context = {
        'user': user,
        'posts':posts,
        'is_visitor': is_visitor(request, pk),
    }
    return render(request, 'registration/profile.html', context)


@login_required
def profileSettingsView(request, pk):
    """Display user profile and profile editing"""
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user,
        'is_visitor': is_visitor(request, pk),
    }

    return render(request, 'registration/profile_settings.html', context)


@is_owner
@login_required
def profileSettingsEditView(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect(f"/accounts/settings/{user.id}/")

    else:
        form = UserProfileEditForm(instance=user)

    context = {
        "user": user,
        "form": form,
    }
    return render(request, 'registration/profile_settings_edit.html', context)


# AJAX response view
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)


def delete_blog(request):
    blogId  = request.GET.get('blogId', None)
    blog    = get_object_or_404(BlogPost, pk=blogId)
    blog.delete()
    data = {
        'blogId': blogId
    }
    return JsonResponse(data)


def delete_series(request):
    seriesId  = request.GET.get('seriesId', None)
    series    = get_object_or_404(BlogSeries, pk=seriesId)
    series.delete()
    data = {
        'seriesId': seriesId
    }
    return JsonResponse(data)
