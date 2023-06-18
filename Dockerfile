FROM python:3.11.4-bullseye

ENV GRAB_INFO=tweet.yml
ARG BROWSER=firefox
ENV BROWSER=$BROWSER
WORKDIR /etc/scrapy

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN playwright install $BROWSER
RUN playwright install-deps

RUN mkdir history
COPY . .

CMD ["python3", "-u", "grab.py"]