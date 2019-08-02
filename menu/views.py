from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Alumno, Tutor, Intervencion, Tipo, Novedades, Tarea, Grupo, Materia
from sysacad.models import (Persona as SysacadPersona, Alumno as SysacadAlumno, Materia as SysacadMateria,
                            Alumcom as MateriaAlumno, Especial as SysacadEspecial, Escuela as SysacadEscuela)
from .forms import (agregarAlumnoForm,  buscarAlumnoForm, editarAlumnoForm, agregarIntervencionForm, agregarIntervencionTipoForm)
from .forms import (agregarTutorForm, buscarTutorForm, agregarTutorPersonalizadoForm, agregarNovedadForm, editarIntervencionForm,
                    editarNovedadForm, agregarTareaForm, editarTutorForm, editarTareaForm, agregarGrupoForm, editarGrupoForm,
                    rankingConsultasTemaForm, agregarEditarMateriaForm)
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from collections import Counter
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
            if not alumno.recursante:
                alumno.motivo_recursante = None
            if not alumno.discapacidad:
                alumno.tipo_discapacidad = None
            if not alumno.dejo_seminario:
                alumno.motivo_dejo_seminario = None
            form.save()
            return render(request, 'menu/editar-alumno.html', {'form': form, 'success': True, 'alumno_inst': alumno, 'nbar': 'alumno'})
        else:
            form = editarAlumnoForm(instance=alumno)
    return render(request, 'menu/editar-alumno.html', {'form': form, 'nbar': 'alumno'})

@login_required
def buscarAlumno(request):
    if request.method == 'POST':
        form = buscarAlumnoForm(request.POST)
        alu = int(form.data.get('id'))
        alumno = Alumno.objects.get(dni=alu)
        try:
            personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
            alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
            especialidadSysacad = SysacadEspecial.objects.get(especialid=alumnoSysacad.especialid)
            intervenciones = Intervencion.objects.filter(alumno=alumno)
            materiaAlumno = MateriaAlumno.objects.filter(legajo=alumno.legajo)
            escuelaSysacad = SysacadEscuela.objects.filter(escuela=personaSysacad.escuela)
        except:
            return render(request, 'menu/buscar-alumno.html',
                          {'form': form, 'not_found': True, 'nbar': 'alumnos'})
        seminario = []
        materias = SysacadMateria.objects.all()
        for ma in materiaAlumno:
            if ma.especialid == 900:
                try:
                    materia = SysacadMateria.objects.get(materia=ma.materia)
                except:
                    return render(request, 'menu/buscar-alumno.html',
                                  {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno,
                                   'intervenciones': intervenciones, 'nbar': 'alumnos', 'origen': alumno.ciudad_origen,
                                   'sys_al': alumnoSysacad, 'sys_per': personaSysacad, 'escuela': escuelaSysacad,
                                   'sys_esp': especialidadSysacad, 'error_materia': True, 'materia': ma, 'materias': materias,
                                    'residencia': alumno.ciudad_residencia})
                seminario.append(tuple((ma, materia)))
        if len(seminario) > 0:
            return render(request, 'menu/buscar-alumno.html', {'form': form, 'materiasAlumno': materiaAlumno ,'alumno_inst': alumno,
                                                               'intervenciones': intervenciones, 'nbar': 'alumnos', 'origen': alumno.ciudad_origen,
                                                               'sys_al': alumnoSysacad, 'sys_per': personaSysacad, 'escuela': escuelaSysacad,
                                                               'sys_esp': especialidadSysacad, 'seminario': seminario, 'cant_seminario': len(seminario),
                                                               'residencia': alumno.ciudad_residencia, 'materias': materias})
        else:
            return render(request, 'menu/buscar-alumno.html',
                          {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno, 'origen': alumno.ciudad_origen,
                           'intervenciones': intervenciones, 'nbar': 'alumnos', 'escuela': escuelaSysacad,
                           'sys_al': alumnoSysacad, 'sys_per': personaSysacad, 'residencia': alumno.ciudad_residencia,
                           'sys_esp': especialidadSysacad, 'materias': materias})
    else:
        form = buscarAlumnoForm()
        return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'alumnos'})

