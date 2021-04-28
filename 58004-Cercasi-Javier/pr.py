import os
import asyncio
from pedido import argumentos
from convertidor_doc import pdf_to_word , word_to_pdf
from convertidor_imag import imagenes
from os import remove
import array
import socket
import queue, threading
from convertidor_audios import audio
argsdocumentroot = os.getcwd()
argssize = 10000


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon"}
    
    data = b''
    fin = True
    data = await reader.read(100)
 
    encabezado = data.decode().splitlines()[0] # GET /imagen.jpg

    if encabezado.split()[0] == "GET":
        archivo = argsdocumentroot + encabezado.split()[1]
        print("ARchivo pedido", archivo)
    
    if encabezado.split()[0] == "POST":
        
        data = await reader.readuntil(separator=b'--\r\n')
        entrada = data.split(b" filename=")[1].split(b'\r\n')[0].split(b'"')[1].decode()
        extension_in = entrada.split(".")[1]
        datos = data.split(b'\r\n\r\n')[3]
        extension_out = data.split(b"\r\n\r\n")[2].split(b"\r\n")[0].decode()
        print("ENTRADA", entrada, "EXTENSION_ENTRADA:",extension_in, "EXTENSION_OUT", str(extension_out))
        with open(entrada, 'wb') as f:
            f.write(bytearray(datos))

        # Conversor Documentos:
        q = queue.Queue()

        if extension_out == "docx":
            hilo = threading.Thread(target=pdf_to_word, args=(entrada, q,))
        
        elif extension_out == "pdf":
            hilo = threading.Thread(target=word_to_pdf, args=(entrada, q,))

        # Conversor de Imagenes:
        if extension_in == "jpg" or extension_in == "png" or extension_in == "ppm" or extension_in == "jpeg" or extension_in == "BMP" or extension_in == "gif" or extension_in == "TIFF" or extension_in == "EPS":
            hilo = threading.Thread(target=imagenes, args=(entrada, extension_out, q,))
            extension = extension_out
        
        if extension_in != "html" and extension_in != "ico" and extension_in != "ogg" and extension_in != "mp3" and extension_in != "wav" and extension_in != "flac" :
            hilo.start()
            archivo = q.get()
            hilo.join()

        #archivo = argsdocumentroot + "/datos."+extension_out


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
    ip = '127.0.0.1'
    #ip = socket.gethostbyname(socket.gethostname())
    server = await asyncio.start_server(
        handle_echo, host=[str(ip)], port=5000, loop=None, limit=500000) 

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())