from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Comment(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date        = models.DateTimeField(auto_now_add=True)
    content         = RichTextUploadingField()

    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