# ESTE BUSCAR ALUMNO ES CON EL CAMPO DE BUSQUEDA COMUN, BUSCAR POR LEGAJO O DNI
# PARA QUE FUNCIONE NECESITAS CAMBIAR EN BUSCAR-ALUMNO-ATOMICO.HTML EL FORM TEMPLATE form_template.html
# Y EL FORM DE BUSCAR ALUMNO POR EL ID COMUN.
# LO MISMO VA A PASAR PARA EL TUTOR, PORQUE CREO QUE ASI ES MEJOR BUSCARLO MAS FACIL.

# @login_required
# def buscarAlumno(request):
#     if request.method == 'POST':
#         form = buscarAlumnoForm(request.POST)
#         if form.is_valid():
#             id = form.cleaned_data['id']
#             # legajo
#             if (int(id) < 999999):
#                 try:
#                     alumno = Alumno.objects.get(legajo=id)
#                     personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                     alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                     especialidadSysacad = SysacadEspecial.objects.get(especialid=alumnoSysacad.especialid)
#                     intervenciones = Intervencion.objects.filter(alumno=alumno)
#                     materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                     materias = SysacadMateria.objects.all()
#                 except:
#                     return render(request, 'menu/buscar-alumno.html', {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#             # dni
#             else:
#                 try:
#                     alumno = Alumno.objects.get(dni=id)
#                     personaSysacad = SysacadPersona.objects.get(numerodocu=alumno.dni)
#                     alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alumno.dni)
#                     especialidadSysacad = SysacadEspecial.objects.get(especialid=alumnoSysacad.especialid)
#                     intervenciones = Intervencion.objects.filter(alumno=alumno)
#                     materiaAlumno = MateriaAlumno.objects.filter(legajo=id)
#                     materias = SysacadMateria.objects.all()
#                 except:
#                     return render(request, 'menu/buscar-alumno.html',
#                                   {'form': form, 'not_found': True, 'nbar': 'alumnos'})
#             seminario = []
#             for ma in materiaAlumno:
#                 if ma.especialid == 900:
#                     try:
#                         materia = SysacadMateria.objects.get(materia=ma.materia)
#                     except:
#                         return render(request, 'menu/buscar-alumno.html',
#                                       {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno,
#                                        'intervenciones': intervenciones, 'nbar': 'alumnos',
#                                        'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
#                                        'sys_esp': especialidadSysacad, 'error_materia': True, 'materia': ma})
#                     seminario.append(tuple((ma, materia)))
#             if len(seminario) > 0:
#                 return render(request, 'menu/buscar-alumno.html', {'form': form, 'materiasAlumno': materiaAlumno ,'alumno_inst': alumno,
#                                                                'intervenciones': intervenciones, 'nbar': 'alumnos',
#                                                                'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
#                                                                'sys_esp': especialidadSysacad, 'seminario': seminario, 'cant_seminario': len(seminario)})
#             else:
#                 return render(request, 'menu/buscar-alumno.html',
#                               {'form': form, 'materiasAlumno': materiaAlumno, 'alumno_inst': alumno,
#                                'intervenciones': intervenciones, 'nbar': 'alumnos',
#                                'sys_al': alumnoSysacad, 'sys_per': personaSysacad,
#                                'sys_esp': especialidadSysacad})
#         else:
#             return render(request, 'menu/buscar-alumno.html', {'form': form,  'nbar': 'alumnos'})
#     else:
#         form = buscarAlumnoForm()
#         return render(request, 'menu/buscar-alumno.html', {'form': form, 'nbar': 'alumnos'})

