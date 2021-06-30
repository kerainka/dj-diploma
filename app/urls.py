from rest_framework.routers import SimpleRouter

from .views import OrderViewSet, ProductViewSet, ReviewViewSet, CollectionViewSet

router = SimpleRouter()

router.register('orders', OrderViewSet, basename='orders')
router.register('products', ProductViewSet, basename='products')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('collections', CollectionViewSet, basename='collections')

urlpatterns = router.urls
