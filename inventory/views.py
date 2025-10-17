# inventory/views.py
from rest_framework import viewsets, filters, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import StoreItem, StoreItemHistory, BarStock, ItemValue
from .serializers import (
    StoreItemSerializer,
    StoreItemHistorySerializer,
    BarStockSerializer,
    ItemValueSerializer,
    UserRegisterSerializer,
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
    authentication_classes = [TokenAuthentication]
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


# ----------------------
# Authentication Views
# ----------------------
class CustomAuthToken(ObtainAuthToken):
    """
    Returns token + user info when login succeeds.
    """
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Deletes user's token on logout.
    """
    token = getattr(request.user, 'auth_token', None)
    if token:
        token.delete()
    return Response({"message": "Successfully logged out"})


# ----------------------
# User Registration View
# ----------------------
class UserRegisterView(generics.CreateAPIView):
    """
    Register new user and return auth token.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response
