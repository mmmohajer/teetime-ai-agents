FROM python:3.12.11-slim-bookworm

LABEL Developer="Mohammad Mahdi Mohajer"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# System dependencies for PDF, OpenCV, Playwright/Chromium, .doc, and .pdf generator
RUN apt-get update && apt-get install -y \
    poppler-utils gcc libpq-dev libglib2.0-0 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libasound2 curl gnupg apt-transport-https libgl1-mesa-glx libpangocairo-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libcairo2 pandoc ffmpeg

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/src/app/docker-entrypoint-prod.sh

EXPOSE 8000

RUN useradd app
RUN chown -R app:app .
USER app