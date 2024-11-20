from rest_framework import serializers
from .models import Stock, StockData
import pytz
from datetime import datetime

class StockDataSerializer(serializers.ModelSerializer):
    
    """ stock = StockSerializer()  # Use nested serializer to include stock details in response """
    date = serializers.SerializerMethodField()
    
    class Meta:
        model: StockData = StockData
        fields: list = ['id', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']
            
    def get_date(self, obj):
        """Return the date as a Unix timestamp in milliseconds."""
        if obj.date:
            date_obj = datetime.combine(obj.date, datetime.min.time())
            
            # Set the timezone to UTC (or any other fixed timezone) explicitly
            date_obj = pytz.UTC.localize(date_obj) if date_obj.tzinfo is None else date_obj

            # Convert to timestamp in milliseconds
            timestamp_ms = int(date_obj.timestamp() * 1000)
            return timestamp_ms
    
        return None

class StockSerializer(serializers.ModelSerializer):
    
    data = StockDataSerializer(many=True, read_only=True) 
     
    class Meta:
        model: Stock = Stock
        fields: list  = ['id', 'symbol', 'company_name', 'industry', 'symbol', 'data']
        
    def to_representation(self, instance):
        """
        Modify the to_representation method to conditionally include `data`
        based on the context (e.g., `include_data` query parameter).
        """
        # Get the context (e.g., `include_data` flag) from the view
        include_data = self.context.get('include_data', False)
        
        # Call the parent method to get the default representation
        representation = super().to_representation(instance)

        # Conditionally include the 'data' field based on `include_data`
        if not include_data:
            representation.pop('data', None)  # Remove 'data' if not needed

        return representation
