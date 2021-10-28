FROM python:3.9

COPY counterfit-app /counterfit-app

WORKDIR /counterfit-app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT python3 src/__main__.py