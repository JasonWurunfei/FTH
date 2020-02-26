from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm

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