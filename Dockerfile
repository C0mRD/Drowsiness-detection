FROM jhonatans01/python-dlib-opencv
COPY . /app
WORKDIR /app
RUN pip3 install -r docker-requirements.txt
CMD ["gunicorn", "-k", "eventlet", "main:app"]
