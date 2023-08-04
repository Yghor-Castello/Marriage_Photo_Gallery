from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from casamento.models import Photo
from casamento.serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    
class UnapprovedPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(approved=False)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        photo = self.get_object()

        if request.user.user_type not in ['groom', 'bride']:
            return Response({"detail": "You do not have permission to approve this photo."}, status=status.HTTP_403_FORBIDDEN)

        photo.approved = True
        photo.save()

        return Response({'status': 'photo approved'})