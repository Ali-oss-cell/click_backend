from rest_framework import serializers
from .models import GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    """
    Gallery image serializer
    """
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'src', 'alt', 'caption', 'category', 
            'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
