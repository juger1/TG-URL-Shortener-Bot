#Author: StupidBoi
#Telegram: https://t.me/StupidBoi69

FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
