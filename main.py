#main.py
import tkinter as tk
from gui import Application
from db_operations import create_db, register_user, validate_login

if __name__ == "__main__":
    create_db()
    app = Application()
    app.mainloop()