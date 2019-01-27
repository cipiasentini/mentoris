from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Alumno, Tutor, Intervencion, Tipo, Novedades, Tarea, Grupo
from sysacad.models import (Persona as SysacadPersona, Alumno as SysacadAlumno, Materia as SysacadMateria, Alumcom as MateriaAlumno, Especial as SysacadEspecial)
from .forms import (agregarAlumnoForm,  buscarAlumnoForm, editarAlumnoForm, agregarIntervencionForm, agregarIntervencionTipoForm)
from .forms import (agregarTutorForm, buscarTutorForm, agregarTutorPersonalizadoForm, agregarNovedadForm, editarIntervencionForm,
                    editarNovedadForm, agregarTareaForm, editarTutorForm, editarTareaForm, agregarGrupoForm, editarGrupoForm)
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# calendario
from django.shortcuts import render_to_response
from django.contrib import messages
from apps_externas.bcal import get_bcal

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

# @login_required
# def buscarAlumnoId(request, id):
#     form = buscarAlumnoForm()
#     if request.method == 'POST':
#         if (int(id) < 999999):
#             try:
#                 alumno = Alumno.objects.get(legajo=id)
#                 alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                 personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                 especialidadSysacad = SysacadEspecial.objects.get(alumnoSysacad.especialid)
#                 intervenciones = Intervencion.objects.filter(alumno=alumno)
#                 materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                 materias = SysacadMateria.objects.all()
#             except:
#                 return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#         else:
#             try:
#                 alumno = Alumno.objects.get(dni=id)
#                 personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                 alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                 especialidadSysacad = SysacadEspecial.objects.get(alumnoSysacad.especialid)
#                 intervenciones = Intervencion.objects.filter(alumno=alumno)
#                 materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                 materias = SysacadMateria.objects.all()
#             except:
#                 return render(request, 'menu/buscar-alumno.html',
#                               {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#         return render(request, 'menu/buscar-alumno.html', {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno,
#                                                            'intervenciones': intervenciones, 'nbar': 'alumnos',
#                                                            'materias': materias, 'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
#                                                            'sys_esp': especialidadSysacad})
#     else:
#         if request.method == 'POST':
#             form = buscarAlumnoForm(request.POST)
#             if form.is_valid():
#                 # form.id
#                 id = form.cleaned_data['id']
#                 if (int(id) < 999999):
#                     try:
#                         alumno = Alumno.objects.get(legajo=id)
#                         personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                         alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                         especialidadSysacad = SysacadEspecial.objects.get(alumnoSysacad.especialid)
#                         intervenciones = Intervencion.objects.filter(alumno=alumno)
#                         materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                         materias = SysacadMateria.objects.all()
#                     except:
#                         return render(request, 'menu/buscar-alumno.html',
#                                       {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#                 else:
#                     try:
#                         alumno = Alumno.objects.get(dni=id)
#                         personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                         alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                         especialidadSysacad = SysacadEspecial.objects.get(alumnoSysacad.especialid)
#                         intervenciones = Intervencion.objects.filter(alumno=alumno)
#                         materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                         materias = SysacadMateria.objects.all()
#                     except:
#                         return render(request, 'menu/buscar-alumno.html',
#                                       {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#                 return render(request, 'menu/buscar-alumno.html',
#                               {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno,
#                                'intervenciones': intervenciones, 'nbar': 'alumnos',
#                                'materias': materias, 'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
#                                 'sys_esp': especialidadSysacad})
#             else:
#                 return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'alumnos'})
#         else:
#             form = buscarAlumnoForm()
#             return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'alumnos'})

