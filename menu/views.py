from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Alumno, Tutor
from sysacad.models import (Persona as SysacadPersona, Alumno as SysacadAlumno)
from .forms import (agregarAlumnoForm,  buscarAlumnoForm)
from .forms import (agregarTutorForm, buscarTutorForm, agregarTutorPersonalizadoForm)
from django.contrib.auth.models import User


def index(request):
    # # Contador de numero de visitas de la sesion
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1
    #
    # # Lista de alumnos
    # alumnos = Alumno.objects.order_by('-fecha_alta')
    #
    # context = {'alumnos': alumnos, 'num_visits': num_visits, 'nbar': 'index'}
    # return render(request, 'menu/index.html', context)
    if request.method == 'POST':
        form = buscarAlumnoForm(request.POST)
        if form.is_valid():
            legajo = form.cleaned_data['legajo_alumno']
            if legajo.isnumeric():
                try:
                    alumno = Alumno.objects.get(legajo=legajo)
                except:
                    return render(request, 'menu/index.html', {'form': form, 'not_found': True, 'nbar': 'index'})
            else:
                try:
                    alumno = Alumno.objects.get(nombre__contains=legajo)
                except:
                    return render(request, 'menu/index.html', {'form': form, 'not_found': True, 'nbar': 'index'})
            return render(request, 'menu/index.html', {'form': form, 'alumno_inst': alumno, 'nbar': 'index'})
    else:
        form = buscarAlumnoForm()
        return render(request, 'menu/index.html', {'form': form, 'nbar': 'index'})


def buscarAlumno(request):
    if request.method == 'POST':
        form = buscarAlumnoForm(request.POST)
        if form.is_valid():
            legajo = form.cleaned_data['legajo_alumno']
            if legajo.isnumeric():
                try:
                    alumno = Alumno.objects.get(legajo=legajo)
                except:
                    return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            else:
                try:
                    alumno = Alumno.objects.get(nombre__contains=legajo)
                except:
                    return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            return render(request, 'menu/buscar-alumno.html', {'form': form, 'alumno_inst': alumno, 'nbar': 'alumnos'})
    else:
        form = buscarAlumnoForm()
        return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'alumnos'})

@login_required
def agregarAlumno(request):
    if request.method == 'POST':
        form = agregarAlumnoForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            observaciones = form.cleaned_data['observaciones']
            try:
                persona_sysacad = SysacadPersona.objects.get(pk = dni)
                alumno_sysacad = SysacadAlumno.objects.get(pk = dni)
            except SysacadAlumno.DoesNotExist:
                return render(request, 'menu/alta-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            nuevo_alumno = Alumno(
                nombre=persona_sysacad.nombre,
                dni=dni,
                legajo=alumno_sysacad.legajo,
                observaciones=observaciones
            )
            Alumno.save(nuevo_alumno)
            form = agregarAlumnoForm()
            return render(request, 'menu/alta-alumno.html', {'form': form, 'alumno': nuevo_alumno, 'success': True, 'nbar': 'alumnos'})
    else:
        form = agregarAlumnoForm()
        return render(request, 'menu/alta-alumno.html', {'form': form, 'nbar': 'alumnos'})

@staff_member_required
def agregarTutor(request):
    if request.method == 'POST':
        form = agregarTutorForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                persona_sysacad = SysacadPersona.objects.get(pk=dni)
                alumno_sysacad = SysacadAlumno.objects.get(pk=dni)
            except SysacadPersona.DoesNotExist:
                return render(request, 'menu/alta-tutor.html',
                              {'form': agregarTutorPersonalizadoForm(request.POST),
                               'alta_manual': True, 'nbar': 'tutores'})
            nuevo_tutor = Tutor(
                nombre=persona_sysacad.nombre.rstrip(),
                dni=dni,
                legajo=alumno_sysacad.legajo,
                telefono=persona_sysacad.telefono,
                mail=persona_sysacad.mail.rstrip(),
                carrera=alumno_sysacad.especialid,
                tipo=form.cleaned_data['tipo'],
                horario=form.cleaned_data['horario'],
                # usuario=persona_sysacad.nombre.rsplit(None, 1)[-1],
                usuario=dni,
            )
            Tutor.save(nuevo_tutor)
            # agregarlo como usuario
            user = User.objects.create_user(dni, persona_sysacad.mail.rstrip(), 'pwd123')
            user.save()
            form = agregarTutorForm()
            return render(request, 'menu/alta-tutor.html', {'form': form, 'tutor': nuevo_tutor, 'success': True, 'nbar': 'tutores'})
    else:
        form = agregarTutorForm()
        return render(request, 'menu/alta-tutor.html', {'form': form, 'nbar': 'tutores'})

@staff_member_required
def agregarTutorPersonalizado(request):
    if request.method == 'POST':
        form = agregarTutorPersonalizadoForm(request.POST)
        if form.is_valid():
            nuevo_tutor = Tutor(
                nombre=form.cleaned_data['nombre'],
                dni=form.cleaned_data['dni'],
                telefono=form.cleaned_data['telefono'],
                mail=form.cleaned_data['mail'],
                tipo=form.cleaned_data['tipo'],
                horario=form.cleaned_data['horario'],
            )
            Tutor.save(nuevo_tutor)
            # agregarlo como usuario
            user = User.objects.create_user(form.cleaned_data['dni'], form.cleaned_data['mail'].rstrip(), 'pwd123')
            user.save()
            form = agregarTutorPersonalizadoForm()
            return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'tutor': nuevo_tutor, 'success': True, 'nbar': 'tutores'})
    else:
        form = agregarTutorPersonalizadoForm()
        return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'nbar': 'tutores'})

@login_required
def buscarTutor(request):
    if request.method == 'POST':
        form = buscarTutorForm(request.POST)
        if form.is_valid():
            try:
                tutor = Tutor.objects.get(dni=form.cleaned_data['dni'])
            except:
                return render(request, 'menu/buscar-tutor.html', {'form': form, 'not_found': True, 'nbar': 'tutores'})
            return render(request, 'menu/buscar-tutor.html', {'form': form, 'tutor': tutor, 'nbar': 'tutores'})
    else:
        form = buscarTutorForm()
        return render(request, 'menu/buscar-tutor.html', {'form': form, 'nbar': 'tutores'})