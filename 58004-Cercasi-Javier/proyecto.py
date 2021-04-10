import os
import asyncio
from pedido import argumentos
from convertidor_doc import pdf_to_word , word_to_pdf
from convertidor_imag import imagenes
from os import remove
from concurrent import futures
argsdocumentroot = os.getcwd()
argssize = 10000


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon"}
    data = await reader.read(100)
    extension = ""
    control = 0
    encabezado = data.decode().splitlines()[0]  # GET /imagen.jpg
    archivo = argsdocumentroot + encabezado.split()[1].split("?")[0]
    addr = writer.get_extra_info('peername')

    if len(encabezado) > 30:
        encabezado = encabezado.replace("&"," ").replace("="," ").replace("?"," ")
        lista = encabezado.split(" ")
        archivo = argsdocumentroot+"/"+lista[3]
        extension = lista[5]

    if archivo == (argsdocumentroot + "/"):
        archivo = argsdocumentroot + '/index.html'

    #if os.path.isfile(archivo) is False and os.path.isfile(archivo+"."+extension) is False :
    #    archivo = argsdocumentroot + '/400error.html'
    #    codigo = "HTTP/1.1 400 File Not Found"
    #    control = 1
    #    extension = "html"

    if len(encabezado.split()[1].split("?")) != 1:
        archivo = argsdocumentroot + '/500error.html'
        codigo = "HTTP/1.1 500 Internal Server Error"
        extension = "html"

    else:
        codigo = "HTTP/1.1 200 OK"
        try:
            if control == 0:
                extension= lista[5]
        except:
            extension = archivo.split('.')[1]

    #print("EXTENsion", extension, archivo)
    #print("EXT", extension)
    # Conversor Documentos:
    hijo = futures.ProcessPoolExecutor()

    if extension == "docx":
        funcion = pdf_to_word
        argumentos = archivo+".pdf"


        futuro = hijo.submit(funcion,argumentos)
        archivo = futuro.result()
        #archivo = pdf_to_word(archivo+".pdf")

    elif extension == "pdf":
        archivo = word_to_pdf(archivo+".docx")

    print("ARCGHI", archivo, "ADS", extension )

    # Conversor de Imagenes:
    if extension == "jpg" or extension == "png" or extension == "ppm" or extension == "jpeg" or extension == "BMP" or extension == "gif" or extension == "TIFF" or extension == "EPS":
        archivo = imagenes(lista[3], lista[5], lista[7])
        extension = lista[7]
    
    #hilo = threading.Thread(target=funcion, args=(argumentos,))
    #hilo.start()
    #hilo.join()

    header = bytearray(codigo + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    writer.write(header)
    print("Archivoooooo salida:", archivo)

    fd = os.open(archivo, os.O_RDONLY)
    fin = True
    while fin is True:
        body = os.read(fd, argssize)
        writer.write(body)
        if (len(body) != argssize):
            os.close(fd)
            await writer.drain()
            fin = False
    writer.close()
    #remove(str(archivo))



async def main():

    server = await asyncio.start_server(
        handle_echo, ['::1', '127.0.0.1'], 5000)

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)



    async with server:
        await server.serve_forever()

asyncio.run(main())