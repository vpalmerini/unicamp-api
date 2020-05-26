## UNICAMP API

This is a REST API for data of the University of Campinas (a.k.a [Unicamp](https://www.unicamp.br/))

### Motivation

The motivation is to have an _resource_ where people (Unicamp students mainly) could get data about Unicamp easily. It could be useful for both academic purpose and applications in general (like bots and web apps). Also, the ideia is to create a project where anybody can contribute with more data or new demands.

### Technologies

##### API

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

##### Data

Most of the data is collected by web scraping

- [Selenium](https://selenium-python.readthedocs.io/)

##### Database

- [Postgres](https://www.postgresql.org/)

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

##### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

##### Running

```shell
# run the scripts to populate the database (this could take a few minutes)
# and run the server
docker-compose up --build
```

Now you can access `http://localhost:8000/admin` to look at the models that were created and the endpoints as well (those are in progress).

### License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
