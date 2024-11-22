from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, StockData
from .serializers import StockSerializer, StockDataSerializer
from rest_framework import generics
from stock_analysis.ai_analysis.chatgpt_service import get_chatgpt_response
from stock_analysis.ai_analysis.gemini_service import get_gemini_response
from stock_analysis.utils.utils import api_response
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime
import re

# Create your views here.

class StockDetailView(APIView):
    """
    Retrieve stock details by symbol.
    """
    def get(self, request, symbol):
        
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        
        try:
            
            stock = Stock.objects.prefetch_related('data').get(symbol=symbol.upper())
            stock_data = stock.data.order_by('date').all()
            
            if date_from and date_to:
                
                date_from = parse_date(date_from)
                date_to = parse_date(date_to)
                
                if date_from and date_to:
                    stock_data = stock_data.filter(date__range=[date_from, date_to])
                else:
                    return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = StockSerializer(stock, context={'include_data': False})
            response_data = serializer.data
            response_data['data'] = StockDataSerializer(stock_data, many=True).data
            
            return Response(response_data, status=status.HTTP_200_OK)
        
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
                return JsonResponse({"error": "Stock data not found for the given symbol."}, status=status.HTTP_404_NOT_FOUND)

            # Prepare the data for analysis (you can pass the raw data or formatted data)
            formatted_stock_data = self.format_stock_data(stock_data)

            # Call AI analysis service
            analysis = self.analyze_stock_data(formatted_stock_data, stock.company_name)

            return JsonResponse({
                "symbol": symbol, 
                "prediction": analysis["prediction"],
                "rating": analysis["rating"],
            })
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        # todo: Feature 4. Technical analysis focusing on indicators such as moving averages, RSI, or MACD.
        prompt = f"""
        Analyze the stock data for {company_name} in the Philippines and provide a technical investment recommendation. Base your analysis on the following criteria:

        1. Identify key insights from trends and patterns observed in the data provided.
        2. Assess both short-term and long-term trends, suggesting potential buying and selling price ranges. Even if the data appears limited, provide your best estimate based on the available information.
        3. Provide a clear investment recommendation in the format: **[Buy Rating: <rating>]**, where <rating> is one of the following: "Strong Buy", "Buy", "Hold", "Sell", or "Strong Sell".
        4. Justify your recommendation with clear reasoning derived directly from the provided data. Avoid statements like "more data is needed" or "insufficient information"; instead, offer the most actionable insights possible within the given dataset.

        Ensure the response is concise, actionable, and follows the requested format.

        Stock Data:
        {stock_data}"""

        # Get a response from AI
        prediction = get_gemini_response(prompt)
        ''' prediction = "The provided data shows a generally downward trend in the PSEi index from April 2022 to November 2024, with some periods of consolidation and minor upward movements. The absence of volume data for most of the period makes a definitive technical analysis challenging.  However, we can observe some broader trends:\n\n**Trends and Patterns:**  The long-term trend is bearish.  While there are short-term fluctuations, the overall direction has been downwards.  There's no clear discernible pattern like a head and shoulders or double bottom to suggest a potential reversal.\n\n\n**Technical Analysis Limitations:** Without volume data, it's impossible to confirm the strength of price movements.  Moving averages would be useful for trend confirmation but are hard to calculate reliably with many 0 volume days.  RSI and MACD would also benefit from complete volume data to paint an accurate picture of momentum and potential overbought/oversold conditions.  The very low or zero volume on many days is highly unusual and may indicate data issues or very low liquidity in the market during those periods.\n\n\n**Recommendation:** Given the predominantly downward trend observed and the limitations imposed by insufficient data, a **[Buy Rating: Hold]** is recommended.  It's prudent to wait for more data, particularly volume data, to perform a robust technical analysis and to understand the market conditions better before taking a buy or sell decision. The low volume itself makes the index less attractive, as there might be difficulties in entering or exiting positions quickly.  Further investigation is required to determine the cause of the zero volume days and assess if the data itself is reliable.\n" '''
        
        pattern = r'\[\s*Buy Rating:\s*(.*?)\s*\]'
        rating = re.findall(pattern, prediction)
        
        analysis = {
            "prediction": prediction,
            "rating": rating[0] if rating else 'None'
        }
        return analysis

class StockListView(generics.ListAPIView):
    """
    ListCreateAPIView - List all Stocks
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


 
    