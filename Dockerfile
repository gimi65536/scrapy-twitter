FROM python:3.11.1-alpine

ARG browser=firefox
ENV GRAB_INFO=tweet.yml

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN playwright install $browser

COPY . .

CMD ["python3", "-u", "grab.py"]