from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Alumno, Tutor, Intervencion, Tipo
from sysacad.models import (Persona as SysacadPersona, Alumno as SysacadAlumno, Materia as SysacadMateria, Alumcom as MateriaAlumno)
from .forms import (agregarAlumnoForm,  buscarAlumnoForm, editarAlumnoForm, agregarIntervencionForm, agregarIntervencionTipoForm)
from .forms import (agregarTutorForm, buscarTutorForm, agregarTutorPersonalizadoForm)
from django.contrib.auth.models import User
from datetime import datetime

@login_required
def editarAlumno(request, dni):
    try:
        alumno = Alumno.objects.get(dni=dni)
    except:
        return render(request, 'menu/editar-alumno.html', {'not_found': True, 'nbar': 'alumno'})
    form = editarAlumnoForm(instance=alumno)
    if request.method == 'POST':
        form = editarAlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-alumno.html', {'form': form, 'success': True, 'alumno_inst': alumno, 'nbar': 'alumno'})
        else:
            form = editarAlumnoForm(instance=alumno)
    return render(request, 'menu/editar-alumno.html', {'form': form, 'nbar': 'alumno'})


# def index(request):
#     # # Contador de numero de visitas de la sesion
#     # num_visits = request.session.get('num_visits', 0)
#     # request.session['num_visits'] = num_visits + 1
#     #
#     # # Lista de alumnos
#     # alumnos = Alumno.objects.order_by('-fecha_alta')
#     #
#     # context = {'alumnos': alumnos, 'num_visits': num_visits, 'nbar': 'index'}
#     # return render(request, 'menu/index.html', context)
#     if request.method == 'POST':
#         form = buscarAlumnoForm(request.POST)
#         if form.is_valid():
#             # form.id
#             id = form.cleaned_data['id']
#             if (int(id) < 999999):
#                 try:
#                     alumno = Alumno.objects.get(legajo=id)
#                 except:
#                     return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'index'})
#             else:
#                 try:
#                     alumno = Alumno.objects.get(dni=id)
#                 except:
#                     return render(request, 'menu/buscar-alumno.html',
#                                   {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#             return render(request, 'menu/buscar-alumno.html', {'form': form, 'alumno_inst': alumno, 'nbar': 'index'})
#         else:
#             return render(request, 'menu/buscar-alumno.html', {'form': form,  'nbar': 'index'})
#     else:
#         form = buscarAlumnoForm()
#         return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'index'})
def index(request):
    if request.method == 'GET':
        return render(request, 'menu/index.html', {'nbar': 'index'})

def buscarAlumno(request):
    if request.method == 'POST':
        form = buscarAlumnoForm(request.POST)
        if form.is_valid():
            # form.id
            id = form.cleaned_data['id']
            if (int(id) < 999999):
                try:
                    alumno = Alumno.objects.get(legajo=id)
                    intervenciones = Intervencion.objects.filter(alumno=alumno)
                    materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
                    materias = SysacadMateria.objects.all()
                except:
                    return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            else:
                try:
                    alumno = Alumno.objects.get(dni=id)
                except:
                    return render(request, 'menu/buscar-alumno.html',
                                  {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            return render(request, 'menu/buscar-alumno.html', {'form': form, 'materiasAlumno': materiaAlumno ,'alumno_inst': alumno,
                                                               'intervenciones': intervenciones, 'nbar': 'alumnos',
                                                               'materias': materias})
        else:
            return render(request, 'menu/buscar-alumno.html', {'form': form,  'nbar': 'alumnos'})
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
                # dni=persona_sysacad,
                legajo=alumno_sysacad.legajo,
                situacion_riesgo='Ninguna',
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
                # return agregarTutorPersonalizado(request)
                return redirect('menu:alta-tutor-personalizada')
                # return render(request, 'menu/alta-tutor-personalizada.html',
                #               {'form': agregarTutorPersonalizadoForm(request.POST),
                #                'alta_manual': True, 'nbar': 'tutores'})
            nuevo_tutor = Tutor(
                nombre=persona_sysacad.nombre.rstrip(),
                dni=persona_sysacad.numerodocu,
                legajo=alumno_sysacad.legajo,
                telefono=persona_sysacad.telefono.rstrip(),
                mail=persona_sysacad.mail.rstrip(),
                # carrera=alumno_sysacad.especialid,
                tipo=form.cleaned_data['tipo'],
                horario=form.cleaned_data['horario'],
                # usuario=persona_sysacad.nombre.rsplit(None, 1)[-1],
                usuario=dni,
            )
            Tutor.save(nuevo_tutor)
            # agregarlo como usuario
            contrasena = 'dni'+str(dni)[0:5]
            user = User.objects.create_user(dni, persona_sysacad.mail.rstrip(), contrasena)
            user.first_name = persona_sysacad.nombre.rstrip()
            user.save()
            form = agregarTutorForm()
            return render(request, 'menu/alta-tutor.html', {'form': form, 'tutor': nuevo_tutor, 'success': True, 'nbar': 'tutores'})
        else:
            return render(request, 'menu/alta-tutor.html', {'form': form,  'nbar': 'tutores'})
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
            contrasena = 'dni' + str(nuevo_tutor.dni)[0:5]
            user = User.objects.create_user(nuevo_tutor.dni, nuevo_tutor.mail.rstrip(), contrasena)
            user.first_name = nuevo_tutor.nombre.rstrip()
            user.save()
            form = agregarTutorPersonalizadoForm()
            return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'tutor': nuevo_tutor,
                                                                          'success': True, 'nbar': 'tutores'})
        else:
            return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'not_found': True, 'nbar': 'tutores'})
    else:
        form = agregarTutorPersonalizadoForm()
        return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'nbar': 'tutores'})