@login_required
def agregarAlumno(request):
    if request.method == 'POST':
        form = agregarAlumnoForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            observaciones = form.cleaned_data['observaciones']
            try:
                persona_sysacad = SysacadPersona.objects.get(numerodocu=dni)
                alumno_sysacad = SysacadAlumno.objects.get(numerodocu=dni)
            except:
                return render(request, 'menu/alta-alumno.html', {'form': form, 'dni': dni, 'not_found': True, 'nbar': 'alumnos'})
            nuevo_alumno = Alumno(
                nombre=persona_sysacad.nombre,
                dni=dni,
                discapacidad=form.cleaned_data['discapacidad'],
                tipo_discapacidad=form.cleaned_data['tipo_discapacidad'],
                telefono=int(persona_sysacad.telefono),
                mail=persona_sysacad.mail,
                legajo=alumno_sysacad.legajo,
                situacion_riesgo='No',
                observaciones=observaciones,
                recursante=form.cleaned_data['recursante'],
                motivo_recursante=form.cleaned_data['motivo_recursante'],
                dejo_seminario=form.cleaned_data['dejo_seminario'],
                motivo_dejo_seminario=form.cleaned_data['motivo_dejo_seminario'],
                ciudad_origen=form.cleaned_data['ciudad_origen'],
                ciudad_residencia=form.cleaned_data['ciudad_residencia'],
                tipo_escuela=form.cleaned_data['tipo_escuela']
            )
            Alumno.save(nuevo_alumno)
            form = agregarAlumnoForm()
            return render(request, 'menu/alta-alumno.html', {'form': form, 'alumno': nuevo_alumno, 'success': True, 'nbar': 'alumnos'})
        else:
            return render(request, 'menu/alta-alumno.html',
                              {'form': form, 'error_form': True, 'nbar': 'alumnos'})
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
                              {'alta_manual': True, 'not_found': True, 'nbar': 'tutores', 'dni': dni})
            nuevo_tutor = Tutor(
                nombre=persona_sysacad.nombre.rstrip(),
                dni=persona_sysacad.numerodocu,
                legajo=alumno_sysacad.legajo,
                telefono=int(persona_sysacad.telefono),
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
            return render(request, 'menu/alta-tutor.html', {'form': form, 'error_form': True, 'nbar': 'tutores'})
    else:
        form = agregarTutorForm()
        return render(request, 'menu/alta-tutor.html', {'form': form, 'nbar': 'tutores'})

@staff_member_required
def agregarTutorPersonalizado(request):
    if request.method == 'POST':
        form = agregarTutorPersonalizadoForm(request.POST)
        if form.is_valid():
            if len(str(form.cleaned_data['dni'])) != 8:
                return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'bad_dni': True, 'nbar': 'tutores'})
            nuevo_tutor = Tutor(
                nombre=form.cleaned_data['nombre'],
                dni=form.cleaned_data['dni'],
                telefono=int(form.cleaned_data['telefono']),
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
            return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'error_form': True, 'nbar': 'tutores'})
    else:
        form = agregarTutorPersonalizadoForm()
        return render(request, 'menu/alta-tutor-personalizada.html', {'form': form, 'nbar': 'tutores'})

@staff_member_required
def editarTutor(request, dni):
    try:
        tutor = Tutor.objects.get(dni=dni)
    except:
        return render(request, 'menu/editar-tutor.html', {'not_found': True, 'nbar': 'tutor'})
    form = editarTutorForm(instance=tutor)
    if request.method == 'POST':
        form = editarTutorForm(request.POST, instance=tutor)
        if form.is_valid():
            if tutor.tipo != "Academico":
                tutor.materia = None
            if len(str(form.cleaned_data['dni'])) != 8:
                return render(request, 'menu/editar-tutor.html', {'form': form, 'bad_dni': True, 'nbar': 'tutores'})
            form.save()
            return render(request, 'menu/editar-tutor.html', {'form': form, 'success': True, 'tutor_inst': tutor, 'nbar': 'tutor'})
        else:
            form = editarTutorForm(instance=tutor)
    return render(request, 'menu/editar-tutor.html', {'form': form, 'nbar': 'tutor'})

