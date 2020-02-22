from django.shortcuts import render
from .forms import MyForm


# Create your views here.
def blogView(request):
    form = MyForm()
    return render(request, 'blog/blog.html', {'form': form})