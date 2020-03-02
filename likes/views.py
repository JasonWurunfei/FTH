from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# models
from .models import LikesAndDislikes
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

# Create your views here.
def likesAndDislikeView(request):
    user   = request.user
    app_label   = request.POST['app_label']
    model       = request.POST['model']
    object_id   = request.POST['object_id']
    like_type   = True if request.POST['like_type'] == 'true' else False

    blogPostType = ContentType.objects.get(app_label=app_label, model=model)

    is_done = LikesAndDislikes.objects.filter(
        user=user,
        content_type=blogPostType,
        object_id=object_id
    )

    if is_done:
        old_like_type = is_done.get().like_type
        if old_like_type == like_type:
            is_done.delete()

        else:
            obj = is_done.get()
            obj.like_type = like_type
            obj.save()

    else:
        LikesAndDislikes.objects.create(
            user=user,
            date=datetime.now(),
            like_type=like_type,
            content_type=blogPostType,
            object_id=object_id
        )
    
    res = LikesAndDislikes.objects.filter(content_type=blogPostType, object_id=object_id)
    num_of_likes = res.filter(like_type=False).count()
    num_of_dislikes = res.filter(like_type=True).count()

    data = {
        'num_of_likes': num_of_likes,
        'num_of_dislikes': num_of_dislikes,
    }

    return JsonResponse(data)
