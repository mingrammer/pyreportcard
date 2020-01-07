<br><br>

<h1 align="center">Python Report Card</h1>

<p align="center">
  <a href="/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"/></a>
  <a href="https://docs.python.org/3/index.html"><img src="https://img.shields.io/badge/python-3.6-blue.svg"/></a>
  <a href="https://www.python.org/dev/peps/pep-0008"><img src="https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg"/></a>
  <a href="https://travis-ci.org/mingrammer/pyreportcard"><img src="https://travis-ci.org/mingrammer/pyreportcard.svg?branch=master"/></a>
</p>

<p align="center">
  Analyze and report the python projects which are on Github
</p>

<br><br><br>

> Inspired by [Go Report Card](https://github.com/gojp/goreportcard)

A report card for your Python applications. This analyzes the source code quality (pep8, pyflakes and bandit etc.) of the Python projects which are hosted on GitHub, checks for license and readme files, and provides some statistics. Then shows the results on the web.

You can see our planning for future versions in [here](https://github.com/mingrammer/pyreportcard/projects/1) too.

## ScreenShots

![main](screenshots/main.png)

![report](screenshots/report.png)

## Features

* [x] Supports checking the code quality using PEP8 and Pyflakes linting tools
* [x] Supports counting the code lines and calculates some stats
* [x] Supports checking the license file
* [x] Provides a grade system
* [x] Provides a pyreportcard web server
* [ ] Supports checking the compatibility of Python 2 and 3
* [ ] Supports checking the security issues
* [ ] Supports customizable analyzing using own configuration file
* [ ] Serves it as web service
* [ ] Provides ranking system
* [ ] Provides badge link of repository grade

## Install and Run

* Clone this repository.
* Run `pip install -r requirements.txt` to install all dependencies (If you don't have `pip`, install `pip` first)
* Install the [MongoDB](https://www.mongodb.com/) that is used for our backend database.
* You must configure the secret values in `config_secret.py`. Firstly, copy the example secret file to create secret file by `cp config_secret.py.example config_secret.py`, and then fill out the secret values with yours.

```python
class SecretConfig:
    SECRET_KEY = '...'

    MONGO_DBNAME = 'reportcard'
    MONGO_HOST = '...'
    MONGO_PORT = ...
    # MONGO_USER = '...'
    # MONGO_PASSWORD = '...'
```

* Run server by `python3 run.py`.
* Go `127.0.0.1:5000` and just use it.

It is also possible to run the app and MongoDB in isolated environment using
Docker and [`docker-compose`](https://docs.docker.com/compose/). Follow the
instructions above up until setting the secret values. Then, create a `.env` file
comprises of environment variables for configuring the app in the container.
An example of `.env` is provided below:

```bash
echo "DEBUG=1" >> .env
echo "FLASK_DEBUG=1" >> .env
echo "FLASK_ENVIRONMENT=development" >> .env
```

To run the app and MongoDB, build the app and run them using `docker-compose`.
By default, the app will bind to port `5000` and can be accessed via `localhost`,
e.g. `127.0.0.1:5000`. If the port conflicted with other running apps, feel free
to modify the port binding in `docker-compose.yml` and re-run the app.

```bash
docker-compose up --build -d
```

> Reminder: If you are going to run the app in production, do not forget to turn
> off DEBUG flags in `.env` file and set the environment to `production`.

## Tests

*Note: We have a test code for only vcs module now. We'll add more tests for all features soon*

```bash
python3 -m unittest discover tests
```

## Dependencies
* [PEP8](http://pep8.readthedocs.io/en/release-1.7.x/)
* [Pyflakes](https://github.com/PyCQA/pyflakes)
* [PyMongo](https://github.com/mongodb/mongo-python-driver)
* [Flask](https://github.com/pallets/flask)
* [MongoDB](https://github.com/mongodb/mongo)

## License
The content of this project itself is licensed under the Creative Commons Attribution 3.0 license, and the underlying source code used to format and display that content is licensed under the MIT license.
