from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('book/', views.book_spa, name='book_spa'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
