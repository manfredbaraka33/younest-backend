from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  
    user_pic = serializers.SerializerMethodField()  
    user_id = serializers.SerializerMethodField()  

    class Meta:
        model = Review
        fields = '__all__'  # Includes created_at as a raw timestamp

    def get_user_pic(self, obj):
        """Retrieve the user's profile image URL"""
        if obj.user.profile_image:
            image= "http://127.0.0.1:8000"+obj.user.profile_image.url # Directly access profile_image from MyUser model
            return image
        return None  # Return None if no profile image exists 
    
    def get_user_id(self, obj):
        """Retrieve the user's id"""
        if obj.user.id:
            user_id=obj.user.id
            return user_id
        return None  # Return None if no profile image exists 

