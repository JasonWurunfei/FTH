from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogForm
from django.contrib.auth.models import User
from datetime import datetime

def blogsView(request):
    """Display all blog posts"""

    posts = BlogPost.objects.all().order_by('-created_date')

    return render(request, 'blog/blog.html', {'posts': posts})


def blogDetailView(request, pk):
    """Display specific blog posts"""

    post_detail = get_object_or_404(BlogPost, pk=pk)

    return render(request, 'blog/post.html', {'post_detail': post_detail})
    
    
@login_required
def newBlogView(request):
    user = User.objects.get(id=request.user.id)
    initial_data = {
        'user': user,
    }
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')
        else:
            print(request.POST)
    else:
        form = BlogForm(initial=initial_data)

    post_url = '/blog/new/'
    return render(request, 'blog/blog_edit.html', {'form': form, 'post_url': post_url})


@login_required
def editBlogView(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    initial_data = {
        'user': blog.user,
        'body': blog.body,
        'title': blog.title,
        'created_date': blog.created_date,
        'mod_date': datetime.now(),
    }
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')
        else:
            print(form.errors)
    else:
        form = BlogForm(initial=initial_data, instance=blog)

    post_url = '/blog/new/' + str(pk) + '/'
    return render(request, 'blog/blog_edit.html', {'form': form, 'post_url': post_url})
