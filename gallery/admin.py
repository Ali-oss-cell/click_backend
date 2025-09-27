from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['alt', 'category', 'display_order', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['alt', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['display_order', '-created_at']