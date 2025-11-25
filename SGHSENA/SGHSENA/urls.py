"""
URL configuration for SGHSENA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
    path('Dashboard/', include('Dashboard.urls')),
    # Paneles personalizados para instructores y coordinadores
    #path('panel-instructor/', login_required(lambda request: render(request, 'html/login-instructor/panel_instructor.html')), name='panel_instructor'),
    #path('panel-coordinador/', login_required(lambda request: render(request, 'html/login-coordinador/panel_coordinador.html')), name='panel_coordinador'),
    path('consultas/', Panel_administrativo.as_view(), name='panel')
]
