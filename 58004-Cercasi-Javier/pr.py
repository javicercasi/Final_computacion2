import os
import asyncio
import array
from os import remove
argsdocumentroot = os.getcwd()
from PIL import Image


def imagenes(output):
    formato = "jpg"
    entrada = "datos.jpg"
    #print("LLEGUEE", entrada+'.'+formato, entrada+'.'+output)
    im = Image.open("datos.jpg")
    rgb_im = im.convert('RGB')
    rgb_im.save("gato."+output, quality=95)
    return("gato."+output)


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon"}
    
    data = b''
    fin = True
    data = await reader.read(100)
    """while fin is True:
        pedido = await reader.read(1024)
        data += pedido
        if len(pedido) < 1024:
            fin = False
    fin = True"""
 
    encabezado2 = data.decode().splitlines()  # GET /imagen.jpg
    encabezado = encabezado2[0]
    print("ENCA", encabezado)
    if encabezado.split()[0] == "GET":
        archivo = argsdocumentroot + encabezado.split()[1]
    if encabezado.split()[0] == "POST":

        data = await reader.read(500000)
        
        #print(encabezado2, "\n\n\n\n", data)
        archi = data.split(b'\r\n\r\n')[3]
        output = data.split(b"\r\n\r\n")[2].split(b"\r\n")[0]
        output = output.decode()
        #print("dataaaaaaaaaa", data, "archiii", archi)
        print("putttttt",output)
        with open('datos.ppm', 'wb') as f:
            f.write(bytearray(archi))
        #archivo = imagenes(output)
        archivo = argsdocumentroot + "/datos.ppm"


    if archivo == (argsdocumentroot + "/"):
        archivo = argsdocumentroot + '/index.html'

    if os.path.isfile(archivo) is False:
        archivo = argsdocumentroot + '/400error.html'
        codigo = "HTTP/1.1 400 File Not Found"
        extension = "html"

    elif len(encabezado.split()[1].split("?")) != 1:
        archivo = argsdocumentroot + '/500error.html'
        codigo = "HTTP/1.1 500 Internal Server Error"
        extension = "html"

    else:
        extension = archivo.split('.')[1]
        codigo = "HTTP/1.1 200 OK"
    print("EXTEEEEEEE", archivo, extension)

    header = bytearray(codigo + "\r\nContent-type:" +
                       dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    
    
    writer.write(header)
    print("ARCHIIIIIIII",archivo, "EXTENSION", extension)
    fd = os.open(archivo, os.O_RDONLY)
    body = os.read(fd, os.path.getsize(archivo))
    writer.write(body)
    os.close(fd)
    await writer.drain()
    writer.close()


async def main():

    server = await asyncio.start_server(
        handle_echo, ['::1', '127.0.0.1'], 5000)

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())