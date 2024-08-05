#db_options.py
import sqlite3
from tkinter import messagebox
import time

def create_db():
    db_path = r'dataBase.db'
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT UNIQUE,
                        codigo TEXT UNIQUE,
                        correo TEXT,
                        contraseña TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sugerencias (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        autor TEXT,
                        sugerencia TEXT,
                        fecha TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reclamos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        autor TEXT,
                        reclamo TEXT,
                        fecha TEXT)''')
    
    conexion.commit()
    conexion.close()

def register_user(nombreusuario, codigousuario, correo, contrasena, contrasenarepe):
    db_path = r'dataBase.db'
    conexion = None
    retries = 5
    while retries > 0:
        try:
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT usuario, codigo FROM usuarios WHERE usuario = ? OR codigo = ?", 
                           (nombreusuario, codigousuario))
            if cursor.fetchone():
                messagebox.showinfo(message="El usuario o el código ya están registrados en el sistema.", title="Aviso")
            else:
                if contrasena == contrasenarepe:
                    cursor.execute("INSERT INTO usuarios (usuario, codigo, correo, contraseña) VALUES (?, ?, ?, ?)", 
                                   (nombreusuario, codigousuario, correo, contrasena))
                    conexion.commit()
                    messagebox.showinfo(message="Registro exitoso!", title="Aviso")
                else:
                    messagebox.showinfo(message="Las contraseñas no coinciden", title="Aviso")
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries -= 1
                time.sleep(1)
            else:
                raise
        except sqlite3.IntegrityError as e:
            messagebox.showinfo(message="Error de integridad: el usuario o el código ya existen.", title="Error")
            break
        finally:
            if conexion:
                conexion.close()

def validate_login(codigo, contrasena, main_menu_callback):
    db_path = r'dataBase.db'
    conexion = None
    retries = 5
    while retries > 0:
        try:
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT contraseña FROM usuarios WHERE codigo = ? AND contraseña = ?", 
                           (codigo, contrasena))
            if cursor.fetchone():
                messagebox.showinfo(title="Inicio de sesión correcto", message="Codigo y contraseña correctos")
                main_menu_callback()
                return True
            else:
                messagebox.showinfo(title="Inicio de sesión incorrecto", message="Codigo o contraseña incorrectos")
                return False
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries -= 1
                time.sleep(1)
            else:
                raise
        finally:
            if conexion:
                conexion.close()
    return False
