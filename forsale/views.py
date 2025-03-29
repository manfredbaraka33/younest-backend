from django.shortcuts import render
from rest_framework import generics,permissions
from .models import ForSaleProduct
from .serializers import ForSaleproductSerializer
from django.http import JsonResponse
from user.models import MyUser
from rest_framework import status
from rest_framework.response import Response
from .models import ProductImage
from rest_framework.parsers import MultiPartParser,FormParser


class ProductForSaleListCreateAPIView(generics.ListCreateAPIView):
    queryset = ForSaleProduct.objects.all()
    serializer_class = ForSaleproductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        
        user_id = request.data.get('seller')
        try:
            user_instance = MyUser.objects.get(id=user_id)  
        except MyUser.DoesNotExist:
            return Response({'detail': f'user {user_id} not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file uploads
        files = request.FILES.getlist('images')  # Get the list of files

        # Remove images from the data to prevent passing them directly to the model
        data = {
            key: value for key, value in request.data.items() if key != 'images'
        }

        # Use serializer to create the product and attach the shop
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # Save the product or service instance without the images
            product_or_service_instance = serializer.save(seller=user_instance)

            # Associate the images with the product (since image is a ManyToManyField)
            for file in files:
                product_image = ProductImage.objects.create(image=file)
                product_or_service_instance.image.add(product_image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

forsaleProduct = ProductForSaleListCreateAPIView.as_view()



def fetch_all_forsale(request):
    products = ForSaleProduct.objects.all()
   
    baseurl = "http://127.0.0.1:8000"
    
    # Prepare response data
    data = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'created_at': p.created_at,
            'location':p.location,
            'image': [
                {'id': idx + 1, 'image': baseurl + img.image.url}  # Access the image field within ProductImage
                for idx, img in enumerate(p.image.all())  # p.image.all() returns related ProductImage objects
            ] if p.image.exists() else [],
            'seller': {
                'id': p.seller.id,
                'name': p.seller.username
            }
        }
        for p in products
    ]
    
    return JsonResponse({'products': data}, safe=False)


class ForSaleDetailAPIView(generics.RetrieveAPIView):
    queryset=ForSaleProduct.objects.all()
    serializer_class=ForSaleproductSerializer

for_sale_detail = ForSaleDetailAPIView.as_view()


class ForSaleUpdateAPIView(generics.UpdateAPIView):
    queryset=ForSaleProduct.objects.all()
    serializer_class = ForSaleproductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        # Get the product instance to update
        product_or_service_instance = self.get_object()

        # Handle file uploads (new images)
        files = request.FILES.getlist('images')  # Get the list of files

        # Make a copy of the request data and remove images to prevent passing them to the model
        data = request.data.copy()  # Make a copy of the data
        data.pop('images', None)  # Remove the images key

        # Use the serializer to update the product data
        serializer = self.get_serializer(product_or_service_instance, data=data, partial=True)
        if serializer.is_valid():
            # Save the updated product or service
            product_or_service_instance = serializer.save()

            # If new images were uploaded, delete existing ones and associate the new ones
            if files:
                # Remove the old images
                product_or_service_instance.image.clear()

                # Add new images
                for file in files:
                    product_image = ProductImage.objects.create(image=file)
                    product_or_service_instance.image.add(product_image)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

forsale_update=ForSaleUpdateAPIView.as_view()



class ForSaleDetleteAPIView(generics.DestroyAPIView):
    queryset=ForSaleProduct.objects.all()
    serializer_class = ForSaleproductSerializer
    permission_classes = [permissions.IsAuthenticated]

forsale_delete = ForSaleDetleteAPIView.as_view()


    