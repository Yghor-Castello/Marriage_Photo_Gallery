from django.db import models

from users.models import CustomUser


class Like(models.Model):

    photo = models.ForeignKey('Photo', related_name='likes', on_delete=models.CASCADE)
    liked_by = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.liked_by.name} liked {self.photo.uploaded_by.name}'s photo from {self.photo.gallery}"
    
    class Meta:
        ordering = ['-id']