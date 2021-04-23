FROM python:3           

RUN git clone https://github.com/javicercasi/Final_computacion2.git


WORKDIR /Final_computacion2/58004-Cercasi-Javier

#RUN pip freeze > requirementss.txt
#RUN pip3 install ffmpeg

RUN pip3 install requests

#RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt
#RUN pip3 install pdf2docx
#RUN pip3 install pillow
#RUN pip3 install pydub
CMD ["python3", "./pr.py"]