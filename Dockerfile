FROM python:3-slim

ADD . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "update_ip.py"]

