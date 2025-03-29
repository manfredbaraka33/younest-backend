from django.db import models
from user.models import MyUser


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return self.image.url

class ForSaleProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ManyToManyField(ProductImage, blank=True) 
    description = models.TextField(null=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(MyUser, related_name='forsale', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.name} by {self.seller}"