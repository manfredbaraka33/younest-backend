from django.db import models
from user.models import MyUser
from django.utils import timezone


class Notification(models.Model):
    TYPES = ( 
    ('follow', 'Follow'), 
    ('review', 'Review'), 
    ('product', 'Product'), 
    ('promo', 'Promo'), 
    ) 
    user = models.ForeignKey(MyUser, related_name="notifications", on_delete=models.CASCADE) 
    message = models.CharField(max_length=255) 
    notification_type = models.CharField(choices=TYPES, max_length=50,null=True) 
    related_id = models.IntegerField(null=True,blank=True)
    read = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now) 
 

    def __str__(self): 
        return f"{self.message} for {self.user.username}" 