@staff_member_required
def bajaTutor(request, dni):
    try:
        tutor = Tutor.objects.get(dni=dni)
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
def altaTutor(request, dni):
    try:
        tutor = Tutor.objects.get(dni=dni)
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
        tut = int(form.data.get('id'))
        tutor = Tutor.objects.get(dni=tut)
        try:
            grupos = Grupo.objects.filter(tutores__dni=tutor.dni)
        except:
            return render(request, 'menu/buscar-tutor.html', {'form': form, 'not_found': True, 'nbar': 'tutores'})
        return render(request, 'menu/buscar-tutor.html', {'form': form, 'tutor': tutor, 'grupos': grupos, 'nbar': 'tutores'})
    else:
        form = buscarTutorForm()
        return render(request, 'menu/buscar-tutor.html', {'form': form, 'nbar': 'tutores'})


# ESTE BUSCAR ALUMNO ES CON EL CAMPO DE BUSQUEDA COMUN, BUSCAR POR LEGAJO O DNI
# PARA QUE FUNCIONE NECESITAS CAMBIAR EN BUSCAR-ALUMNO-ATOMICO.HTML EL FORM TEMPLATE form_template.html
# Y EL FORM DE BUSCAR ALUMNO POR EL ID COMUN.
# LO MISMO VA A PASAR PARA EL TUTOR, PORQUE CREO QUE ASI ES MEJOR BUSCARLO MAS FACIL.

# @staff_member_required
# def buscarTutor(request):
#     if request.method == 'POST':
#         form = buscarTutorForm(request.POST)
#         if form.is_valid():
#             id = form.cleaned_data['id']
#             if (int(id) < 999999):
#                 try:
#                     tutor = Tutor.objects.get(legajo=id)
#                     grupos = Grupo.objects.filter(tutores__dni=tutor.dni)
#                 except:
#                     return render(request, 'menu/buscar-tutor.html',
#                                   {'form': form, 'not_found': True, 'nbar': 'tutores'})
#             else:
#                 try:
#                     tutor = Tutor.objects.get(dni=id)
#                     grupos = Grupo.objects.filter(tutores__dni=tutor.dni)
#                 except:
#                     return render(request, 'menu/buscar-tutor.html', {'form': form, 'not_found': True, 'nbar': 'tutores'})
#             return render(request, 'menu/buscar-tutor.html', {'form': form, 'tutor': tutor, 'grupos': grupos, 'nbar': 'tutores'})
#         else:
#             return render(request, 'menu/buscar-tutor.html', {'form': form, 'bad': True, 'nbar': 'tutores'})
#     else:
#         form = buscarTutorForm()
#         return render(request, 'menu/buscar-tutor.html', {'form': form, 'nbar': 'tutores'})

