# Futureself

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple clone of <a href="https://futureme.org"> futureme </a> that allows users send letters as emails to their future selves <br>
Built with Django, Celery and RabbitMQ.

## Setup
To set up this project locally, make sure you have  <a href="https://docker.com"> Docker </a> installed.


Clone the repository
```
git clone https://github.com/klvxn/futureself
```
<br>

Navigate into project's root directory
```
cd futureself
``` 
<br>

Start the docker daemon and build docker images
```
docker-compose build .
```
<br>

Start the containers
```
docker-compose up
```

