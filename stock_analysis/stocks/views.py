from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer
from rest_framework import generics
# Create your views here.

class StockDetailView(APIView):
    """
    Retrieve stock details by symbol.
    """
    def get(self, request, symbol):
        try:
            stock = Stock.objects.get(symbol=symbol.upper())
            serializer = StockSerializer(stock)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)


class StockPredictionView(APIView):
    """
    Predict the future price of a stock.
    """
    def post(self, request, symbol):
        # Retrieve stock data
        try:
            stock = Stock.objects.get(symbol=symbol.upper())
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        # Example prediction logic (replace with actual model prediction)
        # features = extract_features(stock)  # Processed features for prediction
        # predicted_price = predict_stock_price(features)  # Predicted price

        predicted_price = stock.last_price * 1.05  # Mock prediction (5% increase)

        return Response({
            "symbol": stock.symbol,
            "predicted_price": predicted_price
        }, status=status.HTTP_200_OK)

class StockListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView - List all Stocks or create a new one
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView - Retrieve, update, or delete a single Stock
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer