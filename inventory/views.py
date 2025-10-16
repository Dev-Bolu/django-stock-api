from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
    Returns user info + token when login is successful
    """
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
    request.user.auth_token.delete()
    return Response({"message": "Successfully logged out"})
