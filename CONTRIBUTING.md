# Contributing Guide

The purpose of this guide is to help people get started with making contributions to FASLR. As the project grows these, guidelines should help to establish conventions to keep things organized between contributors.

Since FASLR is still a young project, I would expect these guidelines to rapidly change - for example, there is currently no naming convention for the unit tests, so one will be established in the near future. 

## Virtual Environment

It is recommended that you establish a virtual environment with the following details below.

### Python Version

3.10.2 (main, Jan 15 2022, 18:02:07) [GCC 9.3.0]

### Package Dependencies

FASLR depends on some Python packages. These are listed in the file [requirements.txt](https://github.com/casact/FASLR/blob/main/requirements.txt).

You can install these via pip:

```shell
pip install -r requirements.txt
```

### IDE

I would recommend using PyCharm since it enforces PEP8 and comes with many other features that aid development, like setting up the virtual environment and marking the namespace package. However, you shouldn't feel bound to use this if you have confidence in another IDE.

### Namespace Package

If your IDE has the ability to mark the directory [FASLR/faslr](https://github.com/casact/FASLR/tree/main/faslr) as the Namespace Package, please do so.

## Unit Testing

The unit tests for the project can be found in [FASLR/faslr/tests](https://github.com/casact/FASLR/tree/main/faslr/tests). These are tested using pytest.

## Pull Requests

When making a pull request, please associate it with an outstanding issue. Make sure to run the unit tests using pytest and that they pass. If you are adding a new feature that currently does not have an existing test, please create one for it.