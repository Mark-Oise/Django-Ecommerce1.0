from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Brand, Category


class ProductListView(ListView):
    """
    View for displaying a list of products with filtering and sorting options.
    """

    model = Product
    template_name = 'store/product-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        """
        Customizes the queryset based on filtering and sorting parameters from the request.
        """
        queryset = super().get_queryset()

        # Filter by category
        category_slugs = self.request.GET.getlist('categories')
        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        # Filter by brand
        brand_slugs = self.request.GET.getlist('brands')
        if brand_slugs:
            queryset = queryset.filter(brand__slug__in=brand_slugs)

        # Filter by price
        minimum_price = self.request.GET.get('minimum_price')
        maximum_price = self.request.GET.get('maximum_price')
        if minimum_price and maximum_price:
            queryset = queryset.filter(price__gte=minimum_price, price__lte=maximum_price)
        elif minimum_price:
            queryset = queryset.filter(price__gte=minimum_price)
        elif maximum_price:
            queryset = queryset.filter(price__lte=maximum_price)

        # Filter by condition
        condition_slugs = self.request.GET.getlist('conditions')
        if condition_slugs:
            queryset = queryset.filter(condition__in=condition_slugs)

        # Sort by price
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'ascending-price':
            queryset = queryset.order_by('price')
        elif sort_by == 'descending-price':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds additional context data for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['conditions'] = Product.CONDITION_CHOICES

        return context

    def paginate_products(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')

        try:
            if page is None or page == '':
                products = paginator.page(1)
            else:
                products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, 'store/product-list-partial.html', {
            'products': products
        })


class ProductDetailView(DetailView):
    """
    View for displaying details of a specific product.
    """

    model = Product
    template_name = 'store/product-detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        """
        Adds additional context data for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Retrieve related products of the same category
        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(pk=product.pk)[:6]

        # # Retrieve category and brand objects for the product
        # context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        # context['brand'] = Brand.objects.get(slug=self.kwargs['brand_slug'])
        return context


class ProductSearchView(ListView):
    """
    View for searching products based on a query string.
    """

    model = Product
    template_name = 'store/partials/product-items.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Retrieves the queryset based on the query string provided in the request.
        """
        query = self.request.GET.get('q')
        if query:
            # Filter products by name containing the query string
            queryset = Product.objects.filter(
                Q(name__icontains=query)
            )
        else:
            # If no query is provided, return all products
            queryset = Product.objects.all()
        return queryset
