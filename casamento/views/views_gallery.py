from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from casamento.models import Gallery
from casamento.models.models_photo import Photo
from casamento.serializers import GallerySerializer

class IsGroomOrBride(permissions.BasePermission):

    message = 'Only groom or bride can approve the photos.'

    def has_permission(self, request, view):
        return request.user.is_authorized_to_upload()


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    @action(detail=True, methods=['post'], permission_classes=[IsGroomOrBride])
    def approve(self, request, pk=None):
        photo_id = request.data.get('photo_id')
        if not photo_id:
            return Response({'detail': 'Photo id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response({'detail': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

        if photo.approved:
            return Response({'detail': 'Photo already approved'}, status=status.HTTP_400_BAD_REQUEST)

        photo.approved = True
        photo.gallery = self.get_object()
        photo.save()

        return Response({'status': 'photo approved'})




