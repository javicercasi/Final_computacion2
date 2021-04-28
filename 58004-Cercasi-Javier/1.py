import os
import asyncio
import array
from os import remove
argsdocumentroot = os.getcwd()
import socket

async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "pdf":"application/pdf", "jpg": " image/jpeg", "TIFF": " image/TIFF", "gif": " image/gif", "png": " image/png", "BMP": " image/BMP", "EPS": " image/EPS", "jpeg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "docx": "application/docx", "ico": "image/x-icon"}
    
    data = b''
    fin = True
    data = await reader.read(100)
 
    encabezado = data.decode().splitlines()[0] # GET /imagen.jpg

    if encabezado.split()[0] == "GET":
        archivo = argsdocumentroot + encabezado.split()[1]
        print("ARchivo pedido", archivo)
        
        if archivo == (argsdocumentroot + "/"):
            archivo = argsdocumentroot + '/index.html'
        extension = archivo.split('.')[1]
    
    if encabezado.split()[0] == "POST":

        data = await reader.readuntil(separator=b'--\r\n')
        extension = "png"
        print("LENNNNN", len(data))
        datos = data.split(b'\r\n\r\n')[3]


        with open('datos.'+extension, 'wb') as f:
            f.write(bytearray(datos))

        archivo = argsdocumentroot + "/datos."+extension

    codigo = "HTTP/1.1 200 OK"
    header = bytearray(codigo + "\r\nContent-type:" +
                       dic[extension] + "\r\nContent-length:"+str((os.path.getsize(archivo)))+"\r\n\r\n", 'utf8')
    
    
    writer.write(header)
    fd = os.open(archivo, os.O_RDONLY)
    body = os.read(fd, os.path.getsize(archivo))
    writer.write(body)
    os.close(fd)
    await writer.drain()
    writer.close()


async def main():

    server = await asyncio.start_server(
        handle_echo, host=["127.0.0.1"], port=5000, loop=None, limit=500000) 

    addr = server.sockets[0].getsockname()
    print("\nServidor en:", addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())