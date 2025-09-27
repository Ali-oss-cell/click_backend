from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('', views.send_contact_message, name='send_contact_message'),
    path('newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Admin endpoints
    path('messages/', views.get_contact_messages, name='get_contact_messages'),
    path('messages/<int:pk>/', views.get_contact_message, name='get_contact_message'),
    path('messages/<int:pk>/status/', views.update_contact_message_status, name='update_contact_message_status'),
    path('messages/<int:pk>/delete/', views.delete_contact_message, name='delete_contact_message'),
    path('newsletter/subscribers/', views.get_newsletter_subscribers, name='get_newsletter_subscribers'),
]
