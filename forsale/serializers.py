
from rest_framework import serializers
from .models import ForSaleProduct, ProductImage
from user.models import MyUser
from user.serializers import MyUserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ForSaleproductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all())
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = ForSaleProduct
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        """
        Modify the way the 'shop' and 'images' fields are represented.
        
        """
        representation = super().to_representation(instance)
        request = self.context.get('request', None)

        if request and request.method == 'GET':
            user_serializer = MyUserSerializer(instance.seller, context={'request': request})
            representation['seller'] = user_serializer.data
            
            # Include product images in the response
            images = ProductImage.objects.filter(forsaleproduct=instance)
            representation['images'] = [image.image.url for image in images]

        return representation

   

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Update the product instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle image updates (i.e., add new images if any)
        if images_data:
            for image_data in images_data:
                ProductImage.objects.create(forsaleproduct=instance, image=image_data['image'])

        return instance
