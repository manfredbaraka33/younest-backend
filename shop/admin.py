from django.contrib import admin
from .models import Shop, ProductOrService, OfferOrPromotion, ProductImage

class ProductImageInline(admin.TabularInline):  # TabularInline for a compact inline form
    model = ProductOrService.image.through  # Since it's a ManyToManyField, use the through model
    extra = 1  # Number of blank forms for additional images

class ProductOrServiceAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'description')

admin.site.register(Shop)
admin.site.register(ProductOrService, ProductOrServiceAdmin)
admin.site.register(OfferOrPromotion)
admin.site.register(ProductImage)  # Register ProductImage to manage images directly if needed
