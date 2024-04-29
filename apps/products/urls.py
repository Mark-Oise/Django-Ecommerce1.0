from django.urls import path
from .views import ProductListView, ProductDetailView, ProductSearchView
from .utils import clear_filters

app_name = 'store'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<slug:category_slug>/<slug:brand_slug>/<slug:product_slug>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('search/', ProductSearchView.as_view(), name='search'),

    path('', clear_filters, name='clear_filters')
]
