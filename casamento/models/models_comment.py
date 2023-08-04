from django.db import models

from users.models import CustomUser


class Comment(models.Model):

    photo = models.ForeignKey('Photo', related_name='comments', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.commented_by.name} commented on {self.photo.uploaded_by.name}'s photo"

    class Meta:
        ordering = ['-id']