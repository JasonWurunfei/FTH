from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from likes.models import LikesAndDislikes
from comment.models import Comment
# Create your models here.
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from django.utils import timezone
from datetime import datetime


class DateCreateModMixin(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=timezone.now)
    mod_date     = models.DateTimeField(default=timezone.now, blank=True, null=True)


class BlogSeries(DateCreateModMixin):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    background_image = models.ImageField(
        default='img/header.jpg',
        upload_to=datetime.now().strftime('backgrounds/%Y/%m/%d')
    )

    def description_summary(self):
        if len(self.description) > 20:
            return self.description[:20] + "..."
        else:
            return self.description

class BlogPost(DateCreateModMixin):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series  = models.ForeignKey(BlogSeries, on_delete=models.SET_NULL, null=True, blank=True)
    title   = models.CharField(max_length=100)
    body    = MarkdownxField()

    likes    = GenericRelation(LikesAndDislikes)
    comments = GenericRelation(Comment)

    def formatted_markdown(self):
        return markdownify(self.body)

    def body_summary(self):
        return markdownify(self.body[:300] + "...")