@login_required
def agregarIntervencion(request):
    if request.method == 'POST':
        form = agregarIntervencionForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                m = request.POST.get('materia')
                mat = SysacadMateria.objects.get(materia=m)
            except:
                if request.user.is_staff:
                    nueva_intervencion = Intervencion(
                        tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                        descripcion=str(form.cleaned_data['descripcion']),
                        medio=form.cleaned_data['medio'],
                        tutor_asignado=Tutor.objects.get(dni=form.cleaned_data['tutor_asignado'].dni),
                        alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni),
                        fecha_alta=form.cleaned_data['fecha_alta']
                    )
                else:
                    nueva_intervencion = Intervencion(
                        tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                        descripcion=str(form.cleaned_data['descripcion']),
                        medio=form.cleaned_data['medio'],
                        tutor_asignado=Tutor.objects.get(dni=request.user.username),
                        alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni),
                        fecha_alta=form.cleaned_data['fecha_alta']
                    )
                Intervencion.save(nueva_intervencion)
                form = agregarIntervencionForm(user=request.user)
                return render(request, 'menu/alta-intervencion.html', {'form': form, 'intervencion': nueva_intervencion,
                              'success': True, 'nbar': 'intervencion'})
            if request.user.is_staff:
                nueva_intervencion = Intervencion(
                    tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                    descripcion=str(form.cleaned_data['descripcion']),
                    materia=mat.materia,
                    medio=form.cleaned_data['medio'],
                    tutor_asignado=Tutor.objects.get(dni=form.cleaned_data['tutor_asignado'].dni),
                    alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni),
                    fecha_alta=form.cleaned_data['fecha_alta']
                )
            else:
                nueva_intervencion = Intervencion(
                    tipo=Tipo.objects.get(id=form.cleaned_data['tipo'].id),
                    descripcion=str(form.cleaned_data['descripcion']),
                    materia=mat.materia,
                    medio=form.cleaned_data['medio'],
                    tutor_asignado=Tutor.objects.get(dni=request.user.username),
                    alumno=Alumno.objects.get(dni=form.cleaned_data['alumno'].dni),
                    fecha_alta=form.cleaned_data['fecha_alta']
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
    tipos = Tipo.objects.all()
    if request.method == 'POST':
        form = agregarIntervencionTipoForm(request.POST)
        if form.is_valid():
            nuevo_tipo_intervencion = Tipo(
                descripcion=str(form.cleaned_data['descripcion']),
            )
            Tipo.save(nuevo_tipo_intervencion)
            form = agregarIntervencionTipoForm()
            return render(request, 'menu/alta-tipo-intervencion.html', {'form': form, 'tipo_intervencion': nuevo_tipo_intervencion,
                                                                        'success': True, 'nbar': 'intervencion', 'tipos': tipos})
        else:
            return render(request, 'menu/alta-tipo-intervencion.html', {'form': form,  'nbar': 'intervencion', 'tipos': tipos})
    else:
        form = agregarIntervencionTipoForm()
        return render(request, 'menu/alta-tipo-intervencion.html', {'tipos': tipos, 'form': form, 'nbar': 'intervencion'})


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
            materias = SysacadMateria.objects.all()
            return render(request, 'menu/intervenciones.html', {'intervenciones': intervenciones,'materias': materias, 'nbar': 'intervencion'})
        else:
            return render(request, 'menu/index.html', {'nbar': 'index'})

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

@staff_member_required
def eliminarIntervencion(request, id):
    if request.method == 'GET':
        try:
            intervencion = Intervencion.objects.get(id=id)
        except:
            return redirect('menu:intervenciones')
        intervencion.delete()
        return redirect('menu:intervenciones')

@staff_member_required
def eliminarTipoIntervencion(request, id):
    if request.method == 'GET':
        try:
            tipo = Tipo.objects.get(id=id)
            intervenciones = Intervencion.objects.filter(tipo=tipo)
        except:
            return redirect('menu:alta-tipo-intervencion')
        if intervenciones:
            tipos = Tipo.objects.all()
            form = agregarIntervencionTipoForm()
            return render(request, 'menu/alta-tipo-intervencion.html', {'tipos': tipos, 'form': form, 'no_borrar': True,
                                                                        'nbar': 'intervencion', 'tipo': tipo})
        tipo.delete()
        return redirect('menu:alta-tipo-intervencion')

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
        return redirect('menu:buscar-alumno')

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
        return redirect('menu:buscar-alumno')

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
            # form = agregarTareaForm(user=request.user)
            if request.user.is_staff:
                return render(request, 'menu/alta-tarea.html',
                              {'form': form, 'tarea': nueva_tarea, 'tutor': nueva_tarea.tutor_asignado.nombre, 'success': True,
                               'nbar': 'tareas'})
            else:
                return render(request, 'menu/alta-tarea.html',
                              {'form': form, 'tarea': nueva_tarea, 'tutor': request.user.username, 'success': True,
                               'nbar': 'tareas'})
        return render(request, 'menu/alta-tarea.html',
                      {'form': form, 'tutor': request.user.username, 'error': True,
                       'nbar': 'tareas'})
    else:
        form = agregarTareaForm(user=request.user)
        return render(request, 'menu/alta-tarea.html', {'form': form, 'nbar': 'tareas'})

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
def eliminarTarea(request, id):
    if request.method == 'GET':
        try:
            tarea = Tarea.objects.get(id=id)
        except:
            return bcal(request, datetime.today().year, datetime.today().month, datetime.today().day)
        tarea.delete()
        return bcal(request, datetime.today().year, datetime.today().month, datetime.today().day)
    else:
        return bcal(request, datetime.today().year, datetime.today().month, datetime.today().day)

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
            'calendar': get_bcal(y, m, day),
            'today': today_events,
        },
        content_type='html')

