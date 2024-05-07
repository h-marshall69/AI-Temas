import datetime

class Autor:
    def __init__(self, nombre, nacionalidad):
        self.nombre = nombre
        self.nacionalidad = nacionalidad

    def __str__(self):
        return f"Autor: {self.nombre} ({self.nacionalidad})"

class Libro:
    def __init__(self, titulo, autor, isbn, copias_disponibles):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.copias_disponibles = copias_disponibles

    def prestar(self):
        if self.copias_disponibles > 0:
            self.copias_disponibles -= 1
            return True
        else:
            return False

    def devolver(self):
        self.copias_disponibles += 1

    def __str__(self):
        return f"Libro: {self.titulo} - {self.autor.nombre} (ISBN: {self.isbn})"

class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def __str__(self):
        return f"Usuario: {self.nombre} ({self.email})"

class Prestamo:
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.date.today()
        self.fecha_devolucion = None

    def devolver_libro(self):
        self.libro.devolver()
        self.fecha_devolucion = datetime.date.today()

    def __str__(self):
        return f"Prestamo: {self.libro} - {self.usuario.nombre} ({self.fecha_prestamo})"

# Crear autores
autor1 = Autor("Gabriel García Márquez", "Colombiano")
autor2 = Autor("J.K. Rowling", "Británica")

# Crear libros
libro1 = Libro("Cien años de soledad", autor1, "978-0307474728", 5)
libro2 = Libro("Harry Potter y la piedra filosofal", autor2, "978-8478884457", 3)

# Crear usuarios
usuario1 = Usuario("Juan Pérez", "juan@example.com")
usuario2 = Usuario("María López", "maria@example.com")

# Realizar préstamos
prestamo1 = Prestamo(libro1, usuario1)
prestamo2 = Prestamo(libro2, usuario2)
libro1.prestar()
libro2.prestar()

# Mostrar información
print(autor1)
print(autor2)
print(libro1)
print(libro2)
print(usuario1)
print(usuario2)
print(prestamo1)
print(prestamo2)

# Devolver libros
prestamo1.devolver_libro()
prestamo2.devolver_libro()
print(libro1.copias_disponibles)
print(libro2.copias_disponibles)
