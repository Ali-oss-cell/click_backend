from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryImageListCreateView(generics.ListCreateAPIView):
    """
    List all gallery images or create a new gallery image
    """
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['alt', 'caption']
    ordering_fields = ['display_order', 'created_at']
    ordering = ['display_order', '-created_at']


class GalleryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a gallery image
    """
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_gallery_images(request):
    """
    Get all gallery images (public endpoint)
    GET /gallery-images
    """
    gallery_images = GalleryImage.objects.all().order_by('display_order', '-created_at')
    serializer = GalleryImageSerializer(gallery_images, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'total': gallery_images.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_gallery_image(request, pk):
    """
    Get single gallery image (public endpoint)
    GET /gallery-images/:id
    """
    try:
        gallery_image = GalleryImage.objects.get(pk=pk)
        serializer = GalleryImageSerializer(gallery_image)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except GalleryImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Gallery image not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_gallery_image(request):
    """
    Create gallery image (admin only)
    POST /gallery-images
    """
    serializer = GalleryImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': 'Invalid input data',
            'details': serializer.errors
        }
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_gallery_image(request, pk):
    """
    Update gallery image (admin only)
    PUT /gallery-images/:id
    """
    try:
        gallery_image = GalleryImage.objects.get(pk=pk)
        serializer = GalleryImageSerializer(gallery_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            })
        return Response({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid input data',
                'details': serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    except GalleryImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Gallery image not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_gallery_image(request, pk):
    """
    Delete gallery image (admin only)
    DELETE /gallery-images/:id
    """
    try:
        gallery_image = GalleryImage.objects.get(pk=pk)
        gallery_image.delete()
        return Response({
            'success': True,
            'message': 'Gallery image deleted successfully'
        })
    except GalleryImage.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Gallery image not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)