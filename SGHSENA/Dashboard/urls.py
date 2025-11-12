from django.urls import path
from .views import DashboardInstructorView, DashboardCoordinadorView

app_name = 'dashboard'

urlpatterns = [
    path('instructor/', DashboardInstructorView.as_view(), name='dashboard_instructor'),
    path('coordinador/', DashboardCoordinadorView.as_view(), name='dashboard_coordinador'),
]
