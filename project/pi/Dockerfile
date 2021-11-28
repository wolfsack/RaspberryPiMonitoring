FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /app .

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]