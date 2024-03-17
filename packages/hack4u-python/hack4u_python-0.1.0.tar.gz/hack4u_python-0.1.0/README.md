# Hack4u Academy Courses Library

Una biblioteca Python para consultar los cursos de Hack4u

## Cursos disponibles

- Introduccion a Linux [15 horas]
- Personalizacion de Linux [3 horas]
- Introduccion al Hacking [53 horas]

## Instalacion

Instala el paquete usando `pip3`:

```python3
pip3 install hack4u
```

## Uso basico

### Listar todos los cursos

```python3
from hack4u import list_courses

for course in list_courses:
    print(course)
```

### Obtener un curso por nombre

```python3
from hack4u import search_course_by_name

course = search_course_by_name("Introduccion a Linux")
print(course)
```

### Calcular la duracion total de los cursos

```python3
from hack4u import total_duration:

print(f"Duracion total: {total_duration()} horas")
```
