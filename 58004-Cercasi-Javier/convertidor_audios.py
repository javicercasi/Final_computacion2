from pydub import AudioSegment

audio = AudioSegment.from_mp3(r"/home/javi/Final_computacion2/58004-Cercasi-Javier/Boca.mp3")
audio.export("boqui.wav", format="wav")