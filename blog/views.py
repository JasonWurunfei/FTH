from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django import forms
from .forms import BlogForm, SeriesForm
from comment.forms import CommentForm

from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
from accounts.models import User

from likes.models import LikesAndDislikes
from comment.models import Comment
from .models import BlogPost, BlogSeries

from datetime import datetime
from allauth.account.decorators import verified_email_required
from .decorators import is_owner

def blogsView(request):
    """Display all blog posts"""
    order = request.GET.get('sortOrder')
    if order == None or order == "dec":
        posts = BlogPost.objects.all().order_by('-created_date')
    else:
        posts = BlogPost.objects.all().order_by('created_date')

    return render(request, 'blog/blog.html', {'posts': posts, 'order': order})


@verified_email_required
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

    
@verified_email_required
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


@verified_email_required
@login_required
@is_owner(BlogPost)
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


@login_required
def seriesView(request):
    all_series = BlogSeries.objects.all()
    return render(request, 'blog/series.html', {'all_series': all_series})

@verified_email_required
@login_required
def newSeriesView(request):
    user = User.objects.get(id=request.user.id)
    initial_data = {
        'user': user,
    }

    if request.method == "POST":
        form = SeriesForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            data = form.cleaned_data
            new_series = form.save()
            data['blogs'].update(series=new_series)
            return redirect('blog:series')
        else:
            print(request.POST)
    else:
        form = SeriesForm(initial=initial_data, user=user)

    post_url = '/blog/series/new/'
    return render(request, 'blog/series_edit.html', {'form': form, 'post_url': post_url})


@verified_email_required
@login_required
@is_owner(BlogSeries)
def editSeriesView(request, pk):
    user = User.objects.get(id=request.user.id)
    series = get_object_or_404(BlogSeries, pk=pk)
    blogs = BlogPost.objects.filter(series=series)

    initial_data = {
        'user': series.user,
        'title': series.title,
        'description': series.description,
        'background_image': series.background_image,
        'blogs': blogs,
        'created_date': series.created_date,
        'mod_date': datetime.now(),
    }

    if request.method == "POST":
        form = SeriesForm(request.POST, request.FILES, instance=series, user=user)
        if form.is_valid():
            data = form.cleaned_data
            new_series = form.save()

            # Set all blogs which belongs to this user so that old one will
            # be removed if not selected. 
            BlogPost.objects.filter(user=user).update(series=None)

            data['blogs'].update(series=new_series)
            return redirect('blog:series')
        else:
            print(form.errors)
    else:
        form = SeriesForm(initial=initial_data, user=user)

    # In order to share the edit template, use post_user to dynamically
    # change the form action to different url localtion.
    post_url = '/blog/series/new/' + str(pk) + '/'
    return render(request, 'blog/series_edit.html', {'form': form, 'post_url': post_url})


@verified_email_required
@login_required
def seriesDetailView(request, pk):
    series  = get_object_or_404(BlogSeries, pk=pk)
    blogs   = series.blogpost_set.all()
    context = {
        'series': series,
        'blogs': blogs
    }
    return render(request, 'blog/series_detail.html', context)


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