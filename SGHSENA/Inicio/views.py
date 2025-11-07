
from django.shortcuts import render

def calendario_view(request):
    return render(request, 'html/inicio.html')


