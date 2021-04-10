from concurrent import futures

def tarea(archivo):
    return (archivo+"HOLAA")

archivo = "ASD"
hijo = futures.ProcessPoolExecutor()
futuro = hijo.submit(tarea,archivo)
resultado = futuro.result()
print(resultado)