# Futureself

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple clone of <a href="https://futureme.org"> futureme </a> that allows users send letters as emails to thier future selves <br>
Built with Django, Celery and RabbitMQ.

## Setup

Clone the repository

```
git clone https://github.com/klvxn/futureself
```

Navigate into project's root directory
```
cd futureself
```

Update package installer and install dependencies
```
pip install --upgrade pip

pip install -r requirements.txt
```
Run migrations
```
python3 manage.py migrate
```


Start local server
```
python3 manage.py runserver
```

Open a new terminal and start rabbitmq server and celery beat scheduler
```
service rabbitmq-server start

python3 -m celery -A futureSelf worker -l INFO -B -E
```
