from django.db import models
# from user.models import MyUser
from django.conf import settings


class Shop(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=25)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followedShops', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} by {self.owner}" 



class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return self.image.url


class ProductOrService(models.Model):
    TYPE_CHOICES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    
    shop = models.ForeignKey(Shop, related_name='products_or_services', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='product')
    image = models.ManyToManyField(ProductImage, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(null=True, max_length=150)
    views  = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    


    

class OfferOrPromotion(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='offers_or_promotions')
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='offer_promotion_images/', blank=True, null=True)

    def __str__(self):
        return self.name
