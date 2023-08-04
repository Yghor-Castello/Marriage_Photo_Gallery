from rest_framework import serializers
from casamento.models import Gallery, Photo
from casamento.serializers.serializers_photo import PhotoSerializer


class GallerySerializer(serializers.ModelSerializer):
    
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['id', 'name', 'photos']

    def get_photos(self, obj):
        approved_photos = obj.photos.filter(approved=True)
        return PhotoSerializer(approved_photos, many=True).data


