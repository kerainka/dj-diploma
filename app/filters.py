from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .models import Product, Order, ProductReview


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    desc = filters.CharFilter(lookup_expr='icontains')
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ('name', 'desc', 'price')


class OrderFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=Order.STATUS)

    products = filters.ModelMultipleChoiceFilter(
        field_name="names",
        to_field_name="name",
        queryset=Product.objects.all()
    )

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'updated_at', 'products')


class ReviewFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()

    creator = filters.ModelMultipleChoiceFilter(
        field_name="user",
        to_field_name="user",
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = ProductReview
        fields = ('id', 'review_product', 'created_at')

