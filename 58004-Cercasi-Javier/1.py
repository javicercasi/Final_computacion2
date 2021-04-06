import tkinter as tk
from docx2pdf import convert
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo


def openfile():
    file = askopenfile(filetypes=[("word file", "*.docx")])
    convert('/home/javi/Final_Computacion/58004-Cercasi-Javier/Proyecto.docx', '/home/javi/Final_Computacion/58004-Cercasi-Javier/converted.pdf')


openfile()
