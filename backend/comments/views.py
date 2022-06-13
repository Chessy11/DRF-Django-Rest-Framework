from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer, create_custom_comment_serializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated



class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
comment_list_view = CommentListAPIView.as_view()


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        pk = self.request.GET.get("pk")
        parent_id = self.request.GET.get("parent_id", None)
        return create_custom_comment_serializer(
                model_type,
                pk,
                parent_id,
                author=self.request.user
            )

comment_create_view = CommentCreateAPIView.as_view()


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
comment_detail_view = CommentDetailAPIView.as_view()