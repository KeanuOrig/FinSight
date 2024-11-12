from django.urls import path
from . import views

urlpatterns = [
    path('<str:symbol>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('predict/<str:symbol>', views.StockPredictionView.as_view(), name='stock_prediction'),
    path('', views.StockListCreateView.as_view(), name='stock-list-create'),
    path('retrieve-update-destroy/<int:pk>/', views.StockRetrieveUpdateDestroy.as_view(), name='stock_retrieve_update_destroy'),
]