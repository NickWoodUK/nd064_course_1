FROM python:3.8
LABEL maintainer="Nick Wood"
LABEL "org.opencontainers.image.description"="Tech Trends Project Services"

COPY /techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "app.py" ].
