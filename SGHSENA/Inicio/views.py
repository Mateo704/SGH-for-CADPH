from django.shortcuts import render
from django.views.generic import TemplateView
from Models.models import Jornadas
# Create your views here.
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name="html/index.html"

class Ini(TemplateView):
    template_name = "html/inicial.html"
