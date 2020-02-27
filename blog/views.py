from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogForm
from django.contrib.auth.models import User

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

    return render(request, 'blog/blog_edit.html', {'form': form})