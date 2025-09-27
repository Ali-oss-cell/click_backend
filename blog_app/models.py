from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """
    Blog post model for managing blog content
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title