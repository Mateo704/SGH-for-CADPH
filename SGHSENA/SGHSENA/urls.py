
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required   # ✅ IMPORTANTE
from django.shortcuts import render                         # ✅ IMPORTANTE
from Login import views as login_views
from Inicio.views import *
from Login.urls import *
from consultas.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    # Login del superusuario
    #path('login-admin/', login_views.login_admin_view, name='login_admin'),

    # Login del personal (instructores y coordinadores)
    path('login/', login_views.login_view, name='login_personal'),
    path("dashboard/", include("Dashboard.urls", namespace="dashboard")),
    path('home/', HomeHours.as_view(), name="homehours"),
    path('consultas/', Panel_administrativo.as_view(), name='panel')
]
