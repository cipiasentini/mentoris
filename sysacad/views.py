from django.shortcuts import render
from .models import Materia

def index(request):
    # Lista de alumnos
    materias = Materia.objects.all()

    context = {'materias': materias, 'nbar': 'sysacad'}
    return render(request, 'sysacad/index.html', context)