from django.db import models


class GalleryImage(models.Model):
    """
    Gallery image model for managing image gallery
    """
    CATEGORY_CHOICES = [
        ('portfolio', 'Portfolio'),
        ('gallery', 'Gallery'),
        ('testimonial', 'Testimonial'),
        ('team', 'Team'),
    ]
    
    src = models.ImageField(upload_to='gallery/images/')
    alt = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='gallery')
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gallery_images'
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.alt} ({self.category})"