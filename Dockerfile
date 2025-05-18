# aspyn-utils/Dockerfile
FROM python:3.13
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ /app
COPY assets/ /app/assets
COPY system.json /app/system.json

CMD [ "python", "main.py" ]
