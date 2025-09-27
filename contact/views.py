from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from .models import ContactMessage, NewsletterSubscriber
from .serializers import (
    ContactMessageSerializer, 
    ContactMessageCreateSerializer,
    NewsletterSubscriberSerializer,
    NewsletterSubscribeSerializer
)
from .email_service import MailgunService, DjangoEmailService


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_contact_message(request):
    """
    Send contact message endpoint
    POST /contact/
    """
    serializer = ContactMessageCreateSerializer(data=request.data)
    if serializer.is_valid():
        contact_message = serializer.save()
        
        # Try to send emails
        email_sent = False
        
        # Try Mailgun first
        try:
            mailgun = MailgunService()
            if mailgun.api_key and mailgun.domain:
                # Send notification to admin
                mailgun.send_contact_notification(contact_message)
                # Send confirmation to user
                mailgun.send_contact_confirmation(contact_message)
                email_sent = True
        except Exception as e:
            print(f"Mailgun error: {e}")
        
        # Fallback to Django email if Mailgun fails
        if not email_sent:
            try:
                django_email = DjangoEmailService()
                django_email.send_contact_notification(contact_message)
                django_email.send_contact_confirmation(contact_message)
                email_sent = True
            except Exception as e:
                print(f"Django email error: {e}")
        
        return Response({
            'success': True,
            'message': 'Your message has been sent successfully!',
            'data': ContactMessageSerializer(contact_message).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'details': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def subscribe_newsletter(request):
    """
    Subscribe to newsletter endpoint
    POST /newsletter/
    """
    serializer = NewsletterSubscribeSerializer(data=request.data)
    if serializer.is_valid():
        subscriber = serializer.save()
        
        # Try to send confirmation email
        try:
            mailgun = MailgunService()
            if mailgun.api_key and mailgun.domain:
                mailgun.send_newsletter_confirmation(subscriber.email)
        except Exception as e:
            print(f"Newsletter confirmation email error: {e}")
        
        return Response({
            'success': True,
            'message': 'Successfully subscribed to newsletter!',
            'data': NewsletterSubscriberSerializer(subscriber).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'details': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_contact_messages(request):
    """
    Get all contact messages (admin only)
    GET /contact/messages/
    """
    messages = ContactMessage.objects.all().order_by('-created_at')
    serializer = ContactMessageSerializer(messages, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'total': messages.count()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_contact_message(request, pk):
    """
    Get single contact message (admin only)
    GET /contact/messages/:id
    """
    try:
        contact_message = ContactMessage.objects.get(pk=pk)
        serializer = ContactMessageSerializer(contact_message)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except ContactMessage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Contact message not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_contact_message_status(request, pk):
    """
    Update contact message status (admin only)
    PUT /contact/messages/:id/status/
    """
    try:
        contact_message = ContactMessage.objects.get(pk=pk)
        new_status = request.data.get('status')
        
        if new_status not in ['new', 'read', 'replied', 'closed']:
            return Response({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid status. Must be: new, read, replied, or closed'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        contact_message.status = new_status
        contact_message.save()
        
        serializer = ContactMessageSerializer(contact_message)
        return Response({
            'success': True,
            'data': serializer.data
        })
        
    except ContactMessage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Contact message not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_newsletter_subscribers(request):
    """
    Get all newsletter subscribers (admin only)
    GET /newsletter/subscribers/
    """
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    serializer = NewsletterSubscriberSerializer(subscribers, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'total': subscribers.count()
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_contact_message(request, pk):
    """
    Delete contact message (admin only)
    DELETE /contact/messages/:id/
    """
    try:
        contact_message = ContactMessage.objects.get(pk=pk)
        contact_message.delete()
        return Response({
            'success': True,
            'message': 'Contact message deleted successfully'
        })
    except ContactMessage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Contact message not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)