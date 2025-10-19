# inventory/views.py
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue
from .serializers import (
    StoreItemSerializer,
    StoreItemHistorySerializer,
    BarStockSerializer,
    ItemValueSerializer,
)
from .permissions import IsBarManagerStaffOrReadOnly


# ----------------------
# StoreItem Views
# ----------------------
class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item']
    ordering_fields = ['store_in', 'store_out']


class StoreItemHistoryViewSet(viewsets.ModelViewSet):
    queryset = StoreItemHistory.objects.all()
    serializer_class = StoreItemHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# ----------------------
# BarStock View
# ----------------------
class BarStockViewSet(viewsets.ModelViewSet):
    queryset = BarStock.objects.all()
    serializer_class = BarStockSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsBarManagerStaffOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['record_date', 'closing_stock']


# ----------------------
# ItemValue View
# ----------------------
class ItemValueViewSet(viewsets.ModelViewSet):
    queryset = ItemValue.objects.all()
    serializer_class = ItemValueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBarManagerStaffOrReadOnly]
