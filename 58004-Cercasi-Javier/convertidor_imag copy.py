from PIL import Image


def imagenes(entrada=0):
    im = Image.open('1.png')
    rgb_im = im.convert('RGB')
    rgb_im.save('2.tiff', quality=95)


imagenes()
#im = Image.open('logo-python.jpg')
#im.save('logo-python-2.png')



#im = Image.open('logo-python.png')
#rgb_im = im.convert('RGB')
#rgb_im.save('logo-python.jpg', quality=95)