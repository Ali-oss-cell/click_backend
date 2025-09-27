from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Blog post serializer
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'excerpt', 'content', 'featured_image', 
            'author', 'author_name', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
