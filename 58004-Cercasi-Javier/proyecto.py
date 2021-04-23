import os
import asyncio
from pedido import argumentos
from convertidor_doc import pdf_to_word , word_to_pdf
from convertidor_imag import imagenes
from os import remove
import array
import queue, threading
from convertidor_audios import audio
argsdocumentroot = os.getcwd()
argssize = 10000


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon", "mp3":"audio/mp3", "wav":"audio/wav", "aif":"audio/aif", "flac":"audio/flac", "ogg":"audio/ogg"}
    fin = True

    data = await reader.read(800000)
    fin = True
    extension = ""
    control = 0

    encabezado = data.decode().splitlines()[0] # GET /imagen.jpg

    archivo = argsdocumentroot + encabezado.split()[1]
    addr = writer.get_extra_info('peername')

    if len(encabezado) > 30:
        encabezado = encabezado.replace("&"," ").replace("="," ").replace("?"," ")
        lista = encabezado.split(" ")
        archivo = argsdocumentroot+"/"+lista[3]
        extension = lista[5]

    if archivo == (argsdocumentroot + "/"):
        archivo = argsdocumentroot + '/index.html'

    if os.path.isfile(archivo) is False and os.path.isfile(archivo+"."+extension) is False :
        archivo = argsdocumentroot + '/400error.html'
        codigo = "HTTP/1.1 400 File Not Found"
        control = 1
        extension = "html"

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


    if extension == "ogg" or extension == "mp3" or extension == "wav" or extension == "flac" or extension == "aif":
        #print("AUDIOOO",archivo+"."+extension, lista[7])
        archivo = audio(archivo+"."+extension, lista[7])

    # Conversor Documentos:
    q = queue.Queue()

    if extension == "docx":
        hilo = threading.Thread(target=pdf_to_word, args=(archivo+".pdf", q,))
    
    elif extension == "pdf":
        hilo = threading.Thread(target=word_to_pdf, args=(archivo+".docx", q,))

    # Conversor de Imagenes:
    if extension == "jpg" or extension == "png" or extension == "ppm" or extension == "jpeg" or extension == "BMP" or extension == "gif" or extension == "TIFF" or extension == "EPS":
        hilo = threading.Thread(target=imagenes, args=(lista[3], lista[5], lista[7], q,))
        extension = lista[7]
    
    if extension != "html" and extension != "ico" and extension != "ogg" and extension != "mp3" and extension != "wav" and extension != "flac" :
        hilo.start()
        archivo = q.get()
        hilo.join()

    header = bytearray(codigo + "\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    writer.write(header)

    fd = os.open(archivo, os.O_RDONLY)
    fin = True
    while fin is True:
        body = os.read(fd, argssize)
        writer.write(body)
        if (len(body) != argssize):
            os.close(fd)
            try:
                await writer.drain()
            except ConnectionResetError:
                pass
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