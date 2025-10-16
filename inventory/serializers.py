from rest_framework import serializers
from .models import StoreItem, StoreItemHistory, BarStock, ItemValue


class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'


class StoreItemHistorySerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = StoreItemHistory
        fields = '__all__'


class BarStockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = BarStock
        fields = '__all__'


class ItemValueSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item', read_only=True)

    class Meta:
        model = ItemValue
        fields = '__all__'
