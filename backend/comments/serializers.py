from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from rest_framework.serializers import ValidationError

from .models import Comment

from authentication.models import User


def create_custom_comment_serializer(model_type='blog', pk=None, parent_id=None, author=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'Comments'
            model = Comment
            fields = [
                'parent_id',
                'pk',
                'content',
                'created_at',
                
            ]
  
 
        
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            print(self.model_type)
            self.pk = pk
            self.parent_obj = None
            if parent_id:
                print('======Parent ID=======', parent_id)
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            Sm = model_qs.first().model_class()
            obj_qs = Sm.objects.filter(pk=self.pk)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a primary key for this content type")
            return data

        def create(self,  validated_data):
            content = validated_data.get("content")
            if author:
                main_user = author
            else:
                main_user = author
            model_type = self.model_type
            pk = self.pk

            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type,
                    pk, 
                    content, 
                    main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer




class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'created_at' 
            ]



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        
        fields = [
            'id',
            'content',
            'content_type',
            'object_id',
            'author',
            'created_at',
            'reply_count',
            'replies'
        ]        
        
    
    
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    
    def get_author(self, obj):
        return obj.author.username




class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    reply_count = serializers.SerializerMethodField()
    content_object_url = serializers.SerializerMethodField()
    replies =   serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'reply_count',
            'replies',
            'created_at',
            'content_object_url',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
