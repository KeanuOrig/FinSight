from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, StockData
from .serializers import StockSerializer
from rest_framework import generics
from stock_analysis.ai_analysis.chatgpt_service import get_chatgpt_response
from stock_analysis.ai_analysis.gemini_service import get_gemini_response

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
    def get(self, request, symbol, *args, **kwargs):
        try:

            # Retrieve the stock data for the symbol (e.g., last 30 days)
            stock = Stock.objects.get(symbol=symbol.upper())
            stock_data = StockData.objects.filter(stock__symbol=symbol.upper()).order_by('-date').all()
           
            if not stock_data:
                return JsonResponse({"error": "Stock data not found for the given symbol."}, status=404)

            # Prepare the data for analysis (you can pass the raw data or formatted data)
            formatted_stock_data = self.format_stock_data(stock_data)
            return JsonResponse({"prediction": formatted_stock_data})
            # Call AI analysis service
            prediction = self.analyze_stock_data(formatted_stock_data, stock.company_name)

            return JsonResponse({"symbol": symbol, "prediction": prediction})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    def format_stock_data(self, stock_data):
        # Convert stock data into a readable format for the AI model
        """ formatted_data = "Date | Open | Close | High | Low | Volume\n"
        for record in stock_data:
            formatted_data += f"{record.date} | {record.open_price} | {record.close_price} | {record.high_price} | {record.low_price} | {record.volume}\n"
        return formatted_data """
        formatted_data = "Date | Open | Close | High | Low | Volume\n"
        for record in stock_data:
            formatted_data += f"{record.date} | {record.open_price} | {record.close_price} | {record.high_price} | {record.low_price} | {record.volume}\n"
        return formatted_data

    def analyze_stock_data(self, stock_data, company_name):
        # Generate a prompt based on the stock data
        prompt = f"""This is the stock is for {company_name} in the Philippines. Analyze the following stock data for technical insights and provide an investment recommendation. Include the following:
        1. Key insights from trends and patterns.
        2. Technical analysis focusing on indicators such as moving averages, RSI, or MACD.
        3. A clear recommendation (BUY, HOLD, or SELL), with reasoning.

        Stock Data:
        {stock_data}"""

        # Get a response from ChatGPT
        analysis = get_gemini_response(prompt)

        return analysis

class StockListView(generics.ListAPIView):
    """
    ListCreateAPIView - List all Stocks
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


 
    