from django.urls import path
from . import views
app_name = 'dashboard'

urlpatterns = [
    path("instructor/", views.dashboard_instructor, name="dashboard_instructor"),
    path("api/horarios/", views.horarios_json, name="horarios_json"),
    
]