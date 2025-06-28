
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ver_calendario import CalendarioMensual

# --- CONEXIÓN A BASE ---
def obtener_alumnos_por_curso(curso):
    with sqlite3.connect("colegio.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, apellido, nombre FROM alumnos WHERE curso = ?", (curso,))
        return cursor.fetchall()

def guardar_inasistencias(datos):
    with sqlite3.connect("colegio.sqlite") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO inasistencias (alumno_id, mes, clase_normal, ed_fisica) VALUES (?, ?, ?, ?)", datos
        )
        conn.commit()

# --- GUI PRINCIPAL ---
app = ttk.Window(themename="flatly")
app.title("Sistema de Inasistencias")
app.geometry("700x600")

def limpiar_ventana():
    for widget in app.winfo_children():
        widget.destroy()

def mostrar_inicio():
    limpiar_ventana()
    ttk.Label(app, text="Bienvenida Precep Rocio 👩‍🏫", font=("Helvetica", 18, "bold")).pack(pady=30)
    for curso in ["2do Año", "3er Año"]:
        ttk.Button(app, text=f"Curso {curso}", width=30, bootstyle=PRIMARY,
                   command=lambda c=curso: abrir_menu_curso(c)).pack(pady=10)

def abrir_menu_curso(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"Menú de {curso}", font=("Helvetica", 16, "bold")).pack(pady=20)
    ttk.Button(app, text="Ingresar inasistencias por mes", width=30, bootstyle=SUCCESS,
               command=lambda: ingresar_inasistencias(curso)).pack(pady=10)
    ttk.Button(app, text="Ver total por mes (Calendario)", width=30, bootstyle=INFO,
               command=lambda: mostrar_calendario(curso)).pack(pady=10)
    ttk.Button(app, text="Volver al inicio", bootstyle=SECONDARY, command=mostrar_inicio).pack(pady=20)

def ingresar_inasistencias(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"Ingresar inasistencias - {curso}", font=("Helvetica", 16, "bold")).pack(pady=10)

    ttk.Label(app, text="Mes:", font=("Helvetica", 12)).pack()
    meses = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_combo = ttk.Combobox(app, values=meses)
    mes_combo.pack(pady=5)

    alumnos = obtener_alumnos_por_curso(curso)
    entradas = []

    for alumno_id, apellido, nombre in alumnos:
        frame = ttk.Frame(app)
        frame.pack(pady=5, fill="x", padx=20)
        ttk.Label(frame, text=f"{apellido}, {nombre}", width=25).pack(side="left")
        clase_entry = ttk.Entry(frame, width=5); clase_entry.insert(0, "0"); clase_entry.pack(side="left", padx=10)
        edfis_entry = ttk.Entry(frame, width=5); edfis_entry.insert(0, "0"); edfis_entry.pack(side="left", padx=10)
        entradas.append((alumno_id, clase_entry, edfis_entry))

    def guardar():
        mes = mes_combo.get()
        if not mes:
            ttk.Label(app, text="Seleccioná un mes antes de guardar.", foreground="red").pack()
            return
        datos = []
        for alumno_id, clase_entry, edfis_entry in entradas:
            try:
                clase = int(clase_entry.get())
                edfis = int(edfis_entry.get())
                if clase < 0 or edfis < 0:
                    raise ValueError
                datos.append((alumno_id, mes, clase, edfis))
            except ValueError:
                ttk.Label(app, text="⚠️ Verificá que todas las inasistencias sean números válidos.", foreground="red").pack()
                return
        guardar_inasistencias(datos)
        ttk.Label(app, text="✅ Inasistencias guardadas con éxito.", foreground="green").pack(pady=10)

    ttk.Button(app, text="Guardar", bootstyle=SUCCESS, command=guardar).pack(pady=15)
    ttk.Button(app, text="Volver", bootstyle=SECONDARY, command=lambda: abrir_menu_curso(curso)).pack(pady=10)

def mostrar_calendario(curso):
    limpiar_ventana()
    ttk.Label(app, text=f"📅 Calendario de Inasistencias - {curso}", font=("Helvetica", 16, "bold")).pack(pady=10)
    contenedor = ttk.Frame(app); contenedor.pack(fill="both", expand=True)
    CalendarioMensual(contenedor, curso)
    ttk.Button(app, text="🔙 Volver", bootstyle=SECONDARY, command=lambda: abrir_menu_curso(curso)).pack(pady=10)

mostrar_inicio()
app.mainloop()
