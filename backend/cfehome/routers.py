from rest_framework.routers import DefaultRouter
from products.viewsets import ProductViewSet,ProductGenericViewSet


router = DefaultRouter()
router.register('products',ProductGenericViewSet,basename='products')

# viwsets supports a lot of urls by default and its difficult to understand which ones at first
urlpatterns = router.urls