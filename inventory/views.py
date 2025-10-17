from rest_framework import viewsets, permissions, filters, generics, serializers
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
)


# ----------------------
# Custom Permission
# ----------------------
class IsBarManagerOrReadOnly(permissions.BasePermission):
    """
    Allow full CRUD for superusers/managers.
    Regular staff can only edit the 'sold' field.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Staff can only edit 'sold' field
        if request.method in ['PATCH', 'PUT']:
            allowed_fields = ['sold']
            return set(request.data.keys()).issubset(allowed_fields)

        # Read-only for GET, HEAD, OPTIONS
        return request.method in permissions.SAFE_METHODS


# ----------------------
# ViewSets
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


class BarStockViewSet(viewsets.ModelViewSet):
    queryset = BarStock.objects.all()
    serializer_class = BarStockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBarManagerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['record_date', 'closing_stock']


class ItemValueViewSet(viewsets.ModelViewSet):
    queryset = ItemValue.objects.all()
    serializer_class = ItemValueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# ----------------------
# Authentication Views
# ----------------------
class CustomAuthToken(ObtainAuthToken):
    """
    Returns user info + token when login is successful.
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
    Deletes the user's token on logout.
    """
    token = getattr(request.user, 'auth_token', None)
    if token:
        token.delete()
    return Response({"message": "Successfully logged out"})


# ----------------------
# User Registration
# ----------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)
        # Automatically create token for the new user
        Token.objects.create(user=user)
        return user


class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    Returns 201 Created + token.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
