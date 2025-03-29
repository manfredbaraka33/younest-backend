

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['username', 'email', 'bio', 'profile_image', 'is_staff',]
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_image', 'followed_shops','saved_products_or_services')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_image', 'followed_shops','saved_products_or_services')}),
    )

admin.site.register(MyUser, MyUserAdmin)

