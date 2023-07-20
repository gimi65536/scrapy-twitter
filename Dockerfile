FROM python:3.11.4-bullseye

ENV GRAB_INFO=tweet.yml

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

RUN mkdir history
COPY . .

CMD ["python3", "-u", "app.py"]