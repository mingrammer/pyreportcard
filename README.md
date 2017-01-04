# Python Report Card
> *Inspired by [Go Report Card](https://github.com/gojp/goreportcard)*

A report card for your Python application. This inspects a python project is hosted on Github and analyze the source code quality (PEP8 and Pyflakes), existence of license file, test coverage, and some statistics of codebase. Then shows its analysis results to user.

It will be served as web service later.

*Note: In current, it is not completed yet. This project is in progress. We'll implement following features ASAP*

## Install and Run

We don't provide installation and running instructions yet. When finished, we'll update it.

## Features
 
* [X] Supports checking the code quality using PEP8 and Pyflakes linting tools
* [X] Supports counting the code lines and calculates some stats
* [X] Supports checking the license file
* [ ] Supports calculating the test coverage and shows test results
* [ ] Supports checking the compatibility of Python 2 and 3
* [X] Provides a grade system
* [ ] Serves it as web service
* [ ] Provides ranking system
* [ ] Provides badge link of repository grade

## Libraries we used
* [PEP8](http://pep8.readthedocs.io/en/release-1.7.x/)
* [Pyflakes](https://github.com/PyCQA/pyflakes)
* [Pymongo](https://github.com/mongodb/mongo-python-driver)
