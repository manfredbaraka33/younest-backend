
from rest_framework import serializers
from .models import Shop, ProductOrService, ProductImage
from user.models import MyUser
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class ShopSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all())
    followers_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = '__all__'

    def get_followers_count(self, obj):
        
        return obj.followers.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.followers.filter(id=request.user.id).exists()




class ProductOrServiceSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), required=False)
    images = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = ProductOrService
        fields = '__all__'
        depth = 1
        
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            # Include full shop details
            shop_serializer = ShopSerializer(instance.shop, context={'request': request})
            representation['shop'] = shop_serializer.data

            # Build final image URLs manually using urljoin
            images_qs = ProductImage.objects.filter(productorservice=instance)
            image_urls = []
            for image in images_qs:
                if image.image:
                    # image.image.url is stored as "/media/product_images/xxx.jpeg"
                    # Build absolute URL: e.g., "http://127.0.0.1:8000/media/product_images/xxx.jpeg"
                    absolute_url = urljoin(f"{request.scheme}://{request.get_host()}/", image.image.url.lstrip('/'))
                    image_urls.append(absolute_url)
            representation['images'] = image_urls
        return representation


