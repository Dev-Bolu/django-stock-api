# inventory/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue


# ------------------------------
# Store Serializers
# ------------------------------
class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'


class StoreItemHistorySerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = StoreItemHistory
        fields = '__all__'


# ------------------------------
# BarStock Serializer
# ------------------------------
class BarStockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = BarStock
        fields = '__all__'

    def get_fields(self):
        """
        If user is 'Staff', make all fields read-only except 'sold'.
        """
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            if request.user.groups.filter(name='Staff').exists():
                for field_name in fields.keys():
                    if field_name != 'sold':
                        fields[field_name].read_only = True
        return fields


# ------------------------------
# ItemValue Serializer
# ------------------------------
class ItemValueSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = ItemValue
        fields = '__all__'

    def get_fields(self):
        """
        If user is 'Staff', hide 'cost_price' and 'profit'.
        """
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            if request.user.groups.filter(name='Staff').exists():
                for field in ['cost_price', 'profit']:
                    fields.pop(field, None)
        return fields


# ------------------------------
# User Registration Serializer
# ------------------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create user and automatically generate auth token.
        """
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        return user
