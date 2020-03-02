from django.contrib import admin
from .models import LikesAndDislikes

# Register your models here.
@admin.register(LikesAndDislikes)
class LikesAndDislikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'like_type', 'content_type', 'object_id', 'date')
    list_filter = ('date',)
    search_fields = ('user',)