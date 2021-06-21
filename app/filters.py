from django_filters import rest_framework as filters
from .models import Product, Order, Review


class ProductFilter(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Product.objects.all()
    )

    name = filters.CharFilter(lookup_expr='iexact')
    desc = filters.CharFilter(lookup_expr='iexact')
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ('name', 'desc', 'price')


class OrderFilter(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Order.objects.all()
    )

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
    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Review.objects.all()
    )

    created_at = filters.DateFromToRangeFilter()

    reviews = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Review.objects.all()
    )

    creator = filters.ModelMultipleChoiceFilter(
        field_name="user",
        to_field_name="user",
        queryset=Order.creator.objects.all()
    )

    class Meta:
        model = Review
        fields = ('id', 'reviews', 'created_at')

