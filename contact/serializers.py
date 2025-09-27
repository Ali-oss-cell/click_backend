from rest_framework import serializers
from .models import ContactMessage, NewsletterSubscriber


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Contact message serializer
    """
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'subject', 'message', 'phone',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """
    Contact message creation serializer
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'phone']
    
    def validate_email(self, value):
        """
        Validate email format
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value
    
    def validate_name(self, value):
        """
        Validate name
        """
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()
    
    def validate_message(self, value):
        """
        Validate message
        """
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value.strip()


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    """
    Newsletter subscriber serializer
    """
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'is_active', 'subscribed_at']


class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    """
    Newsletter subscription serializer
    """
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
    
    def validate_email(self, value):
        """
        Validate email format
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value.lower()
    
    def create(self, validated_data):
        """
        Create or update newsletter subscription
        """
        email = validated_data['email']
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        if not created:
            subscriber.is_active = True
            subscriber.save()
        return subscriber
