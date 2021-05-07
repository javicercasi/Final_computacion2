import os
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

def word_to_pdf(entrada_word, q):

    salida_pdf = entrada_word.split(".")[0]+'.pdf'
    output = subprocess.check_output(['unoconv', '-f', 'pdf' ,entrada_word])
    ##output = subprocess.check_output(['abiword', '--to=pdf',entrada_word])
    #abiword --to=pdf pasos.docx
    q.put(salida_pdf)
