from django.db import models


class Gallery(models.Model):
    
    name = models.CharField('Gallery', max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']