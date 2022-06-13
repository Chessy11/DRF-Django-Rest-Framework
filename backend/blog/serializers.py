from requests import request
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField, HyperlinkedIdentityField

from authentication.models import User
from . models import Blog
from comments.serializers import CommentSerializer

from comments.models import Comment





class BlogCreateSerializer(serializers.ModelSerializer):
    is_published = SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'title',
            'content',
            'is_published'
        ]

    def get_is_published(self, obj):
        if obj.is_published == True:
            return obj
        else:
            return {"Your Blog is under review process..."}

post_detail_url = HyperlinkedIdentityField(
        view_name='blog:detail',
    )

    
    
class BlogDetailSerializer(serializers.ModelSerializer):
    # url = post_detail_url
    blog_author = serializers.ReadOnlyField(source='blog_author.username')
    comments = SerializerMethodField()

    class Meta:
        model= Blog
        fields = [
            # "url",
            "id",
            "blog_author",
            "title",
            "content",
            "comments",
            
            ]
    
    def get_blog_author(self, obj):
            return {
            "username": obj.blog_author.username
        }
            
    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments
    
    
class BlogSerializer(serializers.ModelSerializer):
    
        
    class Meta:
        model = Blog
        fields = []

        
        
class BlogForUsersSerializer(serializers.ModelSerializer):
    
    is_published = serializers.SerializerMethodField()
    
    def get_is_published(self, blog):
        qs = Blog.objects.filter(is_published=True)
        blog = BlogSerializer(qs,  many = True).data
        return blog
        
    class Meta:
        model = Blog
        fields = [
            'pk',
            'blog_author',
            'is_published',
            'title',
            
            ]
        
        

class BlogListSerializer(serializers.ModelSerializer):
    blog_author = serializers.ReadOnlyField(source='blog_author.username')
    comments = CommentSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            'pk',
            'blog_author',
            "title",
            "content",
            'comments',
            'is_published'
        ]
        


        
class BlogUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        
        fields = [
            'id',
            'title',
            'content'
        ]
        
