from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_date', 'content_type', 'object_id')
    list_filter = ('pub_date', 'content_type', 'object_id')
    search_fields = ('user',)