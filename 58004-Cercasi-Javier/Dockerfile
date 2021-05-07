FROM python:3           

RUN git clone https://github.com/javicercasi/Final_computacion2.git

WORKDIR /Final_computacion2/58004-Cercasi-Javier

RUN apt-get update && apt-get install -y ffmpeg && apt-get install -y libreoffice
#apt-get install -y abiword

RUN pip3 install -r requirements.txt

CMD ["python3", "proyecto.py", "-p", "5000", "-s", "20000", "-d", "/Final_computacion2/58004-Cercasi-Javier"]

#CMD ["python3", "./proyecto.py"]

#docker build -t server .         docker run -t server