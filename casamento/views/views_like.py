from rest_framework import viewsets, serializers  

from casamento.models import Like
from casamento.serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(photo__approved=True)
    
    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        photo = serializer.validated_data['photo']
        if not photo.approved:
            raise serializers.ValidationError("The photo has not been approved yet.")
        serializer.save(liked_by=self.request.user)
