FROM python:latest
WORKDIR /bot
ADD . /bot

RUN pip install instagrapi Pillow moviepy

CMD ["python3", "-u", "main.py"]