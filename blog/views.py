from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import BlogForm
from comment.forms import CommentForm

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from likes.models import LikesAndDislikes
from comment.models import Comment
from .models import BlogPost

from datetime import datetime

def blogsView(request):
    """Display all blog posts"""
    order = request.GET.get('sortOrder')
    if order == None or order == "dec":
        posts = BlogPost.objects.all().order_by('-created_date')
    else:
        posts = BlogPost.objects.all().order_by('created_date')

    return render(request, 'blog/blog.html', {'posts': posts, 'order': order})

@login_required
def blogDetailView(request, pk):
    """Display specific blog posts"""
    user            = request.user
    post_detail     = get_object_or_404(BlogPost, pk=pk)
    blogPostType    = ContentType.objects.get(app_label='blog', model='blogpost')
    res             = LikesAndDislikes.objects.filter(content_type=blogPostType, object_id=pk)
    num_of_likes    = res.filter(like_type=False).count()
    num_of_dislikes = res.filter(like_type=True).count()

    comments = Comment.objects.filter(content_type=blogPostType, object_id=pk)

    initial_data = {
        'user': user,
        'content': "leave your comment here ~",
        'content_type': blogPostType,
        'object_id': pk,
    }
    form = CommentForm(initial=initial_data)

    context = {
        'post_detail'   : post_detail,
        'num_of_likes'  : num_of_likes,
        'num_of_dislikes': num_of_dislikes,
        'liked': False,
        'disliked': False,
        'form': form,
        'comments': comments,
    }

    is_done = LikesAndDislikes.objects.filter(
        user=user,
        content_type=blogPostType,
        object_id=pk
    )

    if is_done:
        if is_done.get().like_type == False:
            context['liked'] = True
        else:
            context['disliked'] = True

    return render(request, 'blog/post.html', context)
    
    
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
