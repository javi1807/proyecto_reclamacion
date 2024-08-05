from tkinter import *
from tkinter import colorchooser

def elegir_color():
    color = colorchooser.askcolor()
    if color[1]:
        label.config(text=color[1], bg=color[1])
        
root = Tk()
label=Label(root, text="Color", bg="white")
label.pack()
    
btn=Button(root, text="elegir", command=elegir_color)
btn.pack()
    
root.mainloop()
    