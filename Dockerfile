#FROM python:3.9-alpine
#RUN apk add g++ && apk add ffmpeg && pip install numpy
#RUN apk add --no-cache freetype-dev jpeg-dev zlib-dev && apk add --no-cache --virtual .build-deps build-base linux-headers && pip install Pillow
#RUN apk add --no-cache freetype-dev jpeg-dev zlib-dev && apk add --no-cache --virtual .build-deps build-base linux-headers && pip install opencv-python
#RUN pip install mido pipe21

FROM python:3.10
#RUN pip install numpy Pillow mido pipe21 && apt update && apt install --yes ffmpeg

RUN apt update && apt install --yes ffmpeg vim
RUN pip install numpy opencv-python pipe21 requests Pillow musictool

RUN mkdir -p /app/musictool_stream && mkdir -p /app/static && touch /app/credentials.py
WORKDIR /app
COPY static /app/static
COPY musictool_stream /app/musictool_stream
CMD ["python", "-m", "musictool_stream.daw", "video"]
