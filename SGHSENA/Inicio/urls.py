from django.urls import path
from . import views

urlpatterns = [
    path('calendario/', views.calendario_view, name='calendario'),
]