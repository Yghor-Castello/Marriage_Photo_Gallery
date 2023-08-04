from rest_framework import serializers

from casamento.models import UserUpload


class UserUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUpload
        fields = ['upload']

