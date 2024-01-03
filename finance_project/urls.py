"""
URL configuration for finance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from finance_app import views


urlpatterns = [
    path("", views.index, name="inicio"),
    path(
        "redirect-to-analysis/", views.redirect_to_analysis, name="redirect_to_analysis"
    ),
    path("fundamentals/", views.fundamentals_view, name="fundamentals"),
    path("quant-analysis/", views.quants_view, name="quant_analysis"),
    path("admin/", admin.site.urls),
]
