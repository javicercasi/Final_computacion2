from PIL import Image


def imagenes(entrada, formato, output, q):
    print("LLEGUEE", entrada+'.'+formato, entrada+'.'+output)
    im = Image.open(entrada+'.'+formato)
    rgb_im = im.convert('RGB')
    rgb_im.save(entrada+"."+output, quality=95)
    q.put(entrada+'.'+output)
    #return(entrada+'.'+output)
