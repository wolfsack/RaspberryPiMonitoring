FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /wrk

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /app /wrk/app

COPY wsgi.py wsgi.py

ENV ROOT_FS "/rootfs"

EXPOSE 5000

ENTRYPOINT [ "waitress-serve" ]

CMD ["--listen=*:5000", "wsgi:app"]