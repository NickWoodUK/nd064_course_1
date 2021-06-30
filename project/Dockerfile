FROM python:3.8
LABEL maintainer="Nick Wood"
LABEL description="This text illustrates \
that label-values can span multiple lines."


COPY /techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "app.py" ].
