import imp
import json
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from blog.serializers import BlogSerializer

# from blog.models import Blog

 

# @api_view(["POST"])
# def blog_post(request, *args, **kwargs):
#       serializer = BlogSerializer(data=request.data)
      
#       if serializer.is_valid(raise_exception=True):
#              print(serializer.data)
#              return Response(serializer.data)
#       return Response({"Invalid": "Invalid Request"}, status=400)
   


