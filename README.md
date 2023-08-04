# Argo Tech Test - Vacancy Python Developer

This is a project developed with Python and Django Rest Framework. The goal of this project is to provide a REST API for a wedding company.

## Installation

Before starting, it is recommended to check if you have docker and docker compose installed on the machine, if not, check how to install according to your operating system.

## Execution

Start application.

``` wsl
1 - docker-compose up --build
2 - Open a new wsl terminal
3 - docker-compose exec backend python manage.py makemigrations
4 - docker-compose exec backend python manage.py migrate
5 - docker-compose exec backend python manage.py createsuperuser
```

## Note:

To view Django/Admin go to [http://127.0.0.1:8000/admin].
Upload of the spreadsheet that will automate the creation of users must be provided with the following columns:
- email
- name
- user_type (guest, groom and bride)
Model worksheet next to the project

## Endpoints

Endpoints available in the API can be viewed by swagger
[http://127.0.0.1:8000/swagger/]
[http://127.0.0.1:8000/redoc/]