@login_required
def agregarIntervencion(request):
    if request.method == 'POST':
        form = agregarIntervencionForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                mat = SysacadMateria.objects.get(materia=form.cleaned_data['materia'].materia)
            except:
                if request.user.is_staff:
                    nueva_intervencion = Intervencion(
                        tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                        descripcion=str(form.cleaned_data['descripcion']),
                        tutor_asignado=Tutor.objects.get(dni=form.cleaned_data['tutor_asignado'].dni),
                        alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni)
                    )
                else:
                    nueva_intervencion = Intervencion(
                        tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                        descripcion=str(form.cleaned_data['descripcion']),
                        tutor_asignado=Tutor.objects.get(dni=request.user.username),
                        alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni)
                    )
                Intervencion.save(nueva_intervencion)
                form = agregarIntervencionForm()
                return render(request, 'menu/alta-intervencion.html', {'form': form, 'intervencion': nueva_intervencion,
                                                                       'success': True, 'nbar': 'intervencion'})
            if request.user.is_staff:
                nueva_intervencion = Intervencion(
                    tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                    descripcion=str(form.cleaned_data['descripcion']),
                    materia=mat,
                    tutor_asignado=Tutor.objects.get(dni=form.cleaned_data['tutor_asignado'].dni),
                    alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni)
                )
            else:
                nueva_intervencion = Intervencion(
                    tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                    descripcion=str(form.cleaned_data['descripcion']),
                    materia=mat,
                    tutor_asignado=Tutor.objects.get(dni=request.user.username),
                    alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni)
                )
            Intervencion.save(nueva_intervencion)
            form = agregarIntervencionForm(user=request.user)
            return render(request, 'menu/alta-intervencion.html', {'form': form, 'intervencion': nueva_intervencion,
                                                                   'success': True, 'nbar': 'intervencion'})
        else:
            return render(request, 'menu/alta-intervencion.html', {'form': form,  'nbar': 'intervencion'})
    else:
        form = agregarIntervencionForm(user=request.user)
        return render(request, 'menu/alta-intervencion.html', {'form': form, 'nbar': 'intervencion'})

@staff_member_required
def agregarIntervencionTipo(request):
    if request.method == 'POST':
        form = agregarIntervencionTipoForm(request.POST)
        if form.is_valid():
            nuevo_tipo_intervencion = Tipo(
                descripcion=str(form.cleaned_data['descripcion']),
            )
            Intervencion.save(nuevo_tipo_intervencion)
            form = agregarIntervencionTipoForm()
            return render(request, 'menu/alta-tipo-intervencion.html', {'form': form, 'tipo_intervencion': nuevo_tipo_intervencion,
                                                                   'success': True, 'nbar': 'intervencion'})
        else:
            return render(request, 'menu/alta-tipo-intervencion.html', {'form': form,  'nbar': 'intervencion'})
    else:
        form = agregarIntervencionTipoForm()
        return render(request, 'menu/alta-tipo-intervencion.html', {'form': form, 'nbar': 'intervencion'})


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

@login_required
def listarIntervenciones(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'GET':
            try:
                intervenciones = Intervencion.objects.filter(tutor_asignado__dni=username)
            except:
                intervenciones = Intervencion.objects.all()
            return render(request, 'menu/intervenciones.html', {'intervenciones': intervenciones, 'nbar': 'intervencion'})


@login_required
def cerrarIntervencion(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:intervenciones')
        intervencion.estado = 'Cerrada'
        intervencion.fecha_baja = datetime.now()
        intervencion.save()
        return redirect('menu:intervenciones')

@login_required
def abrirIntervencion(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:intervenciones')
        intervencion.estado = 'Abierta'
        intervencion.fecha_baja = None
        intervencion.save()
        return redirect('menu:intervenciones')

