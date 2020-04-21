
![tests](https://github.com/l0rn/django-minutes/workflows/tests/badge.svg)
[![codecov](https://codecov.io/gh/l0rn/django-minutes/branch/master/graph/badge.svg)](https://codecov.io/gh/l0rn/django-minutes)

# django-minutes

A meeting minutes application for django.

## General / State of development

This application aims to be a easy-to-use free meeting minutes application.

As of now it is in initial development phase. Planned features for initial release are:

* Management of meeting series and meetings
* Role based access control of meetings
* Creating agenda items with markdown-based free text fields
* Mentioning of other people with "@" syntax
* Filtering and notifications on mentions
* Export of meetings in plain text or simple print layout


⚠Before releasing 1.0.0 this project might introduce destructive / incompatible database migrations, so beware of running in production before⚠️

## Developing

### Development environment

Development is currently done with Python `3.8`. A list of supported python versions is TBD. 

### Environment / Dependencies

This project uses [poetry](https://github.com/python-poetry/poetry) for dependency management. A simple `poetry install`
will be sufficient for installing all dependencies. To jump into the environment on your shell use `poetry shell`.

### Linting

The `minutes` folder should be automatically linted. Therefore execute this command to check your code:
```shell script
pylint minutes
```

### Tests

The tests for this applications are to be found in `minutes_tests/`.
The tests make use of a special `settings.py` in `minutes_tests/settings.py`, so run tests either with

```shell script
DJANGO_SETTINGS_MODULE=minutes_tests.settings django-admin test
```

For convenience you can find a `runtests.py` that is basically doing exactly that.

### Workbench

To work on the app it is convenient to have a django project to start it in. For that reason we have `minutes_workbench`
which is a very minimal project loading the app. To start use the following command:

```shell script
DJANGO_SETTINGS_MODULE=minutes_workbench.settings django-admin runserver
```

### Database migrations

You might to execute django database migrations which is possible via

```shell script
DJANGO_SETTINGS_MODULE=minutes_workbench.settings django-admin runserver
```