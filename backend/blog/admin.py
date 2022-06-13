from django.contrib import admin

from . models import Blog




class BlogAdmin(admin.ModelAdmin):
        list_display = ['is_published', 'title', 'blog_author']

    
admin.site.register(Blog, BlogAdmin)