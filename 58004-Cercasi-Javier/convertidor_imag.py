from PIL import Image


def imagenes(entrada, output, q):

    salida = entrada.split(".")[0]+'.'+output
    im = Image.open(entrada)
    rgb_im = im.convert('RGB')
    rgb_im.save(salida, quality=95)
    q.put(salida)
    #return(entrada+'.'+output)
