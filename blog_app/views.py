from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    List all blog posts or create a new blog post
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a blog post
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_blog_posts(request):
    """
    Get all published blog posts (public endpoint)
    GET /blog-posts
    """
    blog_posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    serializer = BlogPostSerializer(blog_posts, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'total': blog_posts.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_blog_post(request, pk):
    """
    Get single blog post (public endpoint)
    GET /blog-posts/:id
    """
    try:
        blog_post = BlogPost.objects.get(pk=pk, status='published')
        serializer = BlogPostSerializer(blog_post)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except BlogPost.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Blog post not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_blog_post(request):
    """
    Create blog post (admin only)
    POST /blog-posts
    """
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, status='published')
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
def update_blog_post(request, pk):
    """
    Update blog post (admin only)
    PUT /blog-posts/:id
    """
    try:
        blog_post = BlogPost.objects.get(pk=pk)
        serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
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
    except BlogPost.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Blog post not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_blog_post(request, pk):
    """
    Delete blog post (admin only)
    DELETE /blog-posts/:id
    """
    try:
        blog_post = BlogPost.objects.get(pk=pk)
        blog_post.delete()
        return Response({
            'success': True,
            'message': 'Blog post deleted successfully'
        })
    except BlogPost.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Blog post not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)