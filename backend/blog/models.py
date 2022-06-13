from django.db import models
from django.urls import reverse
from django.conf import settings
from requests import request
from django.utils.text import slugify

from authentication.models import User
from comments.models import Comment


class Blog(models.Model):
    blog_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    # slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-title',)
        
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    def pub_blogs(self):
        return Blog.objects.filter(is_published=True)
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs
    
    
    
    
    


    


    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug