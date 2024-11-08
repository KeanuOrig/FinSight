"""
URL configuration for stock_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),           # Core app (e.g., home page)
    path('stocks/', include('stocks.urls')),  # Stocks app
    path('ai/', include('ai_analysis.urls')), # AI Analysis app
    path('api/', include('api.urls')),        # API app
    path('users/', include('users.urls')),    # User management app
    path('reports/', include('reports.urls')) # Reports app
]
