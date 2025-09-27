from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'author', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']