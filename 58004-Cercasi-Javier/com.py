

from pdf2docx import Converter
import os

# # # dir_path for input reading and output files & a for loop # # #

path_input = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'
path_output = '/home/javi/Final_Computacion/58004-Cercasi-Javier/pdfs/'

for file in os.listdir(path_input):
    cv = Converter(path_input+file)
    cv.convert(path_output+file+'.docx', start=0, end=None)
    cv.close()
    print(file)