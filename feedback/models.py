from django.db import models

# Create your models here.
class Feedback(models.Model):
    email=models.EmailField()
    text=models.TextField()
    
    def __str__(self):
        return f"Feedback from {self.email}"
