from rest_framework import viewsets
from casamento import serializers

from casamento.models import Comment
from casamento.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(photo__approved=True)
    
    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        photo = serializer.validated_data['photo']
        if not photo.approved:
            raise serializers.ValidationError("The photo has not been approved yet.")
        serializer.save(commented_by=self.request.user)
