from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.
class Panel_administrativo(TemplateView):
    template_name= 'html/consultas/panel_consultas.html'