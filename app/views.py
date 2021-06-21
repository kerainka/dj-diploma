from django.shortcuts import render, reverse
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Product, Order, Review, Collection
from .permissions import AllowOnly
from .serializers import ProductSerializer, OrderSerializer, ReviewSerializer, CollectionSerializer
from .filters import ProductFilter, OrderFilter, ReviewFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    permission_classes_by_action = {'retrieve': [AllowAny],
                                    'list': [AllowAny],
                                    'create': [IsAdminUser],
                                    'update': [IsAdminUser],
                                    'destroy': [IsAdminUser],
                                    'default': [IsAuthenticated]
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('order').all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    permission_classes_by_action = {'retrieve': [AllowOnly],
                                    'list': [IsAuthenticated],
                                    'create': [IsAuthenticated],
                                    'update': [IsAdminUser],
                                    'destroy': [IsAdminUser]
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('review').all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter

    permission_classes_by_action = {'retrieve': [AllowAny],
                                    'list': [IsAuthenticated],
                                    'create': [IsAuthenticated],
                                    'update': [AllowOnly],
                                    'destroy': [AllowOnly],
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('products').all()
    serializer_class = CollectionSerializer

    permission_classes_by_action = {'retrieve': [AllowAny],
                                    'list': [AllowAny],
                                    'create': [IsAdminUser],
                                    'update': [IsAdminUser],
                                    'destroy': [IsAdminUser],
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]
