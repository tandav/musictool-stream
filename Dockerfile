FROM tandav/musictool-stream

RUN mkdir -p /app/musictool_stream && mkdir -p /app/static && touch /app/credentials.py
WORKDIR /app
COPY static /app/static
COPY musictool_stream /app/musictool_stream
CMD ["python", "-m", "musictool_stream.daw", "video"]
