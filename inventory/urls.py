from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreItemViewSet,
    StoreItemHistoryViewSet,
    BarStockViewSet,
    ItemValueViewSet,
    
)
from . import views_auth  # import all auth views (API + browser)
from django.contrib.auth.decorators import login_required
from . import views_reports  # import report views
# -----------------------------
# DRF Router for API ViewSets
# -----------------------------
router = DefaultRouter()
router.register(r'store-items', StoreItemViewSet, basename='storeitem')
router.register(r'store-history', StoreItemHistoryViewSet, basename='storeitemhistory')
router.register(r'bar-stock', BarStockViewSet, basename='barstock')
router.register(r'item-value', ItemValueViewSet, basename='itemvalue')

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # 1️⃣ All your API endpoints (CRUD)
    path('', include(router.urls)),

    # 2️⃣ API Authentication routes (for Postman/curl clients)
    path('login/', views_auth.CustomAuthToken.as_view(), name='api_login'),
    path('logout/', views_auth.logout_user, name='api_logout'),
    path('register/', views_auth.UserRegisterView.as_view(), name='api_register'),

    # 3️⃣ Browser-based login/logout/register (for normal web users)
    path('accounts/login/', views_auth.user_login_view, name='login'),
    path('accounts/logout/', views_auth.user_logout_view, name='logout'),
    path('accounts/register/', views_auth.user_register_view, name='register'),
    
     # Home/dashboard page
    path('accounts/home/', views_auth.home_view, name='home'),
    path('reports/daily/', views_reports.daily_sales_summary, name='daily-sales-summary'),
    path('reports/weekly/', views_reports.weekly_sales_summary, name='weekly-sales-summary'),
    path('reports/monthly/', views_reports.monthly_sales_summary, name='monthly-sales-summary'),

]