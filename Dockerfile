FROM python:3

RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "web2bus.py"]