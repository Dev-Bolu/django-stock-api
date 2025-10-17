from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

from .models import StoreItem, StoreItemHistory, BarStock, ItemValue
from .serializers import (
    StoreItemSerializer,
    StoreItemHistorySerializer,
    BarStockSerializer,
    ItemValueSerializer,
)


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class StoreItemHistoryViewSet(viewsets.ModelViewSet):
    queryset = StoreItemHistory.objects.all()
    serializer_class = StoreItemHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class BarStockViewSet(viewsets.ModelViewSet):
    queryset = BarStock.objects.all()
    serializer_class = BarStockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ItemValueViewSet(viewsets.ModelViewSet):
    queryset = ItemValue.objects.all()
    serializer_class = ItemValueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]




class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication endpoint that returns the user's authentication token along with
    additional user information upon successful login.
    def post(self, request):
        # Authenticate user and return token along with user info
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
            "token": "<auth_token>",
            "user_id": 1,
            "username": "exampleuser"
        }
    """
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
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
    Deletes the user's token on logout
    """
    token = getattr(request.user, 'auth_token', None)
    if token:
        token.delete()
    return Response({"message": "Successfully logged out"})
