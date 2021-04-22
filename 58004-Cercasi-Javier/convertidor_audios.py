from pydub import AudioSegment
from pydub.playback import play
from concurrent import futures
duracion = 0
tema = b""

def hilo(cota):
    t = 1000
    intervalo = int(duracion / 5)
    anterior = int(cota) 
    superior = int(cota + intervalo)
    
    if superior > duracion or superior == duracion - 1:
        superior = duracion
    parte = tema[anterior*t:superior*t]
    #parte = (anterior,superior)
    return (parte)

def audio(direccion, salida):

    mix = 0
    global duracion, tema
    tema = AudioSegment.from_mp3(r"{}".format(direccion))
    #duracion = int(audio.duration_seconds) + 1
    duracion = 14
    hilos = futures.ThreadPoolExecutor(max_workers=5)
    resultado_a_futuro = hilos.map(hilo ,range(0,duracion,int(duracion/5)))
    for elemento in list(resultado_a_futuro):
        mix += elemento
        #print(elemento)
    mix.export("Mix."+salida, format=salida)
    play(mix)
    return("Mix."+salida)

direccion = "/home/javi/Final_computacion2/58004-Cercasi-Javier/Boca.mp3"
salida = "wav"
audio(direccion, salida)
