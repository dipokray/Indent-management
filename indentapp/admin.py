from django.contrib import admin
from .models import Profile, Category, Product, Indent


# # Register your models here

class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone',  'birth_date', 'gender', 'dept')


admin.site.register(Profile, AdminProfile)

admin.site.register(Category)


class AdminProduct(admin.ModelAdmin):
    list_display = ('product_category', 'product_name')


admin.site.register(Product, AdminProduct)


class AdminIndent(admin.ModelAdmin):
    list_display = (
        'user', 'category', 'product', 'product_price', 'product_quantity', 'requested_amount', 'paid_amount',
        'balance')


admin.site.register(Indent, AdminIndent)
