from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import MyModel

# Register your models here.
admin.site.register(MyModel, MarkdownxModelAdmin)

