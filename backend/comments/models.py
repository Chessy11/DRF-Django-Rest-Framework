from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models
from authentication.models import User
from django.conf import settings

  
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, pk, content, author, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=pk)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.author = author
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None
  

   
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    objects= CommentManager()
    
    class Meta:
        ordering = ('-created_at',)
        indexes = [ 
                models.Index(fields=["content_type", "object_id"]),
            ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True