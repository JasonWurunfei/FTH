from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CommentForm

# Create your views here.

@login_required
def commentView(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            previous_url = request.META.get('HTTP_REFERER')
            redirect_url = '/blog/' if previous_url==None else previous_url
            return redirect(redirect_url)

