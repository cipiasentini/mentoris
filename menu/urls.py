from django.urls import path
from . import views

app_name = 'menu'

# el name es el nombre al cual debemos referenciar desde los templates o el codigo html.
urlpatterns = [
    path('', views.verNovedades, name = 'index'),
    path('nuevo/alumno', views.agregarAlumno, name = 'alta-alumno'),
    path('editar/alumno/<int:dni>/', views.editarAlumno, name='editar-alumno'),
    path('buscar/alumno', views.buscarAlumno, name = 'buscar-alumno'),
    path('buscar/alumno/<int:id>', views.buscarAlumnoId, name = 'buscar-alumno-id'),
    path('nuevo/tutor', views.agregarTutor, name = 'alta-tutor'),
    path('nuevo/tutor-manual', views.agregarTutorPersonalizado, name = 'alta-tutor-personalizada'),
    path('buscar/tutor', views.buscarTutor, name = 'buscar-tutor'),
    path('editar/tutor/<int:legajo>/', views.editarTutor, name='editar-tutor'),
    path('editar/tutor/baja/<int:legajo>/', views.bajaTutor, name='baja-tutor'),
    path('editar/tutor/alta/<int:legajo>/', views.altaTutor, name='alta-tutor'),
    path('nueva/intervencion', views.agregarIntervencion, name = 'alta-intervencion'),
    path('nueva/intervencion/tipo', views.agregarIntervencionTipo, name = 'alta-tipo-intervencion'),
    path('editar/intervencion/<int:id>/', views.editarIntervencion, name='editar-intervencion'),
    path('intervenciones', views.listarIntervenciones, name = 'intervenciones'),
    path('intervenciones/cerrar/<int:id>/', views.cerrarIntervencion, name = 'cerrar-intervencion'),
    path('intervenciones/abrir/<int:id>/', views.abrirIntervencion, name = 'abrir-intervencion'),
    path('intervenciones/eliminar/<int:id>/', views.eliminarIntervencion, name = 'eliminar-intervencion'),
    path('buscar/alumno/cerrar/<int:id>/', views.cerrarIntervencionB, name = 'cerrar-intervencion-b'),
    path('buscar/alumno/abrir/<int:id>/', views.abrirIntervencionB, name = 'abrir-intervencion-b'),
    path('novedades/panel', views.panelNovedades, name = 'panel-novedades'),
    path('novedades/panel/cerrar/<int:id>/', views.cerrarNovedad, name = 'cerrar-novedad'),
    path('novedades/panel/abrir/<int:id>/', views.abrirNovedad, name = 'abrir-novedad'),
    path('novedades/panel/eliminar/<int:id>/', views.eliminarNovedad, name = 'eliminar-novedad'),
    path('nueva/novedad', views.agregarNovedad, name = 'alta-novedad'),
    path('editar/novedad/<int:id>/', views.editarNovedad, name = 'editar-novedad'),
    path('update_session/<int:collapse>/', views.update_session, name = 'update-session'),
    path('estadisticas', views.estadisticas, name = 'estadisticas'),
    path('password', views.change_password, name='change_password'),
    path('nueva/tarea', views.agregarTarea, name='alta-tarea'),
    path('agenda/<int:year>/<int:month>/<int:day>/', views.bcal, name='agenda-tareas'),
    path('tarea/<int:id>/', views.mostrarTareaId, name='tarea'),
    path('editar/tarea/<int:id>/', views.editarTarea, name='editar-tarea'),
]
