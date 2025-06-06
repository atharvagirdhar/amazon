from django.contrib import admin
from .models import CustomUser, UserProfile, Country, City, Address, Category, SubCategory,Products, ProductImage, Carts, Wishlist, Order
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    def get_list_display(Self,request):
        return [field.name for field in CustomUser._meta.fields]
        
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in UserProfile._meta.fields]
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Country._meta.fields]
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in City._meta.fields]
    
@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Address._meta.fields]
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Category._meta.fields]
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in SubCategory._meta.fields]
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Products._meta.fields]
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in ProductImage._meta.fields]

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Carts._meta.fields]
    
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Wishlist._meta.fields]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_list_display(Self,request):
        return [field.name for field in Order._meta.fields]
    

    
admin.site.site_header = "Amazon Admin"
admin.site.site_title = "App"
admin.site.index_title = "Amazon"