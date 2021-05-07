import os, sys
import subprocess
from pdf2docx import Converter

def pdf_to_word(entrada_pdf, q):
    try:
        salida_doc = entrada_pdf.split(".")[0]+'.docx'
        cv = Converter(entrada_pdf)
        cv.convert(salida_doc, start=0, end=None)
        cv.close()
        q.put(salida_doc)
    except:
        q.put("Error")

def word_to_pdf(entrada_word):

    salida_pdf = entrada_word.split(".")[0]+'.pdf'
    output = subprocess.check_output(['abiword', '--to=pdf',entrada_word])
    #os.system ("clear") 
    #borrarPantalla = lambda: os.system ("clear")
    #borrarPantalla()
word_to_pdf("Archivos/pasos.docx")
