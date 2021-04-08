import os
import subprocess
from pdf2docx import Converter

def pdf_to_word(file):
    #path_input = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    #path_output = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    cv = Converter(file)
    salida = file.split(".")[0]+'.docx'
    print("FILE1",file, "SALIDI", salida)
    cv.convert(salida, start=0, end=None)
    cv.close()
    return(salida)

def word_to_pdf(file):
    #file = "enunciado.docx"
    print("FILE2",file)
    output = subprocess.check_output(['unoconv', '-f', 'pdf' ,"/"+file])
    return(file.split(".")[0]+'.pdf')

#word_to_pdf()
#pdf_to_word()