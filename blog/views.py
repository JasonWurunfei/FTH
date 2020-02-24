from django.shortcuts import render, get_object_or_404

from .models import BlogPost
from .forms import BlogForm

def blogsView(request):
    """Display all blog posts"""

    posts = BlogPost.objects.all().order_by('-created_date')

    return render(request, 'blog/blog.html', {'posts': posts})


def blogDetailView(request, pk):
    """Display specific blog posts"""

    post_detail = get_object_or_404(BlogPost, pk=pk)

    return render(request, 'blog/post.html', {'post_detail': post_detail})

def newBlogView(request):
    form = BlogForm()
    return render(request, 'blog/blog_edit.html', {'form': form})