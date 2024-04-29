from django.contrib import admin
from .models import Category, Brand, Product, ProductImage


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']
    readonly_fields = ['alt_text']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'brand', 'condition', 'description',
        'price', 'quantity', 'available', 'created',
    ]
    list_filter = [
        'brand', 'available', 'category',
        'created', 'updated'
    ]
    list_editable = [
        'description', 'quantity', 'price', 'available'
    ]
    inlines = [ProductImageInline]
