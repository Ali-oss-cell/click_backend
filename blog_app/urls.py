from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_blog_posts, name='get_all_blog_posts'),
    path('<int:pk>/', views.get_blog_post, name='get_blog_post'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('<int:pk>/update/', views.update_blog_post, name='update_blog_post'),
    path('<int:pk>/delete/', views.delete_blog_post, name='delete_blog_post'),
]
