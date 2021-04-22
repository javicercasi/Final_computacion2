import os
import asyncio
import array
from os import remove
argsdocumentroot = os.getcwd()



async def handle_echo(reader, writer):

    dic = {"txt": " text/plain", "jpg": " image/jpeg", "ppm": " image/x-portable-pixmap", "html": " text/html", "pdf": " application/pdf", "ico": "image/x-icon"}
    data = b''
    data = await reader.read()

    print("\n\n\n\n",data)
    i = 0
    try:
        archi = data.split(b"image/x-portable-pixmap\r\n\r\n")[1]
    except:
        pass

    #archi1 = open("datos.ppm","wb")
    #image = array.array('B', archi)
    #image.tofile(archi1)
    
    with open('datos.ppm', 'wb') as f:
        f.write(bytearray(archi))








    #Anda bien:
    try:
        encabezado = data.decode().splitlines()[0]  # GET /imagen.jpg
        archivo = argsdocumentroot + encabezado.split()[1]
    except:
        pass    


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