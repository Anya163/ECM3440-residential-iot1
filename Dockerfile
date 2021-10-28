FROM python:3.9

COPY prosperity /prosperity

RUN useradd prosperity

RUN chown prosperity /prosperity
 
WORKDIR /prosperity

RUN pip install -r requirements-prosperity.txt

EXPOSE 5000

USER prosperity

ENTRYPOINT python3 main.py