from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Admin login endpoint
    POST /auth/login
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'details': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Admin logout endpoint
    POST /auth/logout
    """
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            'success': True,
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 'INVALID_TOKEN',
                'message': 'Invalid token'
            }
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify token endpoint
    GET /auth/verify
    """
    return Response({
        'success': True,
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)