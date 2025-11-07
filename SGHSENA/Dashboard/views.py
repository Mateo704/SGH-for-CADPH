from django.shortcuts import render
from django.views.generic import TemplateView
from Models.models import Jornadas

def dashboard(request):
    jornadas=Jornadas.objects.all()
    return render(request, 'dashboard/panel1.html',{'jornadas':jornadas})