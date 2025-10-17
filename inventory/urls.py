from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreItemViewSet,
    StoreItemHistoryViewSet,
    BarStockViewSet,
    ItemValueViewSet,
    logout_user,
    CustomAuthToken,
    UserRegisterView,
)

# ----------------------
# Router for ViewSets
# ----------------------
router = DefaultRouter()
router.register(r'store-items', StoreItemViewSet, basename='storeitem')
router.register(r'store-history', StoreItemHistoryViewSet, basename='storeitemhistory')
router.register(r'bar-stock', BarStockViewSet, basename='barstock')
router.register(r'item-value', ItemValueViewSet, basename='itemvalue')

# ----------------------
# URL Patterns
# ----------------------
urlpatterns = [
    path('', include(router.urls)),               # All ViewSets
    path('auth/login/', CustomAuthToken.as_view(), name='api_login'),  # Login
    path('auth/logout/', logout_user, name='api_logout'),              # Logout
    path('auth/register/', UserRegisterView.as_view(), name='api_register'),  # Registration
]
