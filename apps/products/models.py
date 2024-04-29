import os

from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify


# Helper functions for dynamic upload paths

def product_image_upload_path(instance, filename):
    """
    Generates a dynamic upload path for product images.
    Uploads to 'media/products/product_slug/filename'.
    """
    # Get the product's slug
    product_slug = instance.product.slug
    filename = os.path.basename(filename)
    # Construct the upload path with the product slug
    return f'products/{product_slug}/{filename}'


def profile_image_upload_path(instance, filename):
    """
    Generates a dynamic upload path for profile images.
    Uploads to 'media/accounts/profile_pictures/filename'.
    """


class Category(models.Model):
    """
    Model to represent product categories.
    """
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL of the category.
        """
        return reverse('store:product_list_by_category', args=[self.slug])


class Brand(models.Model):
    """
    Model to represent product brands.
    """
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL of the brand.
        """
        return reverse('store:product_list_by_brand', args=[self.slug])


class Product(models.Model):
    """
    Model to represent products.
    """
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=200, unique=True)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL of the product detail page.
        """
        return reverse('store:product_detail', args=[self.category.slug, self.brand.slug, self.slug])

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate the slug if it's not provided.
        """
        if not self.slug or self.name != str(self):
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """
    Model to represent product images.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True, help_text='Alt text for the Image')

    def __str__(self):
        return f'{self.product.name} Image'

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate alt text if it's not provided.
        """
        if not self.alt_text:
            # Generate alt text based on the product name and image index
            image_index = self.product.images.count() + 1  # Get the count of existing images
            self.alt_text = f"{slugify(self.product.name, allow_unicode=True)}- Image {image_index}"
            self.alt_text = f'{self.product.name} - Image {image_index}'
        super().save(*args, **kwargs)
