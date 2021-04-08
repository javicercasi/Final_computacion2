import os
import subprocess
from pdf2docx import Converter

def pdf_to_word():
    file="enunciado.pdf"
    entrada_pdf = os.getcwd()+"/"+file
    salida_doc = entrada_pdf.split(".")[0]+'.docx'
    cv = Converter(entrada_pdf)
    cv.convert(salida_doc, start=0, end=None)
    cv.close()
    return(salida_doc)

def word_to_pdf():
    file = "enunciado.docx"
    entrada_word = os.getcwd()+"/"+file
    salida_pdf = entrada_word.split(".")[0]+'.pdf'
    output = subprocess.check_output(['unoconv', '-f', 'pdf' ,entrada_word])
    return(salida_pdf)

#print(word_to_pdf())
#print(pdf_to_word())