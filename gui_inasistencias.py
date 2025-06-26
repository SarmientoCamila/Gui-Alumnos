
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- CONEXIÓN A BASE ---
def obtener_alumnos_por_curso(curso):
    conn = sqlite3.connect("colegio.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, apellido, nombre FROM alumnos WHERE curso = ?", (curso,))
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos

def guardar_inasistencias(datos):
    conn = sqlite3.connect("colegio.sqlite")
    cursor = conn.cursor()
    for alumno_id, mes, clase_normal, ed_fisica in datos:
        cursor.execute("""
            INSERT INTO inasistencias (alumno_id, mes, clase_normal, ed_fisica)
            VALUES (?, ?, ?, ?)
        """, (alumno_id, mes, clase_normal, ed_fisica))
    conn.commit()
    conn.close()

# --- GUI PRINCIPAL ---
app = ttk.Window(themename="flatly")
app.title("Sistema de Inasistencias")
app.geometry("700x600")

# --- FUNCIONES DE NAVEGACIÓN ---
def limpiar_ventana():
    for widget in app.winfo_children():
        widget.destroy()

def mostrar_inicio():
    limpiar_ventana()
    ttk.Label(app, text="Bienvenida Precep Rocio 👩‍🏫", font=("Helvetica", 18, "bold")).pack(pady=30)

    ttk.Button(app, text="Curso 2do año", width=30, bootstyle=PRIMARY,
            command=lambda: abrir_menu_curso("2do Año")).pack(pady=10)

    ttk.Button(app, text="Curso 3er año", width=30, bootstyle=PRIMARY,
            command=lambda: abrir_menu_curso("3er Año")).pack(pady=10)

def abrir_menu_curso(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"Menú de {curso}", font=("Helvetica", 16, "bold")).pack(pady=20)

    ttk.Button(app, text="Ingresar inasistencias por mes", width=30, bootstyle=SUCCESS,
            command=lambda: ingresar_inasistencias(curso)).pack(pady=10)

    ttk.Button(app, text="Ver total por mes (Calendario)", width=30, bootstyle=INFO,
           command=lambda: ver_calendario(curso)).pack(pady=10)

    ttk.Button(app, text="Volver al inicio", bootstyle=SECONDARY, command=mostrar_inicio).pack(pady=20)

# --- INGRESO DE INASISTENCIAS ---
def ingresar_inasistencias(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"Ingresar inasistencias - {curso}", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Selector de mes
    ttk.Label(app, text="Mes:", font=("Helvetica", 12)).pack()
    meses = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_combo = ttk.Combobox(app, values=meses)
    mes_combo.pack(pady=5)

    ttk.Label(app, text="").pack()  # espacio

    alumnos = obtener_alumnos_por_curso(curso)
    entradas = []

    for alumno in alumnos:
        alumno_id, apellido, nombre = alumno
        frame = ttk.Frame(app)
        frame.pack(pady=5, fill="x", padx=20)

        nombre_label = ttk.Label(frame, text=f"{apellido}, {nombre}", width=25)
        nombre_label.pack(side="left")

        clase_normal_entry = ttk.Entry(frame, width=5)
        clase_normal_entry.pack(side="left", padx=10)
        clase_normal_entry.insert(0, "0")

        edfis_entry = ttk.Entry(frame, width=5)
        edfis_entry.pack(side="left", padx=10)
        edfis_entry.insert(0, "0")

        entradas.append((alumno_id, clase_normal_entry, edfis_entry))

    def guardar():
        mes = mes_combo.get()
        if not mes:
            ttk.Label(app, text="Seleccioná un mes antes de guardar.", foreground="red").pack()
            return
        datos = []
        for alumno_id, clase_entry, edfis_entry in entradas:
            try:
                clase_normal = int(clase_entry.get())
                edfis = int(edfis_entry.get())
                if clase_normal < 0 or edfis < 0:
                    raise ValueError
                datos.append((alumno_id, mes, clase_normal, edfis))
            except ValueError:
                ttk.Label(app, text="⚠️ Verificá que todas las inasistencias sean números válidos.", foreground="red").pack()
                return
        guardar_inasistencias(datos)
        ttk.Label(app, text="✅ Inasistencias guardadas con éxito.", foreground="green").pack(pady=10)

    ttk.Button(app, text="Guardar", bootstyle=SUCCESS, command=guardar).pack(pady=15)
    ttk.Button(app, text="Volver", bootstyle=SECONDARY, command=lambda: abrir_menu_curso(curso)).pack(pady=10)
def ver_calendario(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"Calendario de Inasistencias - {curso}", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Aquí se llamaría a la función ver_calendario del módulo ver_calendario
    ver_calendario(curso)
    #MOSTRAR EL CALENDARIO CON TODAS LAS INASISTENCIAS
    from ver_calendario import ver_calendario
    ver_calendario(curso)
    # Mostrar el calendario de inasistencias por mesa
    ttk.Label(app, text="Calendario de inasistencias por mes", font=("Helvetica", 12)).pack(pady=10)
    

    ttk.Button(app, text="Volver al menú del curso", bootstyle=SECONDARY,
            command=lambda: abrir_menu_curso(curso)).pack(pady=10)
# --- INICIO ---
mostrar_inicio()
app.mainloop()
