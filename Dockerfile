ARG PYTHON_VERSION=3.10.4

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py collectstatic --noinput


