from django.db import models

class GeneratedImage(models.Model):
    """ Model schema to save generated image from the prompt text """
    
    prompt = models.CharField(max_length=255)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prompt