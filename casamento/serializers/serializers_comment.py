from rest_framework import serializers

from casamento.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('commented_by',)

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and (request.method in ['POST', 'PUT', 'PATCH']):
            fields.pop('commented_by', None)
        return fields
