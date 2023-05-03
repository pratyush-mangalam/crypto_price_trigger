FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]