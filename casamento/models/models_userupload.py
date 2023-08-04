from django.db import models


class UserUpload(models.Model):
    
    upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return str(self.upload)

    class Meta:
        ordering = ['-id']

        