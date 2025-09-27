from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for user data
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class LoginSerializer(serializers.Serializer):
    """
    Login serializer
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            if not user.is_staff:
                raise serializers.ValidationError('Access denied. Admin privileges required.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password.')
