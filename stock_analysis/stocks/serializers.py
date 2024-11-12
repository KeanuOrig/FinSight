from rest_framework import serializers
from .models import Stock, StockData

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model: Stock = Stock
        fields: list  = ['id', 'symbol', 'company_name', 'industry', 'sector']


class StockDataSerializer(serializers.ModelSerializer):
    
    stock = StockSerializer()  # Use nested serializer to include stock details in response
    
    class Meta:
        model: StockData = StockData
        fields: list = '__all__'