FROM python:3.8

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt --no-cache-dir

RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

