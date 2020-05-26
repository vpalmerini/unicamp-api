# UNICAMP API

## Description

This project intends to serve as a REST API for accessing [Unicamp](https://www.unicamp.br/unicamp/)'s (_University of Campinas_) data. All data for now is obtained by _web scraping_ and the main source of data is the university's website/system.

This first version has the following types of data:

- _Institutes_
- _Courses_
- _Subjects_
- _Classes_
- _Professors_
- _Students_

## Project

The project is built on top of [Django](https://www.djangoproject.com/) and has the following folder structure:

- `api/` - this is the project's main folder (created by Django when the project is created)
- `requirements.txt` - list of dependencies needed to run the application
- `.env/` - folder with environment variables to be defined (more on that later)
- `.vscode/` - folder that contains `tasks.json` which has some VS Code tasks to be run
- `{apps}/` - all other folders are `Django apps`. Each entity acts as an app and it holds its own configuration
- `Dockerfile` - file where we define how API's Docker image should be built
- `docker-compose.yml` - file that defines our docker services (in this case _Django_ and _Postgres_) and allows us to start and stop these services in a very convenient way

### Motivation

The motivation is to have an _resource_ where people (Unicamp students mainly) could get data about Unicamp easily. It could be useful for both academic purpose and applications in general (like bots and web apps). Also, the ideia is to create a project where anybody can contribute with more data or new demands.

This first version gets all data by web scraping. But is very likely that in a near future different data sources can appear.

## Tech Stack

If you want to contribute in some way, it is strongly recommended that you have at least a basic knowledge of the main technologies used in this project. Those are:

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

> Don't worry if you have never worked with Django. It has a very simple and nice API.

Most of the data is collected by web scraping using:

- [Selenium](https://selenium-python.readthedocs.io/)

And the relational database is managed by:

- [Postgres](https://www.postgresql.org/)

## Running Locally

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3](https://docs.python.org/3/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [ChromeDriver](https://chromedriver.chromium.org/)

#### Running

1. Clone the repository

```shell
# https
$ git clone https://github.com/vpalmerini/unicamp-api.git

# ssh
$ git clone git@github.com:vpalmerini/unicamp-api.git
```

2. Initialize a _virtual environment_

```shell
# initialize environment
$ pipenv install

# start environment
$ pipenv shell
```

> You can also create it by using [venv](https://docs.python.org/3/library/venv.html)

3. Install all dependencies in the environment

You may need to install some packages related with `psycopg`. Those are:

```
# debian
$ sudo apt-get install postgresql-libs postgresql-dev python-dev

# redhat/fedora
$ sudo dnf install postgresql-libs postgresql-devel python-devel
```

Then:

```shell
$ pip install -r requirements.txt
```

4. Now is time to scrapy the data. For that, run:

```shell
$ ./scrapy.sh
```

> Assuming that `Chrome driver` is placed in `/usr/local/lib/chromedriver`

> This will scrapy all data that was defined: _intitutes_, _courses_, _subjects_, _classes_, _students_ and _professors_. If it's really what you want, it will take a while...I mean, I'm talking about hours :coffee::coffee::coffee::coffee::coffee:

5. Create a folder named `.env` with the following files:

```
# django.env
SUPERUSER_NAME={superuser}
SUPERUSER_EMAIL={superuser-email}
SUPERUSER_PASSWORD={superuser-password}
DJANGO_SETTINGS_MODULE=api.settings
```

```
# postgres.env
POSTGRES_SERVER=postgres
POSTGRES_USER={user}
POSTGRES_PASSWORD={password}
POSTGRES_DB={database-name}
```

> Fill in the fields with {}.

6. `scrapy.sh` script will create a `.json` file with the data scraped for each entity in its respective folder. After that, it's time to populate the database and start the server (finally!):

```shell
$ docker-compose up -d
```

To access Django's `admin panel`, go to `localhost:8000/admin` and enter with the superuser credentials defined in the previous section.

The API will be available in `localhost:8000/api/v1/` base route.
A more detailed documentation about the endpoints will be relased soon.

### License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
