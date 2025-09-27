from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_gallery_images, name='get_all_gallery_images'),
    path('<int:pk>/', views.get_gallery_image, name='get_gallery_image'),
    path('create/', views.create_gallery_image, name='create_gallery_image'),
    path('<int:pk>/update/', views.update_gallery_image, name='update_gallery_image'),
    path('<int:pk>/delete/', views.delete_gallery_image, name='delete_gallery_image'),
]
