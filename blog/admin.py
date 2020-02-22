from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import BlogPost

# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'created_date', 'mod_date')
    list_filter = ('created_date', 'mod_date')
    search_fields = ('title',)

