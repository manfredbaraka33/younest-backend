from django.contrib import admin
from .models import ForSaleProduct,ProductImage

class ProductImageInline(admin.TabularInline):  # TabularInline for a compact inline form
    model = ForSaleProduct.image.through  # Since it's a ManyToManyField, use the through model
    extra = 1  # Number of blank forms for additional images

class ProductForSaleAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'description')

admin.site.register(ForSaleProduct,ProductForSaleAdmin)
admin.site.register(ProductImage)
