from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType
from likes.models import LikesAndDislikes
from comment.models import Comment
from blog.models import BlogPost
from blog.models import BlogSeries

# Create your views here.
def homeView(request):
    latest_series = BlogSeries.objects.all().order_by('-id')[:3]

    top_liked_blog = None
    top_commented_blog =None
    like_max = -1
    comment_max = -1

    all_blogs = BlogPost.objects.all()
    blogPostType = ContentType.objects.get(
        app_label='blog', model='blogpost')
    commentType = ContentType.objects.get(
        app_label='comment', model='comment')

    for blog in all_blogs:
        num_of_likes = LikesAndDislikes.objects.filter(
            content_type=blogPostType, object_id=blog.id, like_type=False).count()
        num_of_dislikes = LikesAndDislikes.objects.filter(
            content_type=blogPostType, object_id=blog.id, like_type=True).count()
        total_likes = num_of_likes - num_of_dislikes

        num_of_comments = Comment.objects.filter(
            content_type=blogPostType, object_id=blog.id).count()

        if like_max < total_likes:
            like_max = total_likes
            top_liked_blog = blog

        if comment_max < num_of_comments:
            comment_max = num_of_comments
            top_commented_blog = blog

    context = {
        'top_liked_blog': top_liked_blog,
        'top_commented_blog': top_commented_blog,
        'latest_series': latest_series,
    }

    return render(request, 'home/index.html', context)