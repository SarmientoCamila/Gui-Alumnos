
import calendar
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CalendarioMensual:
    def __init__(self, master):
        self.master = master
        self.hoy = datetime.today()
        self.anio = self.hoy.year
        self.mes = self.hoy.month

        self.cal_frame = ttk.Frame(master)
        self.cal_frame.pack(padx=20, pady=20)

        self.titulo = ttk.Label(self.cal_frame, text="", font=("Helvetica", 16, "bold"))
        self.titulo.grid(row=0, column=0, columnspan=7, pady=10)

        self.header_frame = ttk.Frame(self.cal_frame)
        self.header_frame.grid(row=1, column=0, columnspan=7)

        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            ttk.Label(self.header_frame, text=dia, font=("Helvetica", 16, "bold")).grid(row=0, column=i, padx=10)

        self.body_frame = ttk.Frame(self.cal_frame)
        self.body_frame.grid(row=2, column=0, columnspan=7, sticky="nsew")

        nav_frame = ttk.Frame(self.cal_frame)
        nav_frame.grid(row=3, column=0, columnspan=7, pady=10)
        ttk.Button(nav_frame, text="⏪ Mes anterior", bootstyle=SECONDARY, command=self.mes_anterior).pack(side="left", padx=10)
        ttk.Button(nav_frame, text="Mes siguiente ⏩", bootstyle=SECONDARY, command=self.mes_siguiente).pack(side="left", padx=10)

        self.mensaje_label = ttk.Label(self.cal_frame, text="")
        self.mensaje_label.grid(row=4, column=0, columnspan=7, pady=10)

        self.generar_calendario()

    def generar_calendario(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        self.titulo.config(text=f"{calendar.month_name[self.mes]} {self.anio}")

        cal = calendar.Calendar(firstweekday=0)  # Lunes como primer día
        dias_mes = cal.monthdayscalendar(self.anio, self.mes)

        for row_idx, semana in enumerate(dias_mes):
            for col_idx, dia in enumerate(semana):
                if dia == 0:
                    ttk.Label(self.body_frame, text="").grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")
                else:
                    b = ttk.Button(self.body_frame, text=str(dia), width=4, bootstyle=INFO,
                                   command=lambda d=dia: self.dia_seleccionado(d))
                    b.grid(row=row_idx, column=col_idx, padx=3, pady=3, sticky="nsew")

        for i in range(7):
            self.body_frame.columnconfigure(i, weight=1)

    def mes_anterior(self):
        if self.mes == 1:
            self.mes = 12
            self.anio -= 1
        else:
            self.mes -= 1
        self.generar_calendario()

    def mes_siguiente(self):
        if self.mes == 12:
            self.mes = 1
            self.anio += 1
        else:
            self.mes += 1
        self.generar_calendario()

    def dia_seleccionado(self, dia):
        fecha = f"{dia:02d}/{self.mes:02d}/{self.anio}"
        print(f"Seleccionaste: {fecha}")
        self.mensaje_label.config(text=f"Seleccionaste: {fecha}", foreground="blue")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    app.title("Calendario con TTK")
    app.geometry("500x400")

    calendario = CalendarioMensual(app)

    app.mainloop()
