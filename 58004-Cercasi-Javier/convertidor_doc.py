import os
import subprocess
from pdf2docx import Converter

def pdf_to_word(file=0, ):
    file = "enunciado.pdf"
    #path_input = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    #path_output = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
    cv = Converter(os.getcwd()+"/"+file)
    cv.convert(os.getcwd()+"/"+file.split(".")[0]+'.docx', start=0, end=None)
    cv.close()
    return(os.getcwd()+"/"+file.split(".")[0]+'.docx')

def word_to_pdf():
    file = "enunciado.docx"
    output = subprocess.check_output(['unoconv', '-f', 'pdf' ,os.getcwd()+"/"+file])
    return(os.getcwd()+"/"+file.split(".")[0]+'.pdf')

#word_to_pdf()
#pdf_to_word()