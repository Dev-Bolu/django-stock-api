from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreItemViewSet,
    StoreItemHistoryViewSet,
    BarStockViewSet,
    ItemValueViewSet,
    logout_user,
    CustomAuthToken
)

router = DefaultRouter()
router.register(r'store-items', StoreItemViewSet)
router.register(r'store-history', StoreItemHistoryViewSet)
router.register(r'bar-stock', BarStockViewSet)
router.register(r'item-value', ItemValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', logout_user, name='api_logout'),
]
