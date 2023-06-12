FROM mcr.microsoft.com/playwright/python:v1.34.0-jammy

ARG browser=firefox
ENV GRAB_INFO=tweet.yml

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
RUN playwright install $browser

COPY . .

CMD ["python3", "-u", "grab.py"]