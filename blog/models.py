from django.db import models

# Create your models here.
from markdownx.models import MarkdownxField

class MyModel(models.Model):
    myfield = MarkdownxField()