FROM python:3.11.5

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "bot.py"]
