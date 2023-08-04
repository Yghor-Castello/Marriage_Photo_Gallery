from rest_framework import serializers

from casamento.models import Like

   
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('liked_by',)

    def get_fields(self):
        fields = super(LikeSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and (request.method in ['POST', 'PUT', 'PATCH']):
            fields.pop('liked_by', None)
        return fields    

