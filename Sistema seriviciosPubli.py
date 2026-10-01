import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ===============================
# CLASE ABSTRACTA
# ===============================
class ServicioPublico:
    def __init__(self, consumo, tarifa):
        self._consumo = consumo
        self._tarifa = tarifa

    def calcular_costo(self):
        raise NotImplementedError("Método abstracto")

    def calcular_total(self):
        costo = self.calcular_costo()
        recargo = costo * 0.05
        return costo + recargo

# ===============================
# CLASES HIJAS
# ===============================
class Energia(ServicioPublico):
    def __init__(self, consumo):
        super().__init__(consumo, 536)

    def calcular_costo(self):
        return self._consumo * self._tarifa

class Agua(ServicioPublico):
    def __init__(self, consumo):
        super().__init__(consumo, 730)

    def calcular_costo(self):
        return self._consumo * self._tarifa

class Gas(ServicioPublico):
    def __init__(self, consumo):
        super().__init__(consumo, 710)

    def calcular_costo(self):
        return self._consumo * self._tarifa

# ===============================
# HISTORIAL
# ===============================
class Historial:
    def __init__(self):
        self.registros = []

    def agregar(self, servicio, consumo, total):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registros.append(f"{fecha} | {servicio} | Consumo: {consumo} | Total: ${total:.2f}")

    def obtener(self):
        return self.registros

# ===============================
# INTERFAZ GRÁFICA
# ===============================
class SistemaServiciosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema SaaS - UNIR S.A.")
        self.root.geometry("500x500")
        self.root.configure(bg="#2C3E50")

        self.historial = Historial()

        # Título
        titulo = tk.Label(root, text="Sistema de Servicios Públicos",
                          font=("Arial", 16, "bold"),
                          bg="#2C3E50", fg="white")
        titulo.pack(pady=10)

        # Frame principal
        frame = tk.Frame(root, bg="#34495E")
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Consumo
        tk.Label(frame, text="Consumo:", bg="#34495E", fg="white").pack(pady=5)
        self.txt_consumo = tk.Entry(frame, font=("Arial", 12))
        self.txt_consumo.pack(pady=5)

        # Servicio
        tk.Label(frame, text="Servicio:", bg="#34495E", fg="white").pack(pady=5)
        self.combo = ttk.Combobox(frame, values=["Energía", "Agua", "Gas"])
        self.combo.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(frame, bg="#34495E")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Calcular", command=self.calcular,
                  bg="#1ABC9C", fg="white", width=10).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Limpiar", command=self.limpiar,
                  bg="#E74C3C", fg="white", width=10).grid(row=0, column=1, padx=5)

        # Resultado
        self.lbl_resultado = tk.Label(frame, text="Resultado: ",
                                     bg="#34495E", fg="white", font=("Arial", 12))
        self.lbl_resultado.pack(pady=10)

        # Historial
        tk.Label(frame, text="Historial:", bg="#34495E", fg="white").pack()

        self.lista_historial = tk.Listbox(frame, height=10)
        self.lista_historial.pack(fill="both", padx=10, pady=5)

    def calcular(self):
        try:
            consumo = float(self.txt_consumo.get())
            servicio_tipo = self.combo.get()

            if consumo < 0:
                raise ValueError

            if servicio_tipo == "Energía":
                servicio = Energia(consumo)
            elif servicio_tipo == "Agua":
                servicio = Agua(consumo)
            elif servicio_tipo == "Gas":
                servicio = Gas(consumo)
            else:
                messagebox.showwarning("Error", "Seleccione un servicio")
                return

            total = servicio.calcular_total()

            self.lbl_resultado.config(text=f"Total a pagar: ${total:.2f}")

            # Guardar historial
            self.historial.agregar(servicio_tipo, consumo, total)
            self.actualizar_historial()

        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")

    def limpiar(self):
        self.txt_consumo.delete(0, tk.END)
        self.combo.set("")
        self.lbl_resultado.config(text="Resultado:")

    def actualizar_historial(self):
        self.lista_historial.delete(0, tk.END)
        for registro in self.historial.obtener():
            self.lista_historial.insert(tk.END, registro)

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaServiciosApp(root)
    root.mainloop()
