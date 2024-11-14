from django.urls import path
from . import views

urlpatterns = [
    path('pse/<str:symbol>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('list', views.StockListView.as_view(), name='stock_list'),
    path('predict/<str:symbol>', views.StockPredictionView.as_view(), name='stock_prediction'),
]