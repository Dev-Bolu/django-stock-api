from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreItemViewSet, StoreItemHistoryViewSet, BarStockViewSet, ItemValueViewSet

router = DefaultRouter()
router.register(r'store-items', StoreItemViewSet)
router.register(r'store-history', StoreItemHistoryViewSet)
router.register(r'bar-stock', BarStockViewSet)
router.register(r'item-value', ItemValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
