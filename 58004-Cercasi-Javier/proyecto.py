import os
import asyncio
from pedido import argumentos
from convertidor_doc import pdf_to_word , word_to_pdf
#args = argumentos()
#argsdocumentroot = "/home/javi/Final_Computacion/58004-Cercasi-Javier"
argsdocumentroot = os.getcwd()
argssize = 10000


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon"}
    data = await reader.read(100)
    encabezado = data.decode().splitlines()[0]  # GET /imagen.jpg
    archivo = argsdocumentroot + encabezado.split()[1].split("?")[0]
    addr = writer.get_extra_info('peername')

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

    header = bytearray(codigo + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    writer.write(header)

    #Tratado de archivo:

    #if extension == "pdf":
    #   archivo = pdf_to_word()
    """if extension == "docx":
        archivo = word_to_pdf()"""
    
    print("ARCHIVO", archivo, dic[extension])
    
    fd = os.open(archivo, os.O_RDONLY)
    body = os.read(fd, 100000)
    writer.write(body)
    writer.close()
    
    """fin = True
    while fin is True:
        body = os.read(fd, argssize)
        writer.write(body)
        if (len(body) != argssize):
            os.close(fd)
            await writer.drain()
            fin = False
    writer.close()"""


async def main():

    server = await asyncio.start_server(
        handle_echo, ['::1', '127.0.0.1'], 5000)

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())