@login_required
def agregarGrupo(request):
    if request.method == 'POST':
        form = agregarGrupoForm(request.POST, user=request.user)
        if form.is_valid():
            if request.user.is_staff:
                tutores = form.cleaned_data['tutores']
            alumnos = form.cleaned_data['alumnos']
            grupo = Grupo.objects.create(
                titulo=form.cleaned_data['titulo'],
                descripcion=form.cleaned_data['descripcion'],
                horario=form.cleaned_data['horario'],
                fecha_alta=datetime.today()
            )
            if request.user.is_staff:
                for tut in tutores:
                    grupo.tutores.add(tut)
            else:
                grupo.tutores.add(Tutor.objects.get(dni=int(request.user.username)))
            # for alu in alumnos:
            #     try:
            #         alumno_existente = Alumno.objects.get(dni=int(alu.numerodocu))
            #         grupo.alumnos.add(alumno_existente)
            #     except:
            #         try:
            #             persona_sysacad = SysacadPersona.objects.get(numerodocu=alu.numerodocu)
            #         except:
            #             return render(request, 'menu/alta-grupo.html', {'form': form, 'error_alumno': True, 'nbar': 'grupos'})
            #         nuevo_alumno = Alumno(
            #             nombre=persona_sysacad.nombre.rstrip(),
            #             dni=int(alu.numerodocu),
            #             telefono=int(persona_sysacad.telefono),
            #             mail=persona_sysacad.mail.rstrip(),
            #             legajo=alu.legajo,
            #             situacion_riesgo='No'
            #         )
            #         Alumno.save(nuevo_alumno)
            #         grupo.alumnos.add(nuevo_alumno)
            grupo.alumnos = alumnos
            Grupo.save(grupo)
            grupos = Grupo.objects.all()
            return render(request, 'menu/listar-grupos-activos.html', {'grupos': grupos, 'grupo': grupo, 'agregado': True, 'nbar': 'grupos'})
        else:
            return render(request, 'menu/alta-grupo.html',
                          {'form': form, 'success': False, 'nbar': 'grupos'})
    else:
        form = agregarGrupoForm(user=request.user)
        return render(request, 'menu/alta-grupo.html', {'form': form, 'nbar': 'grupos'})

@login_required
def listarGrupos(request):
    if request.method == 'GET':
        if request.user.is_staff:
            try:
                grupos = Grupo.objects.all().extra(order_by=['estado'])
            except:
                return render(request, 'menu/listar-grupos-activos.html', {'nbar': 'grupos', 'not_found': True})
        else:
            try:
                grupos = Grupo.objects.filter(tutores__dni=request.user.username).extra(order_by=['estado'])
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
            return redirect('menu:listar-grupos')
        else:
            form = editarGrupoForm(instance=grupo)
            return render(request, 'menu/editar-grupo.html', {'form': form, 'nbar': 'grupos', 'not_found': True})
    else:
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
    else:
        return redirect('menu:listar-grupos')


