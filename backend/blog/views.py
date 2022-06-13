from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from . serializers import  BlogCreateSerializer, BlogDetailSerializer, BlogListSerializer, BlogUpdateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import AuthenticationFailed


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer
    permission_classes = [IsAuthenticated]
   


            
    
    def perform_create(self, serializer):
        token = self.request.COOKIES.get('access')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        else:
            
            message = {"Your post is sent for moderation, please wait until it's permitted"}
            return (serializer.save(blog_author=self.request.user), message)
    
    
 
                
blog_create_view = BlogCreateAPIView.as_view()



class BlogDetailApiView(generics.RetrieveAPIView):
    serializer_class = BlogDetailSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Blog.objects.all()
        return queryset.filter(is_published=True)
    
blog_detail_view = BlogDetailApiView.as_view()


    

class BlogListingAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # lookup_field = 'blog_author'
    
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        return queryset
    
blog_listing_view = BlogListingAPIView.as_view()


class BlogUpdateAPIView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

blog_update_view = BlogUpdateAPIView.as_view()
            
# blog_update_view = BlogUpdateAPIView.as_view()


# class BlogDeleteAPIView(generics.DestroyAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
    
#     def perform_destroy(self, instance):
#         super().perform_destroy(instance)
            
# blog_delete_view = BlogDeleteAPIView.as_view()