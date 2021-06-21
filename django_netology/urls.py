"""django_netology URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views


router1 = DefaultRouter()
router1.register("api/v1/products", views.ProductViewSet, basename="products")

router2 = DefaultRouter()
router2.register("api/v1/product-reviews", views.ReviewViewSet, basename="product-reviews")

router3 = DefaultRouter()
router3.register("api/v1/orders", views.OrderViewSet, basename="orders")

router4 = DefaultRouter()
router4.register("api/v1/product-collections", views.CollectionViewSet, basename="product-collections")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router1.urls), name='products'),
    path('', include(router2.urls), name='reviews'),
    path('', include(router3.urls), name='orders'),
    path('', include(router4.urls), name='collections'),
]
