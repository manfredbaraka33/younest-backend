from rest_framework import serializers
from .models import MyUser
from shop.models import Shop,ProductOrService
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


from rest_framework import serializers
from .models import MyUser
from shop.models import Shop, ProductOrService
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class MyUserSerializer(serializers.ModelSerializer):
    followed_shops = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), many=True, required=False)
    saved_products_or_services = serializers.PrimaryKeyRelatedField(queryset=ProductOrService.objects.all(), many=True, required=False)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_image', 'followed_shops', 'saved_products_or_services']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        # Check if the username already exists, excluding the current user
        user = self.context.get('user')
        if MyUser.objects.filter(username=value).exclude(id=user.id).exists():
            raise ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        # Check if the email is already taken, excluding the current user
        user = self.context.get('user')
        if MyUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise ValidationError("This email is already taken.")
        return value

    def update(self, instance, validated_data):
        # Only update fields that are passed in the request data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)

        # Handle image upload if provided
        if 'profile_image' in validated_data:
            instance.profile_image = validated_data.get('profile_image', instance.profile_image)

        # Handle ManyToMany relationships (followed_shops and saved_products_or_services)
        if 'followed_shops' in validated_data:
            instance.followed_shops.set(validated_data['followed_shops'])
        if 'saved_products_or_services' in validated_data:
            instance.saved_products_or_services.set(validated_data['saved_products_or_services'])

        instance.save()
        return instance

    def create(self, validated_data):
        # Create a new user instance (same logic as before for password handling)
        password = validated_data.pop('password')
        followed_shops = validated_data.pop('followed_shops', [])
        saved_products_or_services = validated_data.pop('saved_products_or_services', [])

        user = MyUser.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        # Assign ManyToMany relationships
        if followed_shops:
            user.followed_shops.set(followed_shops)
        if saved_products_or_services:
            user.saved_products_or_services.set(saved_products_or_services)

        return user


# class MyUserSerializer(serializers.ModelSerializer):
#     followed_shops = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), many=True, required=False)
#     saved_products_or_services = serializers.PrimaryKeyRelatedField(queryset=ProductOrService.objects.all(), many=True, required=False)

#     class Meta:
#         model = MyUser
#         fields = ['id','username', 'email', 'password', 'bio', 'profile_image', 'followed_shops', 'saved_products_or_services']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         # Extract fields that are not password-related
#         password = validated_data.pop('password')
#         followed_shops = validated_data.pop('followed_shops', [])
#         saved_products_or_services = validated_data.pop('saved_products_or_services', [])

#         # Create the user instance
#         user = MyUser.objects.create(**validated_data)
#         user.set_password(password)  # Hash the password
#         user.save()

#         # Assign ManyToMany relationships
#         if followed_shops:
#             user.followed_shops.set(followed_shops)  # Use .set() to assign ManyToMany
#         if saved_products_or_services:
#             user.saved_products_or_services.set(saved_products_or_services)  # Use .set() for ManyToMany

#         return user
    
    
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        # Check if the new passwords match
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match.")
        # Validate the new password using Django's built-in validators
        validate_password(attrs['new_password'])
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
