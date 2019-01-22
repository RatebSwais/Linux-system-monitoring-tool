FROM python:latest

MAINTAINER Rateb "rfswais@gmail.com"

EXPOSE 5000

COPY . /app

WORKDIR /app

RUN pip install flask && pip install psutil && pip install pygal

ENTRYPOINT ["python"]

CMD ["app.py"]
