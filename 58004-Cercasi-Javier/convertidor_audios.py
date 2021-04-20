from pydub import AudioSegment
from pydub.playback import play
from concurrent import futures


def audio(incio, fin):
    audio = AudioSegment.from_mp3(r"/home/javi/Final_computacion2/58004-Cercasi-Javier/Boca.mp3")
    t = 1000
    duracion = int(audio.duration_seconds) + 1
    incio = audio [0:5*t]
    ultimos = audio[5*t:8*t]
    mix = incio + ultimos
    #mix.export("Mix.mp3", format="mp3")

def pensar(a):
    print("PASEE")
    #print(a)
    return(a)

#audio()
hilos = futures.ThreadPoolExecutor(max_workers=5) #max_workers=3)
resultado_a_futuro = hilos.map(pensar ,range(0,92,int(92/5)))
print(list(resultado_a_futuro))