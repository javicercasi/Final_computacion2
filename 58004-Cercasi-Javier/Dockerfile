FROM python:3           

RUN git clone https://github.com/javicercasi/Final_computacion2.git


WORKDIR /Final_computacion2/58004-Cercasi-Javier

RUN pip freeze > requirementss.txt
#RUN apt install ffmpeg

RUN pip3 install requests

RUN pip3 install -r requirementss.txt

CMD ["python3", "./proyecto.py"]