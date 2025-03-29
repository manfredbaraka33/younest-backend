from django.db import models
from user.models import MyUser
from shop.models import Shop,ProductOrService


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(ProductOrService, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user') 

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} -- {self.rating}⭐"