@staff_member_required
def rankingConsultas(request):
    if request.method == 'POST':
        form = rankingConsultasTemaForm(request.POST)
        if form.is_valid():
            try:
                desde = form.cleaned_data['desde']
                hasta = form.cleaned_data['hasta']
            except:
                return render(request, 'menu/informe-ranking-consultas.html', {'form': form, 'error': True, 'nbar': 'informes'})
            try:
                int = Intervencion.objects.filter(fecha_alta__range=(desde, hasta))
            except:
                return render(request, 'menu/informe-ranking-consultas.html', {'form': form, 'error': True, 'nbar': 'informes'})
            lista = []
            for i in int:
                lista.append(i.tipo)
                intervenciones = Counter(lista)
            if len(lista) == 0:
                return render(request, 'menu/informe-ranking-consultas.html',
                              {'form': form, 'not_found': True, 'nbar': 'informes'})
            return render(request, 'menu/resultado-informe-ranking-consultas.html', {'todas_intervencions': int, 'intervenciones': intervenciones, 'desde': desde, 'hasta': hasta, 'nbar': 'informes'})
    else:
        form = rankingConsultasTemaForm()
        return render(request, 'menu/informe-ranking-consultas.html', {'form': form, 'nbar': 'informes'})


@staff_member_required
def categorizacionAlumnos(request):
    if request.method == 'POST':
        form = rankingConsultasTemaForm(request.POST)
        if form.is_valid():
            try:
                desde = form.cleaned_data['desde']
                hasta = form.cleaned_data['hasta']
            except:
                return render(request, 'menu/informe-categorizacion-alumnos.html', {'form': form, 'error': True, 'nbar': 'informes'})
            try:
                alumnos = Alumno.objects.filter(fecha_alta__range=(desde, hasta))
            except:
                return render(request, 'menu/informe-categorizacion-alumnos.html', {'form': form, 'error': True, 'nbar': 'informes'})
            recursantes = {
                5: 0,
                8: 0,
                27: 0,
                84: 0
            }
            aprobados = {
                5: 0,
                8: 0,
                27: 0,
                84: 0
            }
            abandonaron = {
                5: 0,
                8: 0,
                27: 0,
                84: 0
            }
            codigos = {
                5: 'ISI',
                84: 'LAR',
                27: 'IQ',
                8: 'IEM'
            }
            for alu in alumnos:
                try:
                    alumnoSysacad = SysacadAlumno.objects.get(numerodocu=alu.dni)
                except:
                    continue
                if alu.recursante:
                    recursantes[alumnoSysacad.especialid] += 1
                if alu.dejo_seminario:
                    abandonaron[alumnoSysacad.especialid] += 1
                try:
                    materias_alumno = MateriaAlumno.objects.filter(especialid=900, legajo=alu.legajo)
                except:
                    continue
                if len(materias_alumno) == 3:
                    aprobados[alumnoSysacad.especialid] += 1
            totalAp = aprobados.get(5) + aprobados.get(84) + aprobados.get(27) + aprobados.get(8)
            totalRec = recursantes.get(5) + recursantes.get(84) + recursantes.get(27) + recursantes.get(8)
            totalAba = abandonaron.get(5) + abandonaron.get(84) + abandonaron.get(27) + abandonaron.get(8)
            return render(request, 'menu/resultado-informe-categorizacion-alumnos.html', {'recursantes': recursantes,
                                                                               'aprobados': aprobados,
                                                                               'abandonaron': abandonaron,
                                                                               'desde': desde, 'hasta': hasta,
                                                                               'nbar': 'informes',
                                                                               'totAp': totalAp, 'totRec': totalRec,
                                                                               'totAba': totalAba, 'cod': codigos})
    else:
        form = rankingConsultasTemaForm()
        return render(request, 'menu/informe-categorizacion-alumnos.html', {'form': form, 'nbar': 'informes'})

