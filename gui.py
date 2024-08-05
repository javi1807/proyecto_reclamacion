#gui.py
import tkinter as tk
from tkinter import PhotoImage, messagebox
from sugerencias import Sugerencias
from reclamos import Reclamos
from db_operations import register_user, validate_login, create_db

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reclamos y Sugerencias")
        self.geometry("300x380")
        self._load_images()
        self._setup_main_screen()

        # Crear la base de datos si no existe
        create_db()

    def _load_images(self):
        self.usuario_image = PhotoImage(file="usuario.png").subsample(2, 2)
        self.menu_image = PhotoImage(file="img/img.png").subsample(1, 1)

    def _setup_main_screen(self):
        tk.Label(self, text="Acceso al Sistema", bg="#004040", fg="white", width=250, height=3, font=("Comic Sans MS", 15)).pack()
        tk.Label(self, text="").pack()

        label = tk.Label(self, image=self.usuario_image)
        label.pack()

        tk.Button(self, text="Iniciar Sesión", bg="#1e7880", fg="white", height=3, width=30, command=self._login_screen).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Registrarse", bg="#bebebe", fg="black", height=3, width=30, command=self._register_screen).pack()

    def _login_screen(self):
        pantalla1 = tk.Toplevel(self)
        pantalla1.geometry("350x250")
        pantalla1.title("Inicio de Sesión")

        tk.Label(pantalla1, text="Ingrese su Usuario o código y contraseña", width=250, bg="#004040", fg="white").pack()
        tk.Label(pantalla1, text="").pack()

        codigo_verify = tk.StringVar()
        contrasena_verify = tk.StringVar()

        tk.Label(pantalla1, text="Código").pack()
        tk.Entry(pantalla1, textvariable=codigo_verify).pack()
        tk.Label(pantalla1).pack()

        tk.Label(pantalla1, text="Contraseña").pack()
        tk.Entry(pantalla1, show="*", textvariable=contrasena_verify).pack()
        tk.Label(pantalla1).pack()

        tk.Button(pantalla1, text="Iniciar Sesión", bg="#1e7880", fg="white", command=lambda: self._validate_login(codigo_verify, contrasena_verify, pantalla1)).pack()

    def _register_screen(self):
        pantalla2 = tk.Toplevel(self)
        pantalla2.geometry("300x400")
        pantalla2.title("Registrarse")

        tk.Label(pantalla2, text="Por favor complete la siguiente información", width=300, bg="#004040", fg="white").pack()
        tk.Label(pantalla2, text="").pack()

        correousuario_entry = tk.StringVar()
        nombreusuario_entry = tk.StringVar()
        codigousuario_entry = tk.StringVar()
        contrasena_entry = tk.StringVar()
        contrasenarepe_entry = tk.StringVar()

        tk.Label(pantalla2, text="Correo").pack()
        tk.Entry(pantalla2, textvariable=correousuario_entry).pack()
        tk.Label(pantalla2).pack()

        tk.Label(pantalla2, text="Nombre de usuario").pack()
        tk.Entry(pantalla2, textvariable=nombreusuario_entry).pack()
        tk.Label(pantalla2).pack()

        tk.Label(pantalla2, text="Código").pack()
        tk.Entry(pantalla2, textvariable=codigousuario_entry).pack()
        tk.Label(pantalla2).pack()

        tk.Label(pantalla2, text="Contraseña").pack()
        tk.Entry(pantalla2, textvariable=contrasena_entry, show="*").pack()
        tk.Label(pantalla2).pack()

        tk.Label(pantalla2, text="Repita contraseña").pack()
        tk.Entry(pantalla2, textvariable=contrasenarepe_entry, show="*").pack()
        tk.Label(pantalla2).pack()

        tk.Button(pantalla2, text="Registrarse", bg="#1e7880", fg="white", command=lambda: self._register_user(nombreusuario_entry, codigousuario_entry, correousuario_entry, contrasena_entry, contrasenarepe_entry, pantalla2)).pack()

    def _register_user(self, nombreusuario, codigousuario, correo, contrasena, contrasenarepe, window):
        register_user(nombreusuario.get(), codigousuario.get(), correo.get(), contrasena.get(), contrasenarepe.get())
        window.destroy()

    def _validate_login(self, codigo, contrasena, window):
        success = validate_login(codigo.get(), contrasena.get(), self.pantalla_menu)
        if success:
            window.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def pantalla_menu(self):
        self.title("Menú Principal")
        self.geometry("300x400")
        self._pantalla_menu()

    def _pantalla_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        tk.Label(self, text="Menú principal", bg="#004040", fg="white", width=250, height=3, font=("Comic Sans", 14)).pack()
        tk.Label(self, text="").pack()
        
        label = tk.Label(self, image=self.menu_image)
        label.pack()

        tk.Button(self, text="RECLAMOS", command=self.open_reclamos, font=("Comic Sans", 12), bg='#1e7880', fg='white', width=20).pack(pady=20)
        tk.Button(self, text="SUGERENCIAS", command=self.open_sugerencias, font=("Comic Sans", 12), bg='#bebebe', fg='white', width=20).pack(pady=20)

    def open_reclamos(self):
        self.new_window = tk.Toplevel(self)
        Reclamos(self.new_window, False)

    def open_sugerencias(self):
        self.new_window = tk.Toplevel(self)
        Sugerencias(self.new_window, False)
        