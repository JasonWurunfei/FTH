from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/blog")
    else:
        form = RegisterForm(request.POST)

    return render(request, 'registration/register.html', context={'form': form})

class MyLoginView(LoginView):
    form_class = LoginForm

@login_required
def profileView(request, pk):
    """Display user profile"""

    user = get_object_or_404(User, pk=pk)

    return render(request, 'registration/profile.html', {'user': user})



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