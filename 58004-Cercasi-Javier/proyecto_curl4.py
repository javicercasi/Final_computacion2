import os, asyncio, array, socket, queue, threading
from os import remove
from pedido import argumentos
from convertidor_doc import pdf_to_word , word_to_pdf
from convertidor_imag import imagenes
from convertidor_audios import audio
argsdocumentroot = os.getcwd()
argssize = 1000000


async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon", "mp3":"audio/mp3", "wav":"audio/wav", "aif":"audio/aif", "flac":"audio/flac", "ogg":"audio/ogg"}
    data = b''
    fin = True
    data = await reader.read(100)
    error = 0
 
    encabezado = data.decode().splitlines()[0] # GET /imagen.jpg

    if encabezado.split()[0] == "GET":
        archivo = argsdocumentroot + encabezado.split()[1]
        #print("ARchivo pedido", archivo)
    
    if encabezado.split()[0] == "POST":

        print("DATAAAAAAA",data)

        
        if (b'User-Agent: curl') in data:
            print("SI HAYYYYYYYYYYY")
        else:
            print("NO HAYYYYYYYYY")
        data = await reader.readuntil(separator=b'--\r\n')
        entrada = data.split(b" filename=")[1].split(b'\r\n')[0].split(b'"')[1].decode()
        extension_in = entrada.split(".")[1]
        #datos = data.split(b'\r\n\r\n')[3]
        #extension_out = data.split(b"\r\n\r\n")[2].split(b"\r\n")[0].decode()
        datos = data.split(b'\r\n\r\n')[2]
        #print(data)
        part = data.split(b'output=')[1].split(b';')[0].decode()
        print(part)

        print("Archivo recibido",entrada,"EXTENSION_IN:",extension_in) #, "EXTENSION_OUT",extension_out )
        with open(entrada, 'wb') as f:
            f.write(bytearray(datos))

        archivo = entrada

    if archivo == (argsdocumentroot + "/"):
        archivo = argsdocumentroot + '/index.html'

    if archivo == "Error":
        archivo = argsdocumentroot + '/500error.html'
        codigo = "HTTP/1.1 500 Internal Server Error"
        extension_out = "html"

    if os.path.isfile(archivo) is False:
        archivo = argsdocumentroot + '/400error.html'
        codigo = "HTTP/1.1 400 File Not Found"
        extension_out = "html"
    
    else:
        extension_out = archivo.split('.')[1]
        codigo = "HTTP/1.1 200 OK"

    header = bytearray(codigo + "\r\nContent-type:" +
                       dic[extension_in] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')

    
    print("ARCHIVO", archivo)

    
    writer.write(header)
    fd = os.open(archivo, os.O_RDONLY)
    body = os.read(fd, int(os.path.getsize(archivo)))
    writer.write(body)
    await writer.drain()
    writer.close()
    if archivo.split(".")[1] != "html" and archivo.split(".")[1] != "py" and archivo.split(".")[1] != extension_out:
        remove(archivo)


async def main():
    #ip = '192.168.0.106'
    ip = "127.0.0.1"
    #ip = socket.gethostbyname(socket.gethostname())
    server = await asyncio.start_server(
        handle_echo, host=[str(ip)], port=5000, loop=None, limit=50000000) 

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())