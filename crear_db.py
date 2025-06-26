import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("colegio.sqlite")
cursor = conn.cursor()

# Crear tabla alumnos
cursor.execute("""
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apellido TEXT NOT NULL,
    nombre TEXT NOT NULL,
    curso TEXT NOT NULL
)
""")

# Crear tabla inasistencias
cursor.execute("""
CREATE TABLE IF NOT EXISTS inasistencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER,
    mes TEXT,
    clase_normal INTEGER,
    ed_fisica INTEGER,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
)
""")

# Insertar alumnos si está vacío
cursor.execute("SELECT COUNT(*) FROM alumnos")
if cursor.fetchone()[0] == 0:
    alumnos = [
        ("Pérez", "Juan", "2do Año"),
        ("García", "Ana", "2do Año"),
        ("Díaz", "Leo", "3er Año"),
        ("Fernández", "Lucía", "3er Año")
    ]
    cursor.executemany("INSERT INTO alumnos (apellido, nombre, curso) VALUES (?, ?, ?)", alumnos)

conn.commit()
conn.close()

print("✔ Base de datos creada con éxito.")