@staff_member_required
def estadoEscuelas(request):
    if request.method == 'POST':
        form = rankingConsultasTemaForm(request.POST)
        if form.is_valid():
            try:
                desde = form.cleaned_data['desde']
                hasta = form.cleaned_data['hasta']
            except:
                return render(request, 'menu/informe-escuela.html', {'form': form, 'error': True, 'nbar': 'informes'})
            try:
                alumnos = Alumno.objects.filter(fecha_alta__range=(desde, hasta))
            except:
                return render(request, 'menu/informe-escuela.html', {'form': form, 'error': True, 'nbar': 'informes'})

            recursantes = {
                'Tecnica': 0,
                'No tecnica': 0,
                'P': 0,
                'R': 0,
                None: 0
            }
            aprobados = {
                'Tecnica': 0,
                'No tecnica': 0,
                'P': 0,
                'R': 0,
                None: 0
            }
            abandonaron = {
                'Tecnica': 0,
                'No tecnica': 0,
                'P': 0,
                'R': 0,
                None: 0
            }
            for alu in alumnos:
                try:
                    personaSysacad = SysacadPersona.objects.get(numerodocu=alu.dni)
                    escuelaSysacad = SysacadEscuela.objects.get(escuela=personaSysacad.escuela).tipoescuel
                except:
                    continue
                if alu.recursante:
                    recursantes[alu.tipo_escuela] += 1
                    recursantes[escuelaSysacad] += 1
                if alu.dejo_seminario:
                    abandonaron[alu.tipo_escuela] += 1
                    abandonaron[escuelaSysacad] += 1
                try:
                    materias_alumno = MateriaAlumno.objects.filter(especialid=900, legajo=alu.legajo)
                except:
                    continue
                if len(materias_alumno) == 3:
                    aprobados[alu.tipo_escuela] += 1
                    aprobados[escuelaSysacad] += 1
            totalAp = aprobados.get('P') + aprobados.get('R') + aprobados.get(None)
            totalRec = recursantes.get('P') + recursantes.get('R') + recursantes.get(None)
            totalAba = abandonaron.get('P') + abandonaron.get('R') + abandonaron.get(None)
            return render(request, 'menu/resultado-informe-escuela.html', {'recursantes': recursantes,
                    'aprobados': aprobados, 'abandonaron': abandonaron, 'desde': desde, 'hasta': hasta, 'nbar': 'informes',
                    'totAp': totalAp, 'totRec': totalRec, 'totAba': totalAba})
    else:
        form = rankingConsultasTemaForm()
        return render(request, 'menu/informe-escuela.html', {'form': form, 'nbar': 'informes'})

# PARA LAS MATERIAS
@staff_member_required
def listarMaterias(request):
    if request.method == 'GET':
        materias = Materia.objects.all()
        return render(request, 'menu/panel-materias.html', {'materias': materias, 'nbar': 'administrador'})


@staff_member_required
def agregarMateria(request):
    if request.method == 'POST':
        form = agregarEditarMateriaForm(request.POST)
        if form.is_valid():
            nueva_materia = Materia(
                materia=str(form.cleaned_data['materia']),
                especialidad=str(form.cleaned_data['especialidad'])
            )
            Materia.save(nueva_materia)
            form = agregarEditarMateriaForm()
            return render(request, 'menu/alta-materia.html', {'form': form, 'materia': nueva_materia,
                                                              'success': True, 'nbar': 'administrador'})
        else:
            return render(request, 'menu/alta-materia.html', {'form': form,  'nbar': 'administrador'})
    else:
        form = agregarEditarMateriaForm()
        return render(request, 'menu/alta-materia.html', {'form': form, 'nbar': 'administrador'})


@staff_member_required
def eliminarMateria(request, id):
    if request.method == 'GET':
        try:
            materia = Materia.objects.get(id=id)
        except:
            return redirect('menu:index')
        materia.delete()
        return redirect('menu:index')
    else:
        return redirect('menu:index')


@staff_member_required
def editarMateria(request, id):
    try:
        materia = Materia.objects.get(id=id)
    except:
        return render(request, 'menu/editar-materia.html', {'not_found': True, 'nbar': 'administrador'})
    form = agregarEditarMateriaForm(instance=materia)
    if request.method == 'POST':
        form = agregarEditarMateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return render(request, 'menu/editar-materia.html', {'form': form, 'success': True, 'materia': materia, 'nbar': 'administrador'})
        else:
            form = agregarEditarMateriaForm(instance=materia)
            return render(request, 'menu/editar-materia.html', {'form': form, 'nbar': 'administrador', 'not_found': True})
    else:
        return render(request, 'menu/editar-materia.html', {'form': form, 'materia': materia, 'nbar': 'administrador'})
