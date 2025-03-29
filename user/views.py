from rest_framework import generics,permissions
from .serializers import MyUserSerializer,ChangePasswordSerializer
from .models import MyUser
from django.contrib.auth.decorators import login_required
from shop.models import ProductOrService as Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import permissions,views
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics,status
from shop.serializers import ProductOrServiceSerializer
from rest_framework.response import Response
from shop.models import Shop



class UserCreateAPIView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes=[permissions.AllowAny]

register_view =   UserCreateAPIView.as_view() 


class UserdetailAPIView(generics.RetrieveAPIView):
     queryset= MyUser.objects.all()
     serializer_class = MyUserSerializer
     permission_classes=[permissions.IsAuthenticated]

     def get_object(self):
          return self.request.user
     
user_details = UserdetailAPIView.as_view()

class ToggleSaveProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, product_id):
        user = request.user  # Get authenticated user
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        # Check if product is already in saved products
        if product in user.saved_products_or_services.all():
            user.saved_products_or_services.remove(product)  # Remove from saved
            saved = False
        else:
            user.saved_products_or_services.add(product)  # Add to saved
            product.saves += 1
            saved = True
            
         # Save the updated saves count
        product.save(update_fields=["saves"])

        # Return response with status and saved state
        return JsonResponse({
            "message": "Product added to saved" if saved else "Product removed from saved",
            "saved": saved,
            "product_id": product.id
        })

toggle_save_product = ToggleSaveProductView.as_view()




class SavedProductsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        saved_products = user.saved_products_or_services.all()  # Get the saved products
        
        if not saved_products:
            pass

        serialized_products = ProductOrServiceSerializer(saved_products, many=True).data
        
        
        
        return Response({"saved_products": serialized_products})
    
        
get_saved_products = SavedProductsListView.as_view()



class OtherUserDetails(generics.RetrieveAPIView):
    serializer_class=MyUserSerializer
    queryset=MyUser.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    

get_other_user_details=OtherUserDetails.as_view()




class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        # Returns the current authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class UserProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def patch(self, request, *args, **kwargs):
        # Get the currently authenticated user
        user = request.user

        # Initialize the serializer with the user's data and the provided request data
        serializer = MyUserSerializer(user, data=request.data, partial=True, context={'user': user})

        # Check if the data is valid
        if serializer.is_valid():
            # Save the updated user data
            serializer.save()
            return Response({'detail': 'Profile updated successfully!'}, status=status.HTTP_200_OK)

        # Return validation errors if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)