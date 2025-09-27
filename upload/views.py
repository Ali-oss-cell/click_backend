from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import os


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_image(request):
    """
    Upload image endpoint
    POST /upload/image
    """
    if 'image' not in request.FILES:
        return Response({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'No image file provided'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']
    category = request.data.get('category', 'gallery')
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if image_file.content_type not in allowed_types:
        return Response({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid file type. Only JPEG, PNG, and GIF files are allowed.'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate unique filename
    file_extension = os.path.splitext(image_file.name)[1]
    unique_filename = f"image_{uuid.uuid4().hex}{file_extension}"
    
    # Determine upload path based on category
    if category == 'blog':
        upload_path = f'blog/images/{unique_filename}'
    elif category == 'gallery':
        upload_path = f'gallery/images/{unique_filename}'
    else:
        upload_path = f'uploads/images/{unique_filename}'
    
    # Save file
    try:
        saved_path = default_storage.save(upload_path, ContentFile(image_file.read()))
        file_url = f'/media/{saved_path}'
        
        return Response({
            'success': True,
            'data': {
                'filename': unique_filename,
                'url': file_url,
                'size': image_file.size,
                'mimetype': image_file.content_type
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 'UPLOAD_ERROR',
                'message': f'Failed to upload image: {str(e)}'
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)