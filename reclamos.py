import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3

class Reclamos:
    db_name = r'dataBase.db'

    def __init__(self, window, ver=False):
        self.wind = window
        self.wind.title('Menú Principal')
        self.wind.geometry("300x450")
        self.ver = ver

        # Cambiar el color de fondo de la ventana principal
        self.wind.configure(bg='#e7e7e7')  # Color de fondo gris claro

        # Estilo para los botones
        style = ttk.Style()
        style.configure('TButton', background='#005b5b', foreground='#004040', font=('Arial', 10, 'bold'))
        style.map('TButton', background=[('active', '#003d3d')])

        frame = tk.LabelFrame(self.wind, text='RECLAMOS\nIngrese su reclamo', labelanchor='n', bg='#008080', fg='#ffffff', font=('Arial', 12, 'bold'))
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        if not self.ver:
            tk.Label(frame, text='Autor: ', bg='#008080', fg='#ffffff').pack(anchor=tk.W, pady=5)
            self.author = ttk.Entry(frame, font=('Arial', 12))
            self.author.pack(fill=tk.X, pady=5)
            self.author.focus()

            tk.Label(frame, text='Fecha: ', bg='#008080', fg='#ffffff').pack(anchor=tk.W, pady=5)
            self.date = ttk.Entry(frame, font=('Arial', 12))
            self.date.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.date.pack(fill=tk.X, pady=5)

            tk.Label(frame, text='A continuación ingrese su reclamo detalladamente:', bg='#008080', fg='#ffffff').pack(anchor=tk.W, pady=5)
            self.reclamo = tk.Text(frame, height=6, font=('Arial', 12))
            self.reclamo.pack(fill=tk.BOTH, pady=5)

            button_frame = tk.Frame(frame, bg='#008080')
            button_frame.pack(fill=tk.X, pady=10)

            ttk.Button(button_frame, text='Volver al menú', command=self.wind.destroy, style='TButton').pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            ttk.Button(button_frame, text='Ver reclamos', command=self.ver_reclamos, style='TButton').pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

            ttk.Button(frame, text='Guardar Reclamo', command=self.add_reclamo, style='TButton').pack(fill=tk.X, pady=5)

        self.message = tk.Label(self.wind, text='', foreground='red', font=('Arial', 12), bg='#e7e7e7')
        self.message.pack(pady=10)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def validation(self):
        return len(self.author.get()) != 0 and len(self.reclamo.get("1.0", tk.END).strip()) != 0

    def add_reclamo(self):
        if self.validation():
            query = 'INSERT INTO Reclamos VALUES(NULL, ?, ?, ?)'
            parameters = (self.author.get(), self.reclamo.get("1.0", tk.END).strip(), self.date.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Reclamo {self.author.get()} añadido exitosamente'
            self.author.delete(0, tk.END)
            self.reclamo.delete("1.0", tk.END)
            self.date.delete(0, tk.END)
            self.date.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            self.message['text'] = 'Autor y Reclamo son requeridos'

    def ver_reclamos(self):
        self.new_window = tk.Toplevel(self.wind)
        self.new_window.geometry("800x600")
        self.new_window.title('Ver Reclamos')

        tree_frame = ttk.Frame(self.new_window)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, height=15, columns=('reclamo', 'fecha'))
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading('#0', text='Autor', anchor=tk.CENTER)
        self.tree.heading('#1', text='Reclamo', anchor=tk.CENTER)
        self.tree.heading('#2', text='Fecha', anchor=tk.CENTER)

        self.get_reclamos()

        ttk.Button(self.new_window, text='Cerrar', command=self.new_window.destroy).pack(pady=10)

    def get_reclamos(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM Reclamos ORDER BY fecha DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))
