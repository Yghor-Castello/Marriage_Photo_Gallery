from rest_framework import serializers

from casamento.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['gallery', 'image', 'approved']


