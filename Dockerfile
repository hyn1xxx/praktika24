FROM python:3.12-slim

WORKDIR /bot
VOLUME  C:\Docker\pgdev:/var/lib/sqlite/data

COPY requirements.txt ./
RUN pip install -r req.txt

COPY . /bot

CMD ["python", "main.py"]