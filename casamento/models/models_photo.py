from django.db import models

from users.models import CustomUser


class Photo(models.Model):
    
    gallery = models.ForeignKey('Gallery', related_name='photos', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(CustomUser, related_name='uploaded_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.image)
    
    class Meta:
        ordering = ['-id']