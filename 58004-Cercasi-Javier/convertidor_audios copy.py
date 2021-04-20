from pydub import AudioSegment
from pydub.playback import play

audio = AudioSegment.from_mp3(r"/home/javi/Final_computacion2/58004-Cercasi-Javier/Boca.mp3")
#audio.export("boqui.wav", format="wav")
#reversed_aduio = audio.reverse()
#reversed_aduio.export("bos.mp3", format="mp3")
t = 1000
print(int(audio.duration_seconds))
incio = audio [0:5*t]
#ultimos = audio[-10000:]
ultimos = audio[5*t:8*t]
incio.export("Mix.ogg", format="ogg")

#incio = incio + 10
#ultimos = ultimos + 20

mix = incio + ultimos
#mix.export("Mix.mp3", format="mp3")
#play(mix)