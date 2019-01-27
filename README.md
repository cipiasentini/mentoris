# Preguntar a Bianca:
1. Si le gustaria mas buscar el tutor por nombre que por DNI/Legajo (seguramente si)?
2. Los grupos se borran? Con que periodicidad? O queda todo guardado nomas...

---

## To-Do:
##### Funcionalidades
1. Ver como hacer para que los grupos se borren automaticamente al iniciar un nuevo ciclo lectivo.
2. Generacion de reportes y formato para impresion/exportacion PDF
3. Pedir a la mendez tabla de escuela y seminario con datos.
4. Agregar datos faltantes del alumno segun el mail: creo que falta lo de la escuela y el seminario universitario.
5. Agregar a "buscar tutor" estilo solapas donde muestre info personal y grupos a su cargo.


##### Bugs:
7. Fixear el problema de display en pantallas chicas (celulares)
8. Refactorizar buscarAlumnoId (creo que esta demas, la borre por el momento y parece no afectar nada...)

## Work in progress:
6. Ver alumnos a cargo de un tutuor, que liste nomas los vagos y que le deje seleccionar como para ver sus datos.

## Done:
4. Pantalla de "buscar/editar tutor" agregar funcionalidad a editar y dar de baja tutor
5. Agregar Editar intervenciones
3. Management completo de tareas de tutores: falta editar tarea y verificar formato.
6. Poner modales a todos los eliminar/dar de baja que existan.
9. Ver como dar de baja usuario de un tutor al dar de baja el tutor (baja logica tendria que ser porque fisica se van a perder las cosas hechas por ese tutor).
Entonces posible solucion: hay que ver como hacer para que al setear "fecha_desvinculacion", se cambie la contraseña del usuario. Asi si se lo vuelve a dar de alta se le da la contraseña por defecto.
9. Ver que hacer con lo de todos los estados (activa/inactiva) de los modelos (ejemplo tarea, tutor, etc).
10. El calendario, ver como limitar los elementos, que los tutores solo vean lo suyo. Y Bianca todo.
8. Ver como funcionan las tablas de matcom y eso para poder determinar las notas y si regularizo/aprobo una determinada materia, (y parciales).
12. Creacion de grupos.
1. Management completo de grupos: falta busqueda y edicion.

--- 

## SI SOBRA TIEMPO:
-  Ver como mejorar la logica de la busqueda de materias y notas por alumno (porque lo hace secuencialmente actualmente, buscar-alumno-atomico.html).
 igual esto no nos pidio, asi que nada..