@login_required
def buscarAlumno(request):
    if request.method == 'POST':
        form = buscarAlumnoForm(request.POST)
        if form.is_valid():
            # form.id
            id = form.cleaned_data['id']
            if (int(id) < 999999):
                try:
                    alumno = Alumno.objects.get(legajo=id)
                    personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
                    alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
                    especialidadSysacad = SysacadEspecial.objects.get(especialid=alumnoSysacad.especialid)
                    intervenciones = Intervencion.objects.filter(alumno=alumno)
                    materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
                    materias = SysacadMateria.objects.all()
                except:
                    return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            else:
                try:
                    alumno = Alumno.objects.get(dni=id)
                    personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
                    alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
                    especialidadSysacad = SysacadEspecial.objects.get(especialid=alumnoSysacad.especialid)
                    intervenciones = Intervencion.objects.filter(alumno=alumno)
                    materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
                    materias = SysacadMateria.objects.all()
                except:
                    return render(request, 'menu/buscar-alumno.html',
                                  {'form': form, 'not_found': True, 'nbar': 'alumnos'})
            return render(request, 'menu/buscar-alumno.html', {'form': form, 'materiasAlumno': materiaAlumno ,'alumno_inst': alumno,
                                                               'intervenciones': intervenciones, 'nbar': 'alumnos',
                                                               'materias': materias, 'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
                                                                'sys_esp': especialidadSysacad})
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
                discapacidad=form.cleaned_data['discapacidad'],
                tipo_discapacidad=form.cleaned_data['tipo_discapacidad'],
                telefono=persona_sysacad.telefono,
                mail=persona_sysacad.mail,
                legajo=alumno_sysacad.legajo,
                situacion_riesgo='Ninguna',
                observaciones=observaciones,
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
                # return render(request, 'menu/alta-tutor-personalizada.html', {'not_found': True, 'nbar': 'tutores', 'dni': dni})
                return render(request, 'menu/alta-tutor.html',
                              {'alta_manual': True, 'not_found': True, 'nbar': 'tutores', 'dni': dni})
                # return redirect('menu:alta-tutor-personalizada', {'not_found': True, 'nbar': 'tutores', 'dni': dni})
                # return render(request, 'menu/alta-tutor-personalizada.html',
                #               {'form': agregarTutorPersonalizadoForm(request.POST),
                #                'alta_manual': True, 'nbar': 'tutores'})
            nuevo_tutor = Tutor(
                nombre=persona_sysacad.nombre.rstrip(),
                dni=persona_sysacad.numerodocu,
                legajo=alumno_sysacad.legajo,
                telefono=persona_sysacad.telefono.rstrip(),
                mail=persona_sysacad.mail.rstrip(),
                tipo=form.cleaned_data['tipo'],
                horario=form.cleaned_data['horario'],
                materia=form.cleaned_data['materia'],
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
                materia=form.cleaned_data['materia'],
                mail=form.cleaned_data['mail'],
                tipo=form.cleaned_data['tipo'],
                horario=form.cleaned_data['horario'],
                usuario=form.cleaned_data['dni'],
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

@staff_member_required
def editarTutor(request, legajo):
    try:
        tutor = Tutor.objects.get(legajo=legajo)
    except:
        return render(request, 'menu/editar-tutor.html', {'not_found': True, 'nbar': 'tutor'})
    form = editarTutorForm(instance=tutor)
    if request.method == 'POST':
        form = editarTutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-tutor.html', {'form': form, 'success': True, 'tutor_inst': tutor, 'nbar': 'tutor'})
        else:
            form = editarTutorForm(instance=tutor)
    return render(request, 'menu/editar-tutor.html', {'form': form, 'nbar': 'tutor'})

@staff_member_required
def bajaTutor(request, legajo):
    try:
        tutor = Tutor.objects.get(legajo=legajo)
    except:
        return render(request, 'menu/buscar-tutor.html', {'not_found': True, 'nbar': 'tutor'})
    tutor.fecha_desvinculacion = datetime.today()
    tutor.save()
    u = User.objects.get(username=tutor.dni)
    u.set_password('passwordOf@tutorWhichIsNoLongerAvailable')
    u.save()
    # return redirect('menu:buscar-tutor')
    # form = buscarTutorForm()
    return render(request, 'menu/buscar-tutor.html', {'baja': True, 'tutor_inst': tutor, 'nbar': 'tutor'})

@staff_member_required
def altaTutor(request, legajo):
    try:
        tutor = Tutor.objects.get(legajo=legajo)
    except:
        return render(request, 'menu/buscar-tutor.html', {'not_found': True, 'nbar': 'tutor'})
    tutor.fecha_alta = datetime.today()
    tutor.fecha_desvinculacion = None
    tutor.save()
    u = User.objects.get(username=tutor.dni)
    contrasena = 'dni' + str(tutor.dni)[0:5]
    u.set_password(contrasena)
    u.save()
    # return redirect('menu:buscar-tutor')
    # form = buscarTutorForm()
    return render(request, 'menu/buscar-tutor.html', {'alta': True, 'tutor_inst': tutor, 'nbar': 'tutor'})

@staff_member_required
def buscarTutor(request):
    if request.method == 'POST':
        form = buscarTutorForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            if (int(id) < 999999):
                try:
                    tutor = Tutor.objects.get(legajo=id)
                except:
                    return render(request, 'menu/buscar-tutor.html',
                                  {'form': form, 'not_found': True, 'nbar': 'tutores'})
            else:
                try:
                    tutor = Tutor.objects.get(dni=id)
                except:
                    return render(request, 'menu/buscar-tutor.html', {'form': form, 'not_found': True, 'nbar': 'tutores'})
            return render(request, 'menu/buscar-tutor.html', {'form': form, 'tutor': tutor, 'nbar': 'tutores'})
        form = buscarTutorForm()
        return render(request, 'menu/buscar-tutor.html', {'form': form, 'bad': True, 'nbar': 'tutores'})
    else:
        form = buscarTutorForm()
        return render(request, 'menu/buscar-tutor.html', {'form': form, 'nbar': 'tutores'})

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
                form = agregarIntervencionForm(user=request.user)
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
def editarIntervencion(request, id):
    try:
        intervencion = Intervencion.objects.get(id=id)
    except:
        return render(request, 'menu/editar-intervencion.html', {'not_found': True, 'nbar': 'intervencion'})
    form = editarIntervencionForm(user=request.user, instance=intervencion)
    if request.method == 'POST':
        form = editarIntervencionForm(request.POST, user=request.user, instance=intervencion)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-intervencion.html', {'form': form, 'success': True, 'nbar': 'intervencion'})
        else:
            form = editarIntervencionForm(user=request.user, instance=intervencion)
    return render(request, 'menu/editar-intervencion.html', {'form': form, 'nbar': 'intervencion'})

# Estos son para los del template intervenciones.html
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

# Estos son iguales pero para los del template buscar-alumno-atomico.html
@login_required
def cerrarIntervencionB(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:buscar-alumno')
        intervencion.estado = 'Cerrada'
        intervencion.fecha_baja = datetime.now()
        intervencion.save()
        return redirect('menu:buscar-alumno-id', id=intervencion.alumno.legajo)

@login_required
def abrirIntervencionB(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:buscar-alumno')
        intervencion.estado = 'Abierta'
        intervencion.fecha_baja = None
        intervencion.save()
        return redirect('menu:buscar-alumno-id', id=intervencion.alumno.legajo)

@staff_member_required
def eliminarIntervencion(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:intervenciones')
        intervencion.delete()
        return redirect('menu:intervenciones')

# NOVEDADES

@login_required
def verNovedades(request):
    if request.method == 'GET':
        novedades = Novedades.objects.filter(estado='Activa')
        return render(request, 'menu/index.html', {'novedades': novedades, 'nbar': 'index'})

@staff_member_required
def panelNovedades(request):
    if request.method == 'GET':
        novedades = Novedades.objects.all()
        return render(request, 'menu/panel-novedades.html', {'novedades': novedades, 'nbar': 'administrador'})

@staff_member_required
def cerrarNovedad(request, id):
    if request.method == 'GET':
        try:
            novedad = Novedades.objects.get(id=id)
        except:
            return redirect('menu:panel-novedades')
        novedad.estado = 'Cerrada'
        novedad.save()
        return redirect('menu:panel-novedades')

@staff_member_required
def abrirNovedad(request, id):
    if request.method == 'GET':
        try:
            novedad = Novedades.objects.get(id=id)
        except:
            return redirect('menu:panel-novedades')
        novedad.estado = 'Activa'
        novedad.save()
        return redirect('menu:panel-novedades')

@staff_member_required
def eliminarNovedad(request, id):
    if request.method == 'GET':
        try:
            novedad = Novedades.objects.get(id=id)
        except:
            return redirect('menu:panel-novedades')
        novedad.delete()
        return redirect('menu:panel-novedades')

@staff_member_required
def agregarNovedad(request):
    if request.method == 'POST':
        form = agregarNovedadForm(request.POST)
        if form.is_valid():
            nueva_novedad = Novedades(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
            )
            Novedades.save(nueva_novedad)
            form = agregarNovedadForm()
            return render(request, 'menu/alta-novedad.html', {'form': form, 'novedad': nueva_novedad, 'success': True, 'nbar': 'administrador'})
    else:
        form = agregarNovedadForm()
        return render(request, 'menu/alta-novedad.html', {'form': form, 'nbar': 'administrador'})

@staff_member_required
def editarNovedad(request, id):
    try:
        novedad = Novedades.objects.get(id=id)
    except:
        return render(request, 'menu/editar-novedad.html', {'not_found': True, 'nbar': 'administrador'})
    form = editarNovedadForm(instance=novedad)
    if request.method == 'POST':
        novedad.fecha_alta = datetime.now()
        form = editarNovedadForm(request.POST, instance=novedad)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-novedad.html', {'form': form, 'success': True, 'novedad': novedad, 'nbar': 'administrador'})
        else:
            form = editarNovedadForm(instance=novedad)
    return render(request, 'menu/editar-novedad.html', {'form': form, 'nbar': 'administrador'})


# Para poder setear sesion y mantener el estado anterior del collapse
def update_session(request, collapse):
    # if not request.is_ajax() or not request.method == 'POST':
    #     return HttpResponseNotAllowed(['POST'])
    request.session['collapse'] = collapse
    return HttpResponse('ok')

@login_required
def estadisticas(request):
    alumnos = Alumno.objects.all()
    anios = Alumno.objects.datetimes('fecha_alta', 'year')
    alumnos_anios = {}
    for a in anios:
        alumnos_anios.update({str(a.year): Alumno.objects.filter(fecha_alta__year=a.year).count()})
    pop = dict(alumnos_anios)
    ult_anio = pop.popitem()[0]
    total = alumnos.filter(fecha_alta__year=ult_anio).count()
    riesgo = alumnos.filter(situacion_riesgo='Si').filter(fecha_alta__year=ult_anio).count()
    no_riesgo = total - riesgo
    return render(request, 'menu/estadisticas.html', {'alumnos_anios': alumnos_anios, 'ult_anio': ult_anio, 'alumnos_riesgo': riesgo, 'alumnos_no_riesgo': no_riesgo})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'menu/change_password.html', {
                'form': form, 'success': True, 'user': request.user
            })
        else:
            return render(request, 'menu/change_password.html', {
                'form': form, 'not_found': True
            })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'menu/change_password.html', {
        'form': form
    })

@login_required
def agregarTarea(request):
    if request.method == 'POST':
        form = agregarTareaForm(request.POST, user=request.user)
        if form.is_valid():
            if request.user.is_staff:
                nueva_tarea = Tarea(
                    titulo=form.cleaned_data['titulo'],
                    descripcion=form.cleaned_data['descripcion'],
                    fecha_alta=form.cleaned_data['fecha_alta'],
                    tutor_asignado=form.cleaned_data['tutor_asignado'],
                )
            else:
                nueva_tarea = Tarea(
                    titulo=form.cleaned_data['titulo'],
                    descripcion=form.cleaned_data['descripcion'],
                    fecha_alta=form.cleaned_data['fecha_alta'],
                    tutor_asignado=Tutor.objects.get(usuario=request.user.username),
                )
            Tarea.save(nueva_tarea)
            form = agregarTareaForm(user=request.user)
            return render(request, 'menu/alta-tarea.html', {'form': form, 'tarea': nueva_tarea, 'tutor': request.user.username, 'success': True, 'nbar': 'tareas'})
    else:
        form = agregarTareaForm(user=request.user)
        return render(request, 'menu/alta-tarea.html', {'form': form, 'nbar': 'tareas'})


@login_required
def bcal(request, year, month, day):
    today = datetime.today()
    today_events = Tarea.objects.filter(fecha_alta__year=year).filter(fecha_alta__month=month).filter(fecha_alta__day=day)
    if int(month) > 12:
        y = str(today.year)
        m = str(today.month)
        messages.add_message(request, messages.WARNING, 'Error de mes')
    else:
        y = year
        m = month

    return render(
        request,
        'menu/agenda-tareas.html',
        {
            'calendar': get_bcal(y, m, day, user=request.user),
            'today': today_events,
        },
        content_type='html')


@login_required
def mostrarTareaId(request, id):
    if request.method == 'GET':
        try:
            tarea = Tarea.objects.get(id=id)
        except:
            return render(request, 'menu/index.html')
        return render(request, 'menu/tarea.html', {'nbar': 'tareas', 'tarea': tarea})

@login_required
def editarTarea(request, id):
    try:
        tarea = Tarea.objects.get(id=id)
    except:
        return render(request, 'menu/editar-tarea.html', {'not_found': True, 'nbar': 'tareas'})
    form = editarTareaForm(instance=tarea)
    if request.method == 'POST':
        form = editarTareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return render(request, 'menu/tarea.html', {'form': form, 'success': True, 'tarea': tarea, 'nbar': 'tareas'})
        else:
            form = editarTareaForm(instance=tarea)
    return render(request, 'menu/editar-tarea.html', {'form': form, 'tarea': tarea, 'nbar': 'tareas'})

@staff_member_required
def agregarGrupo(request):
    if request.method == 'POST':
        form = agregarGrupoForm(request.POST)
        if form.is_valid():
            tutores = form.cleaned_data['tutores']
            alumnos = form.cleaned_data['alumnos']

            grupo = Grupo.objects.create(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                horario=form.cleaned_data['horario'],
                fecha_alta=form.cleaned_data['fecha_alta'],
            )

            for tut in tutores:
                grupo.tutores.add(tut)
            for alu in alumnos:
                try:
                    alumno_existente = Alumno.objects.get(dni=alu.numerodocu)
                    grupo.alumnos.add(alumno_existente)
                except:
                    try:
                        persona_sysacad = SysacadPersona.objects.get(numerodocu=alu.numerodocu)
                    except:
                        return render(request, 'menu/alta-grupo.html', {'form': form, 'nbar': 'grupos'})
                    nuevo_alumno = Alumno(
                        nombre=persona_sysacad.nombre,
                        dni=alu.numerodocu,
                        telefono=persona_sysacad.telefono,
                        mail=persona_sysacad.mail,
                        legajo=alu.legajo,
                        situacion_riesgo='Ninguna'
                    )
                    Alumno.save(nuevo_alumno)
                    grupo.alumnos.add(nuevo_alumno)

            Grupo.save(grupo)
            return render(request, 'menu/alta-grupo.html', {'form': form, 'grupo': grupo, 'success': True, 'nbar': 'grupos'})
    else:
        form = agregarGrupoForm()
        return render(request, 'menu/alta-grupo.html', {'form': form, 'nbar': 'grupos'})

@login_required
def listarGrupos(request):
    if request.method == 'GET':
        if request.user.is_staff:
            try:
                grupos = Grupo.objects.all()
            except:
                return render(request, 'menu/listar-grupos-activos.html', {'nbar': 'grupos', 'not_found': True})
        else:
            try:
                grupos = Grupo.objects.filter(tutores__dni=request.user.username)
            except:
                return render(request, 'menu/listar-grupos-activos.html', {'nbar': 'grupos', 'not_found': True})
        return render(request, 'menu/listar-grupos-activos.html', {'nbar': 'grupos', 'grupos': grupos})

@login_required
def editarGrupo(request, id):
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        return render(request, 'menu/editar-grupo.html', {'not_found': True, 'nbar': 'grupos'})
    form = editarGrupoForm(instance=grupo)
    if request.method == 'POST':
        form = editarGrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-grupo.html', {'form': form, 'success': True, 'grupo': grupo, 'nbar': 'grupos'})
        else:
            form = editarGrupoForm(instance=grupo)
    return render(request, 'menu/editar-grupo.html', {'form': form, 'grupo': grupo, 'nbar': 'grupos'})

@staff_member_required
def eliminarGrupo(request, id):
    if request.method == 'GET':
        try:
            grupo = Grupo.objects.get(id=id)
        except:
            return redirect('menu:listar-grupos')
        grupo.delete()
        return redirect('menu:listar-grupos')