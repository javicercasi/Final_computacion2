import os
import subprocess
from pdf2docx import Converter

def pdf_to_word(file=0):
    file = "enunciado.pdf"
    path_input = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    path_output = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    cv = Converter(path_input+file)
    cv.convert(path_output+file.split(".")[0]+'.docx', start=0, end=None)
    cv.close()

pdf_to_word()

def word_to_pdf():
    output = subprocess.check_output(['unoconv', '-f', 'pdf' ,'/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/enunciado.pdf.docx'])
